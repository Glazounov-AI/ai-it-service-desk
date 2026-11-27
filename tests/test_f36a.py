import pytest
from service_desk.diagnostic_case import DiagnosticCase, Evidence, DiagnosticAction
from service_desk.ticket_draft import TicketDraftBuilder


def make_case(category='VPN', subcategory='RESOURCE_ACCESS', group='Network'):
    return DiagnosticCase(session_id='s', revision=5, category=category, subcategory=subcategory,
        issue_summary='Проблема сохраняется.', confirmed_facts=[Evidence(message_id=1,text='Проблема сохраняется.')],
        resolution='not_resolved', support_group=group, priority='normal', escalation_reason='Требуется специалист.',
        created_at='2026-11-26', updated_at='2026-11-26')


def session(status='escalation_required'):
    return dict(id='s',user_id='u',status=status)


def test_vpn_exhaustion_d18():
    b = TicketDraftBuilder()
    c = make_case()
    c.kb_article_ids=['KB-011']
    for i, instruction in enumerate(b.taxonomy.articles[('VPN','RESOURCE_ACCESS')]['user_actions'].split('|'),2):
        c.confirmed_facts.append(Evidence(message_id=i,text='Не помогло.'))
        c.actions.append(DiagnosticAction(action_id=f'KB-011:{i}',instruction=instruction.strip(),status='completed',evidence_message_id=i,result='not_resolved'))
    d=b.build(c,session())
    assert d.troubleshooting_completed and not d.is_complete
    assert d.assigned_group=='Network' and d.kb_article=='KB-011' and d.case_revision==5
    assert len(d.troubleshooting_actions)==4 and d.missing_information
    assert d.status=='draft' and d.action=='escalate'


def test_admin_no_kb():
    d=TicketDraftBuilder().build(make_case('ACCESS','PERMISSIONS','Identity & Access'),session())
    assert d.kb_article is None and not d.troubleshooting_completed and d.is_complete


@pytest.mark.parametrize('status',['new','resolved','closed','ticket_draft_ready'])
def test_wrong_status(status):
    with pytest.raises(ValueError): TicketDraftBuilder().build(make_case(),session(status))


def test_wrong_group():
    with pytest.raises(ValueError): TicketDraftBuilder().build(make_case(group='Other'),session())


def test_missing_evidence():
    c=make_case(); c.actions=[DiagnosticAction(action_id='a',instruction='check',status='completed',evidence_message_id=99)]
    with pytest.raises(ValueError): TicketDraftBuilder().build(c,session())


def test_redaction():
    c=make_case(); c.confirmed_facts.append(Evidence(message_id=2,text='пароль: Secret12345'))
    d=TicketDraftBuilder().build(c,session())
    assert 'Secret12345' not in d.model_dump_json()
