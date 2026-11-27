'use strict';
const $ = id => document.getElementById(id);
const key = 'service-desk-session-v1';
const terminal = new Set(['resolved','escalation_required','ticket_draft_ready','closed']);
const labels = {new:'Новое',clarifying:'Уточнение',troubleshooting:'Диагностика',awaiting_result:'Ожидание результата',resolved:'Решено',escalation_required:'Эскалация',ticket_draft_ready:'Черновик готов',closed:'Закрыто'};
let session = null, busy = false, synchronized = false, draft = null, pendingType = null;
function saved(){try{return localStorage.getItem(key)}catch{return null}}
function remember(id){try{if(id)localStorage.setItem(key,id);else localStorage.removeItem(key)}catch{/* Storage unavailable */}}
async function api(path, method='GET', body){
  const response=await fetch(path,{method,cache:'no-store',headers:body?{'Content-Type':'application/json'}:{},body:body?JSON.stringify(body):undefined});
  if(!response.ok){const error=new Error(`HTTP ${response.status}`);error.status=response.status;throw error;}
  return response.json();
}
function controls(){
  const active=!!session && synchronized && !terminal.has(session.status);
  $('status').textContent=session?(labels[session.status]||session.status):'Нет обращения';
  $('new').disabled=busy;$('refresh').disabled=busy;$('close').disabled=busy||!session||!synchronized||session.status==='closed';
  $('query').disabled=busy||!active;$('send').disabled=busy||!active;
  $('quick').hidden=!active||session.status!=='awaiting_result';
  $('quick').querySelectorAll('button').forEach(b=>{b.disabled=busy||!active; b.hidden=pendingType==='information'?b.dataset.answer!=='Не отображается'&&b.dataset.answer!=='Нет информации'&&b.dataset.answer!=='Проблема устранена': ['Не отображается','Нет информации'].includes(b.dataset.answer)||(pendingType==='remediation'&&['Да','Нет'].includes(b.dataset.answer));});
  $('copy-draft').disabled=busy||!synchronized||!draft;
  $('waiting').textContent=busy?'Выполняется запрос…':'';
}
function render(messages){
  $('chat').replaceChildren();
  for(const message of messages){const el=document.createElement('article');el.className='message '+(message.role==='user'?'user':'assistant');const title=document.createElement('strong');title.textContent=message.role==='user'?'Вы':'IT Service Desk';const content=document.createElement('div');content.textContent=message.content;el.append(title,content);$('chat').append(el);}
  $('chat').scrollTop=$('chat').scrollHeight;
}
function element(tag,text){const node=document.createElement(tag);node.textContent=text;return node;}
const resultLabels={information_reported:'Сведения получены',information_unavailable:'Сведения недоступны',check_positive:'Подтверждено',check_negative:'Не подтверждено',unknown:'Не установлен',resolved:'Устранена',not_resolved:'Не устранена',suggested:'Предложено',completed:'Выполнено',normal:'Обычный',high:'Высокий'};
function value(v){return v==null||v===''?'Не указано':(resultLabels[v]||String(v));}
function fields(parent,entries){const dl=document.createElement('dl');for(const [name,v] of entries){dl.append(element('dt',name),element('dd',value(v)));}parent.append(dl);}
function items(parent,title,values){parent.append(element('h3',title));if(!values.length){parent.append(element('p','Нет данных'));return;}const ul=document.createElement('ul');for(const v of values)ul.append(element('li',v));parent.append(ul);}
function actions(values){return values.map(a=>`${value(a.status)}: ${a.instruction}${a.result?' — '+value(a.result):''}${a.evidence_message_id?' (сообщение '+a.evidence_message_id+')':''}`);}
function clearPanels(){draft=null;pendingType=null;$('diagnostic').replaceChildren();$('draft').replaceChildren();$('panel-status').textContent=session?'Обновление данных…':'Нет обращения';$('copy-status').textContent='';$('copy-draft').disabled=true;}
async function optional(path){try{return await api(path)}catch(e){if(e.status===404)return null;throw e;}}
async function refreshPanels(path){
  const [c,t]=await Promise.allSettled([optional(path+'/diagnostic-case'),optional(path+'/ticket-draft')]);
  $('panel-status').textContent=c.status==='fulfilled'?'Сведения со слов пользователя':'Не удалось загрузить диагностику. Нажмите «Обновить».';
  if(c.status==='fulfilled'&&c.value){const d=c.value,p=$('diagnostic');pendingType=d.actions.find(a=>a.status==='suggested')?.action_type||null;fields(p,[['Категория',d.category],['Подкатегория',d.subcategory],['Приоритет',d.priority],['Описание',d.issue_summary],['Результат',d.resolution],['Группа поддержки',d.support_group],['Причина эскалации',d.escalation_reason]]);items(p,'Сообщённые сведения',d.confirmed_facts.map(e=>e.text));items(p,'Недостающая информация',d.missing_information);items(p,'Диагностические действия',actions(d.actions));items(p,'Статьи базы знаний',d.kb_article_ids);}
  else if(c.status==='fulfilled')$('diagnostic').append(element('p','Диагностический случай ещё не создан.'));
  const p=$('draft');if(t.status==='rejected'){p.append(element('p','Не удалось загрузить черновик. Нажмите «Обновить».'));return;}
  if(!t.value){p.append(element('p','Черновик пока отсутствует.'));return;}
  draft=t.value;fields(p,[['Номер черновика',draft.ticket_id],['Тема',draft.title],['Описание',draft.issue_summary],['Категория',draft.category],['Подкатегория',draft.subcategory],['Группа поддержки',draft.assigned_group],['Приоритет',draft.priority],['Полнота',draft.is_complete?'Достаточно данных':'Требуются сведения'],['Диагностика завершена',draft.troubleshooting_completed?'Да':'Нет'],['Причина эскалации',draft.escalation_reason]]);items(p,'Статьи базы знаний',draft.kb_article_ids);items(p,'Действия',actions(draft.troubleshooting_actions));items(p,'Недостающая информация',draft.missing_information);p.append(element('p','Черновик не отправлен в поддержку.'));
}
$('copy-draft').addEventListener('click',async()=>{if(!draft||busy||!synchronized)return;const text=JSON.stringify(draft,null,2);try{await navigator.clipboard.writeText(text);$('copy-status').textContent='Черновик скопирован.';}catch{ $('copy-status').textContent='Копирование недоступно. Выделите текст карточки вручную.';}});
async function refresh(id){
  synchronized=false;clearPanels();
  const path='/sessions/'+encodeURIComponent(id);
  let state;
  try{state=await api(path)}catch(e){if(e.status===404){session=null;remember(null);render([]);return;}throw e;}
  const messages=await api(path+'/messages');session=state;remember(state.id);render(messages);synchronized=true;await refreshPanels(path);
}
async function run(action){if(busy)return;busy=true;$('error').hidden=true;controls();try{await action()}catch(e){$('error').textContent='Не удалось завершить операцию ('+(e.status?'HTTP '+e.status:'ошибка соединения')+'). Обновите обращение перед повторной отправкой.';$('error').hidden=false;}finally{busy=false;controls();}}
$('new').addEventListener('click',()=>run(async()=>{if(session&&!terminal.has(session.status)&&!confirm('Начать новое обращение? Предыдущее останется в базе.'))return;const created=await api('/sessions','POST',{user_id:'local-web'});session=created;clearPanels();remember(created.id);$('query').value='';render([]);await refresh(created.id);}));
$('refresh').addEventListener('click',()=>run(async()=>{const id=session?.id||saved();if(id)await refresh(id);else await api('/health');}));
$('close').addEventListener('click',()=>run(async()=>{if(!session||!confirm('Закрыть обращение?'))return;const id=session.id;synchronized=false;await api('/sessions/'+encodeURIComponent(id)+'/close','POST');await refresh(id);}));
async function send(text){if(busy||!session||!synchronized||terminal.has(session.status)||!text.trim()||text.trim().length>2000)return;await run(async()=>{const id=session.id;synchronized=false;$('query').value='';try{await api('/sessions/'+encodeURIComponent(id)+'/messages','POST',{query:text.trim()});}catch(e){try{await refresh(id)}catch{/* Keep disabled until refresh */}throw e;}await refresh(id);});}
$('form').addEventListener('submit',e=>{e.preventDefault();send($('query').value);});
$('quick').addEventListener('click',e=>{if(e.target.dataset.answer)send(e.target.dataset.answer);});
controls();run(async()=>{const id=saved();if(id)await refresh(id);else await api('/health');});
