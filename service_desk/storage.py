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
            db.execute('INSERT INTO messages(session_id,role,content,metadata_json,created_at) VALUES (?,?,?,?,?)',
                       (sid,role,content,json.dumps(metadata or {},ensure_ascii=False),stamp))
            db.execute('UPDATE sessions SET updated_at=? WHERE id=?', (stamp,sid))

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
