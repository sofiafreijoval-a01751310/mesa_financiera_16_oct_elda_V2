"""Candidato inactivo: n8n DataTable CAS + API OpenAI. No usa credenciales ni red."""
import json,uuid
from pathlib import Path
R=Path(__file__).resolve().parents[1]
core=(R/'src/n8n_guard/ledger.js').read_text()
W={'name':'Lincoln | Proxy OpenAI con reserva previa | CANDIDATO','active':False,'nodes':[],'connections':{},'settings':{'executionOrder':'v1','executionTimeout':240,'saveDataErrorExecution':'none','saveDataSuccessExecution':'none','saveManualExecutions':False,'saveExecutionProgress':False,'availableInMCP':False},'pinData':{}}
def node(name,typ,p,ver=2,**extra):
 n={'id':str(uuid.uuid5(uuid.NAMESPACE_URL,'lincoln-guard/'+name)),'name':name,'type':'n8n-nodes-base.'+typ,'typeVersion':ver,'position':[len(W['nodes'])*210,0],'parameters':p,**extra};W['nodes'].append(n);return n

def code(name,s):return node(name,'code',{'jsCode':s})
def edge(a,b,out=0):
 c=W['connections'].setdefault(a,{'main':[]})['main']
 while len(c)<=out:c.append([])
 c[out].append({'node':b,'type':'main','index':0})

def cond(name,expression):return node(name,'if',{'conditions':{'options':{'caseSensitive':True,'typeValidation':'strict','version':2},'conditions':[{'id':str(uuid.uuid5(uuid.NAMESPACE_URL,name)),'leftValue':'={{ '+expression+' }}','rightValue':True,'operator':{'type':'boolean','operation':'true','singleValue':True}}],'combinator':'and'},'options':{}},2.2)

def read(name):return node(name,'dataTable',{'operation':'get','dataTableId':{'__rl':True,'value':'CONFIGURAR_TABLA_lincoln_guard_ledger','mode':'id'},'matchType':'allConditions','filters':{'conditions':[{'keyValue':1}]},'returnAll':False,'limit':2},1.1,alwaysOutputData=True)

def cas(name,source):return node(name,'dataTable',{'operation':'update','dataTableId':{'__rl':True,'value':'CONFIGURAR_TABLA_lincoln_guard_ledger','mode':'id'},'matchType':'allConditions','filters':{'conditions':[{'keyValue':1},{'keyName':'state_json','keyValue':'={{ $("'+source+'").item.json.old_json }}'}]},'columns':{'mappingMode':'defineBelow','value':{'state_json':'={{ $("'+source+'").item.json.next_json }}'},'matchingColumns':[],'schema':[{'id':'state_json','displayName':'state_json','type':'string','required':False,'defaultMatch':False,'display':True,'readOnly':False,'removed':False}],'attemptToConvertTypes':False,'convertFieldsToString':False},'options':{}},1.1,alwaysOutputData=True)
for kind,path in [('call','chat/completions'),('admit','admit')]:
 node('Webhook '+kind,'webhook',{'httpMethod':'POST','path':'lincoln-llm-guard/v1/'+path,'authentication':'headerAuth','responseMode':'responseNode','options':{}},2.1)
 code('Ruta '+kind,"return $input.all().map(i=>({json:{...i.json,kind:'"+kind+"'}}));")
 edge('Webhook '+kind,'Ruta '+kind);edge('Ruta '+kind,'Normalizar')
