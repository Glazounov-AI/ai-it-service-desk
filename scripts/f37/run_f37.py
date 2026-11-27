import argparse,json,time,urllib.request,urllib.error
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--output',required=True); p.add_argument('--base',default='http://127.0.0.1:9992'); p.add_argument('--pause',type=float,default=13); a=p.parse_args()
scenarios=json.loads(Path(__file__).with_name('scenarios.json').read_text(encoding='utf-8')); report={'scenarios':[],'additional':[]}; out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
def save(): out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def call(path,method='GET',body=None):
    t=time.monotonic(); status=0; data=None; error=None
    try:
        req=urllib.request.Request(a.base+path,data=json.dumps(body,ensure_ascii=False).encode() if body is not None else None,headers={'Content-Type':'application/json'},method=method)
        try: r=urllib.request.urlopen(req,timeout=40)
        except urllib.error.HTTPError as e: r=e
        with r: status=r.code; data=json.loads(r.read())
    except Exception as e: error=str(e)
    return {'status':status,'body':data,'elapsed_ms':round((time.monotonic()-t)*1000),'error':error}
assert call('/health')['status']==200,'Service Desk unavailable'
for s in scenarios:
    item={'id':s['id'],'query':s['query'],'expected_classification':s['expected'],'calls':{},'checks':{},'manual_review':'pending'}; report['scenarios'].append(item); c=item['calls']; checks=item['checks']; c['create']=call('/sessions','POST',{'user_id':'f37-'+s['id']}); sid=(c['create']['body'] or {}).get('id'); checks['created']=c['create']['status']==201 and bool(sid)
    if sid:
        path='/sessions/'+sid; c['answer']=call(path+'/messages','POST',{'query':s['query']}); c['session']=call(path); c['case']=call(path+'/diagnostic-case'); c['history']=call(path+'/messages'); c['draft']=call(path+'/ticket-draft'); b=c['answer']['body'] or {}; cl=b.get('classification') or {}; state=(c['session']['body'] or {}).get('status'); case=c['case']['body'] or {}; draft=c['draft']['body'] or {}; checks['http']=c['answer']['status']==200 and all(c[k]['status']==200 for k in ('session','case','history')) and c['draft']['status'] in (200,404)
        for k,v in s['expected'].items(): checks['classification_'+k]=v in cl.get('safety_flags',[]) if k=='flag' else cl.get(k)==v
        n=int(s['id'][-3:]); kb={1:'KB-007',2:'KB-009',3:'KB-013',4:'KB-014',5:'KB-015',21:'KB-016'}
        if n in kb: checks['diagnostic_started']=state=='awaiting_result'; checks['targeted_source']=b.get('strategy')=='targeted' and bool(b.get('retrieved_sources')) and all(x.get('source')==kb[n]+'.md' for x in b['retrieved_sources'])
        if 6<=n<=10: checks['clarifying']=state=='clarifying' and not case.get('actions') and not b.get('retrieved_sources')
        if n in (11,13,15,18,19,22):
            checks['escalation_draft']=state=='ticket_draft_ready' and c['draft']['status']==200 and bool(draft.get('ticket_id'))
            group={11:'Identity & Access',13:'Workplace',15:'Network',18:'Identity & Access',22:'Network'}.get(n)
            if group: checks['group']=draft.get('assigned_group')==group
        if n==12: checks['alternative_mfa_question']=state in ('clarifying','awaiting_result') and '?' in b.get('answer','')
        if n==14: checks['no_repeated_reconnect']=state=='awaiting_result' and 'повторно подключить VPN' not in b.get('answer','')
        if n in (16,17,20): checks['local_safety']=bool(cl.get('safety_flags')) and b.get('model')=='local-decision' and not b.get('retrieved_sources') and c['draft']['status']==404
        if n==22: checks['draft_fields']=all(draft.get(k)==v for k,v in dict(category='VPN',subcategory='RESOURCE_ACCESS',priority='normal',assigned_group='Network',kb_article='KB-011',troubleshooting_completed=True,resolution='not_resolved',action='escalate',is_complete=False).items())
        if n in (11,13): checks['kb_reference']=draft.get('kb_article')=={11:'KB-002',13:'KB-012'}[n]
    item['automatic_pass']=all(checks.values()); save(); print(s['id'], 'PASS' if item['automatic_pass'] else 'REVIEW', [k for k,v in checks.items() if not v],flush=True); time.sleep(a.pause)
def extra(name,path,method='GET',body=None,expected=200):
    r=call(path,method,body); report['additional'].append({'id':name,'expected':expected,'response':r,'pass':r['status']==expected}); save()
extra('invalid_query','/consult','POST',{'query':''},422); extra('missing_session','/sessions/00000000-0000-0000-0000-000000000000',expected=404)
c=call('/sessions','POST',{'user_id':'f37-boundary'}); sid=(c['body'] or {}).get('id');
if sid:
    path='/sessions/'+sid; extra('premature_draft',path+'/ticket-draft','POST',expected=409); extra('close',path+'/close','POST'); extra('closed_message',path+'/messages','POST',{'query':'Не работает VPN.'},409)
    
report['automatic_passed']=sum(x['automatic_pass'] for x in report['scenarios']); report['total']=len(scenarios); save(); print('Automatic:',report['automatic_passed'],'/',report['total'],'; manual review pending; report:',out)
