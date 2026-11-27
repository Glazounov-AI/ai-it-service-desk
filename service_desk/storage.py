from .ticket_draft import TicketDraft, TicketDraftBuilder
from .diagnostic_case import DiagnosticCase
import sqlite3
import json
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def now():
    return datetime.now(timezone.utc).isoformat()


class SessionError(Exception):
    def __init__(self, status, message):
        self.status = status
        super().__init__(message)


TRANSITIONS = {
    'new': {'clarifying', 'troubleshooting', 'escalation_required', 'closed'},
    'clarifying': {'troubleshooting', 'escalation_required', 'closed'},
    'troubleshooting': {'awaiting_result', 'escalation_required', 'closed'},
    'awaiting_result': {'troubleshooting', 'resolved', 'escalation_required', 'closed'},
    'resolved': {'closed'},
    'escalation_required': {'ticket_draft_ready', 'closed'},
    'ticket_draft_ready': {'closed'},
    'closed': set(),
}


class SQLiteRepository:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY, user_id TEXT NOT NULL,
                    status TEXT NOT NULL, created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL, closed_at TEXT
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id),
                    role TEXT NOT NULL CHECK(role IN ('user','assistant')),
                    content TEXT NOT NULL, metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS diagnostic_cases (
                    session_id TEXT PRIMARY KEY REFERENCES sessions(id),
                    revision INTEGER NOT NULL, payload_json TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS ticket_drafts (
                    session_id TEXT PRIMARY KEY REFERENCES sessions(id),
                    ticket_id TEXT NOT NULL UNIQUE, payload_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS messages_session ON messages(session_id,id);
            ''')

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=2)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        try:
            with db:
                yield db
        finally:
            db.close()

    def _get(self, db, session_id):
        row = db.execute('SELECT * FROM sessions WHERE id=?', (session_id,)).fetchone()
        if row is None:
            raise SessionError(404, 'Сессия не найдена')
        return dict(row)

    def create(self, user_id):
        sid, stamp = str(uuid4()), now()
        with self.connection() as db:
            db.execute('INSERT INTO sessions VALUES (?,?,?,?,?,NULL)', (sid,user_id,'new',stamp,stamp))
            return self._get(db, sid)

    def get(self, sid):
        with self.connection() as db:
            return self._get(db, sid)

    def transition(self, sid, target):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            session = self._get(db, sid)
            if target not in TRANSITIONS[session['status']]:
                raise SessionError(409, 'Недопустимый переход состояния')
            stamp = now()
            db.execute('UPDATE sessions SET status=?, updated_at=?, closed_at=? WHERE id=?',
                       (target, stamp, stamp if target == 'closed' else None, sid))
            return self._get(db, sid)

    def append(self, sid, role, content, metadata=None):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            session = self._get(db, sid)
            if session['status'] in {'closed', 'resolved', 'ticket_draft_ready'}:
                raise SessionError(409, 'Сессия не принимает сообщения')
            stamp = now()
            cursor = db.execute('INSERT INTO messages(session_id,role,content,metadata_json,created_at) VALUES (?,?,?,?,?)',
                       (sid,role,content,json.dumps(metadata or {},ensure_ascii=False),stamp))
            db.execute('UPDATE sessions SET updated_at=? WHERE id=?', (stamp,sid))
            return cursor.lastrowid

    def messages(self, sid):
        with self.connection() as db:
            self._get(db, sid)
            rows = db.execute('SELECT * FROM messages WHERE session_id=? ORDER BY id', (sid,)).fetchall()
            result = []
            for row in rows:
                item = dict(row)
                item['metadata'] = json.loads(item.pop('metadata_json'))
                result.append(item)
            return result

    def recent_messages(self, sid):
        with self.connection() as db:
            self._get(db, sid)
            rows = db.execute('SELECT role,content FROM messages WHERE session_id=? ORDER BY id DESC LIMIT 6', (sid,)).fetchall()
            return [dict(row) for row in reversed(rows)]

    def get_case(self, sid):
        with self.connection() as db:
            session = self._get(db, sid)
            row = db.execute('SELECT payload_json FROM diagnostic_cases WHERE session_id=?', (sid,)).fetchone()
            if row:
                return DiagnosticCase.model_validate_json(row['payload_json'])
            return DiagnosticCase(session_id=sid, created_at=session['created_at'], updated_at=session['created_at'])

    def save_case(self, case):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            session = self._get(db, case.session_id)
            if session['status'] in {'closed', 'resolved', 'ticket_draft_ready'}:
                raise SessionError(409, 'Сессия не принимает изменения')
            row = db.execute('SELECT revision FROM diagnostic_cases WHERE session_id=?', (case.session_id,)).fetchone()
            if (row['revision'] if row else 0) != case.revision:
                raise SessionError(409, 'Конфликт версии диагностики')
            for evidence in case.confirmed_facts:
                source = db.execute('SELECT role,content FROM messages WHERE id=? AND session_id=?', (evidence.message_id, case.session_id)).fetchone()
                if not source or source['role'] != 'user' or source['content'] != evidence.text:
                    raise SessionError(409, 'Недопустимый источник сведений')
            updated = case.model_copy(update={'revision': case.revision + 1, 'updated_at': now()})
            db.execute('INSERT INTO diagnostic_cases VALUES (?,?,?) ON CONFLICT(session_id) DO UPDATE SET revision=excluded.revision,payload_json=excluded.payload_json', (updated.session_id, updated.revision, updated.model_dump_json()))
            return updated

    def finish_diagnostic_turn(self, case, status, target, result):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            session = self._get(db, case.session_id)
            if session['status'] != status:
                raise SessionError(409, 'Конфликт состояния')
            row = db.execute('SELECT revision FROM diagnostic_cases WHERE session_id=?', (case.session_id,)).fetchone()
            if (row['revision'] if row else 0) != case.revision:
                raise SessionError(409, 'Конфликт версии диагностики')
            for e in case.confirmed_facts:
                source = db.execute('SELECT role,content FROM messages WHERE id=? AND session_id=?', (e.message_id,case.session_id)).fetchone()
                if not source or source['role'] != 'user' or source['content'] != e.text:
                    raise SessionError(409, 'Недопустимый источник сведений')
            for a in case.actions:
                if a.status == 'completed' and a.evidence_message_id not in {e.message_id for e in case.confirmed_facts}:
                    raise SessionError(409, 'Нет подтверждения действия')
            path = []
            if target == 'awaiting_result' and status in {'new','clarifying'}:
                path.append('troubleshooting')
            if target != status:
                path.append(target)
            for step in path:
                if step not in TRANSITIONS[status]:
                    raise SessionError(409, 'Недопустимый переход состояния')
                status = step
            stamp = now()
            updated = case.model_copy(update={'revision':case.revision+1,'updated_at':stamp})
            db.execute('INSERT INTO diagnostic_cases VALUES (?,?,?) ON CONFLICT(session_id) DO UPDATE SET revision=excluded.revision,payload_json=excluded.payload_json', (case.session_id,updated.revision,updated.model_dump_json()))
            if status == 'escalation_required':
                draft = self._insert_draft(db, updated, dict(session, status=status))
                status = 'ticket_draft_ready'
                result.answer += ' Черновик заявки подготовлен; заявка не отправлена.'
            db.execute('INSERT INTO messages(session_id,role,content,metadata_json,created_at) VALUES (?,?,?,?,?)', (case.session_id,'assistant',result.answer,json.dumps(result.model_dump(exclude={'query','answer'}),ensure_ascii=False),stamp))
            db.execute('UPDATE sessions SET status=?,updated_at=? WHERE id=?',(status,stamp,case.session_id))

    def _insert_draft(self, db, case, session):
        try:
            draft = TicketDraftBuilder().build(case, session)
        except ValueError:
            raise SessionError(409, 'Недостаточно подтвержденных данных для черновика') from None
        db.execute('INSERT INTO ticket_drafts VALUES (?,?,?)', (case.session_id, draft.ticket_id, draft.model_dump_json()))
        return draft

    def get_ticket_draft(self, sid):
        with self.connection() as db:
            self._get(db, sid)
            row = db.execute('SELECT payload_json FROM ticket_drafts WHERE session_id=?', (sid,)).fetchone()
            if not row:
                raise SessionError(404, 'Черновик не найден')
            return TicketDraft.model_validate_json(row['payload_json'])

    def ensure_ticket_draft(self, sid):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            session = self._get(db, sid)
            row = db.execute('SELECT payload_json FROM ticket_drafts WHERE session_id=?', (sid,)).fetchone()
            if row:
                return TicketDraft.model_validate_json(row['payload_json'])
            if session['status'] != 'escalation_required':
                raise SessionError(409, 'Сессия не требует эскалации')
            row = db.execute('SELECT payload_json FROM diagnostic_cases WHERE session_id=?', (sid,)).fetchone()
            if not row:
                raise SessionError(409, 'Диагностика отсутствует')
            case = DiagnosticCase.model_validate_json(row['payload_json'])
            for e in case.confirmed_facts:
                source = db.execute('SELECT role,content FROM messages WHERE id=? AND session_id=?', (e.message_id,sid)).fetchone()
                if not source or source['role'] != 'user' or source['content'] != e.text:
                    raise SessionError(409, 'Недопустимый источник сведений')
            draft = self._insert_draft(db, case, session)
            db.execute('UPDATE sessions SET status=?,updated_at=? WHERE id=?', ('ticket_draft_ready',now(),sid))
            return draft