code('Normalizar',core+'''
try {
 const i=$input.first().json,case_id=String(i.headers?.['x-lincoln-case']??'');
 if(!/^LIN-\\d+-\\d+$/.test(case_id))fail('CASO_INVALIDO');
 const req={kind:i.kind,id:String($execution.id),case_id};
 if(req.kind==='admit'){if(!i.body||i.body.case_id!==case_id)fail('CASO_INVALIDO');req.event_id=i.body.event_id;}
 else {req.body=i.body;Object.assign(req,normalizeCall(req.body));}
 return [{json:{ok:true,req}}];
}catch(e){return [{json:{ok:false,code:e.code??'ESQUEMA_INVALIDO',status:400}}];}
''')
cond('Solicitud válida','$json.ok===true');edge('Normalizar','Solicitud válida');edge('Solicitud válida','Leer reserva');edge('Solicitud válida','Responder error',1)
read('Leer reserva')
code('Plan reserva',core+'''
try {
 if($runIndex>=3)fail('CONFLICTO_PERSISTENTE');
 const rows=$input.all().map(i=>i.json);if(rows.length!==1||rows[0].id!==1||typeof rows[0].state_json!=='string')fail('INICIALIZAR_LEDGER');
 const old_json=rows[0].state_json,req=$('Normalizar').first().json.req;
 return [{json:{ok:true,old_json,next_json:plan(old_json,req,Date.now())}}];
}catch(e){return [{json:{ok:false,code:e.code??'LEDGER_INVALIDO',status:409}}];}
''')
cond('Puede reservar','$json.ok===true');edge('Leer reserva','Plan reserva');edge('Plan reserva','Puede reservar');edge('Puede reservar','Reservar CAS');edge('Puede reservar','Responder error',1)
cas('Reservar CAS','Plan reserva')
code('Verificar reserva',core+'''
try {
 const rows=$input.all().map(i=>i.json),req=$('Normalizar').first().json.req;
 if(rows.length!==1||rows[0].id!==1||typeof rows[0].state_json!=='string')return [{json:{ok:false,retry:true}}];
 const s=readLedger(rows[0].state_json);
 const owned=req.kind==='admit'?s.cases.some(c=>c.case_id===req.case_id&&c.event_id===req.event_id):s.requests.some(r=>r.id===req.id&&r.case_id===req.case_id&&r.state==='RESERVADO'&&r.reservedNano===quote());
 return [{json:{ok:owned,retry:!owned}}];
}catch(e){return [{json:{ok:false,retry:false,code:'LEDGER_INVALIDO',status:409}}];}
''')
cond('Reserva propia','$json.ok===true');cond('Reintentar reserva','$json.retry===true');edge('Reservar CAS','Verificar reserva');edge('Verificar reserva','Reserva propia');edge('Reserva propia','Es admisión');edge('Reserva propia','Reintentar reserva',1);edge('Reintentar reserva','Leer reserva');edge('Reintentar reserva','Responder error',1)
cond('Es admisión','$("Normalizar").first().json.req.kind==="admit"');edge('Es admisión','Responder admisión');edge('Es admisión','OpenAI controlado',1)
node('OpenAI controlado','httpRequest',{'method':'POST','url':'https://api.openai.com/v1/chat/completions','authentication':'predefinedCredentialType','nodeCredentialType':'openAiApi','sendBody':True,'contentType':'raw','rawContentType':'application/json','body':'={{ JSON.stringify($("Normalizar").first().json.req.upstream) }}','options':{'timeout':60000,'redirect':{'redirect':{'followRedirects':False}},'response':{'response':{'fullResponse':True,'neverError':True,'responseFormat':'json'}}}},4.2,onError='continueRegularOutput',retryOnFail=False)
read('Leer conciliación');edge('OpenAI controlado','Leer conciliación')
code('Plan conciliación',core+'''
try {
 if($runIndex>=3)fail('CONCILIACION_PENDIENTE');
 const rows=$input.all().map(i=>i.json);if(rows.length!==1||rows[0].id!==1||typeof rows[0].state_json!=='string')fail('LEDGER_INVALIDO');
 const req=$('Normalizar').first().json.req,r=$('OpenAI controlado').first().json;
 const old_json=rows[0].state_json,next_json=reconcile(old_json,req,r.statusCode===200?r.body:{},Date.now());
 return [{json:{ok:true,old_json,next_json}}];
}catch(e){return [{json:{ok:false,code:e.code??'CONCILIACION_PENDIENTE',status:502}}];}
''')
cond('Puede conciliar','$json.ok===true');edge('Leer conciliación','Plan conciliación');edge('Plan conciliación','Puede conciliar');edge('Puede conciliar','Conciliar CAS');edge('Puede conciliar','Responder error',1)
cas('Conciliar CAS','Plan conciliación')
code('Verificar conciliación',core+'''
try {
 const rows=$input.all().map(i=>i.json),req=$('Normalizar').first().json.req;
 if(rows.length!==1||rows[0].id!==1||typeof rows[0].state_json!=='string')return [{json:{ok:false,retry:true}}];
 const r=readLedger(rows[0].state_json).requests.find(r=>r.id===req.id&&r.case_id===req.case_id);
 if(r?.state==='CONCILIADO')return [{json:{ok:true,retry:false}}];
 if(r?.state==='INCIERTO')return [{json:{ok:false,retry:false,code:'USAGE_INCIERTO',status:502}}];
 return [{json:{ok:false,retry:true}}];
}catch(e){return [{json:{ok:false,retry:false,code:'CONCILIACION_PENDIENTE',status:502}}];}
''')
cond('Conciliación propia','$json.ok===true');cond('Reintentar conciliación','$json.retry===true');edge('Conciliar CAS','Verificar conciliación');edge('Verificar conciliación','Conciliación propia');edge('Conciliación propia','Formar respuesta');edge('Conciliación propia','Reintentar conciliación',1);edge('Reintentar conciliación','Leer conciliación');edge('Reintentar conciliación','Responder error',1)
code('Formar respuesta',core+"\nreturn [{json:responseEnvelope($('OpenAI controlado').first().json.body,$('Normalizar').first().json.req.clientStream)}];")
node('Responder modelo','respondToWebhook',{'respondWith':'text','responseBody':'={{ $json.body }}','options':{'responseHeaders':{'entries':[{'name':'Content-Type','value':'={{ $json.contentType }}'},{'name':'Cache-Control','value':'no-store'}]}}},1.4);edge('Formar respuesta','Responder modelo')
node('Responder admisión','respondToWebhook',{'respondWith':'json','responseBody':'={{ {ok:true,admitido:true,caso_id:$("Normalizar").first().json.req.case_id} }}','options':{'responseHeaders':{'entries':[{'name':'Cache-Control','value':'no-store'}]}}},1.4)
node('Responder error','respondToWebhook',{'respondWith':'json','responseBody':'={{ {error:{message:"Control Lincoln: "+($json.code??"CONTROL_BLOQUEADO"),type:"lincoln_guard",code:$json.code??"CONTROL_BLOQUEADO"},ok:false,admitido:false} }}','options':{'responseCode':'={{ $json.status??409 }}','responseHeaders':{'entries':[{'name':'Cache-Control','value':'no-store'}]}}},1.4)
(R/'exports/Lincoln_Proxy_OpenAI_CANDIDATO_PUBLICO.json').write_text(json.dumps(W,ensure_ascii=False,indent=2))
print(f'Proxy inactivo generado: {len(W["nodes"])}nodos. Falta tabla, credenciales y prueba viva CAS.')
