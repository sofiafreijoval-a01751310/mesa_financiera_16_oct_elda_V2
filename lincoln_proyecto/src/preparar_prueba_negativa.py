import json,uuid
from pathlib import Path
R=Path(__file__).resolve().parents[1];base=json.loads((R/'exports/Lincoln_Proxy_OpenAI_CANDIDATO_PUBLICO.json').read_text());core=(R/'src/n8n_guard/ledger.js').read_text()
w={'name':'Lincoln | Pruebas negativas guardián SIN MODELOS','active':False,'nodes':[],'connections':{},'settings':{'executionOrder':'v1','executionTimeout':120},'pinData':{}}
def add(name,t,p,v=2):
 prev=w['nodes'][-1]['name'] if w['nodes'] else None
 w['nodes'].append({'name':name,'id':str(uuid.uuid5(uuid.NAMESPACE_URL,'lincoln-test/'+name)),'type':'n8n-nodes-base.'+t,'typeVersion':v,'parameters':p,'position':[len(w['nodes'])*240,0]})
 if prev:w['connections'][prev]={'main':[[{'node':name,'type':'main','index':0}]]}
add('Prueba manual','manualTrigger',{},1)
r=next(n for n in base['nodes'] if n['name']=='Leer reserva')['parameters'];r['dataTableId']['value']='CONFIGURAR_TABLA_lincoln_guard_ledger';add('Leer ledger','dataTable',r,1.1)
add('Preparar fixture','code',{'jsCode':core+'''
const rows=$input.all().map(i=>i.json);if(rows.length!==1||rows[0].id!==1)throw Error('Ledger ambiguo');
const old_json=rows[0].state_json,s=readLedger(old_json),e=String($execution.id),case_id='LIN-'+e+'000-1',parallel_case='LIN-'+e+'001-1';
if(s.cases.some(c=>c.case_id===case_id)||s.cases.length>=98)throw Error('Fixture repetido');
s.cases.push({case_id,event_id:'manual:'+e+'000',created:new Date().toISOString(),capNano:POLICY.capNano});
for(let i=0;i<11;i++)s.requests.push({id:'TEST_BUDGET_'+e+'_'+i,case_id,state:'RESERVADO',reservedNano:quote(),actualNano:null,model:POLICY.model,created:new Date().toISOString(),diagnostico:'RESERVA_SINTETICA_SIN_LLAMADA_API'});
s.seq++;const next_json=JSON.stringify(s);readLedger(next_json);
return [{json:{old_json,next_json,case_id,parallel_case,event_id:'manual:'+e+'001'}}];
'''})
c=next(n for n in base['nodes'] if n['name']=='Reservar CAS')['parameters'];c['dataTableId']['value']='CONFIGURAR_TABLA_lincoln_guard_ledger';c['filters']['conditions'][1]['keyValue']='={{ $json.old_json }}';c['columns']['value']['state_json']='={{ $json.next_json }}';add('Guardar fixture CAS','dataTable',c,1.1)
add('Verificar fixture y lote','code',{'jsCode':core+'''
const row=$input.first().json,f=$('Preparar fixture').first().json;if(row.id!==1||row.state_json!==f.next_json)throw Error('CAS no confirmado');
const s=readLedger(row.state_json),rr=s.requests.filter(r=>r.case_id===f.case_id);if(rr.length!==11||rr.some(r=>r.state!=='RESERVADO'||r.actualNano!==null))throw Error('Fixture inválido');
const budget={case_id:f.case_id,path:'chat/completions',body:{model:POLICY.model,messages:[{role:'user',content:'Prueba sintética que debe bloquearse antes de API.'}],max_tokens:1,stream:false}};
const admit={case_id:f.parallel_case,path:'admit',body:{case_id:f.parallel_case,event_id:f.event_id}};
return [budget,admit,admit].map(x=>({json:x}));
'''})
add('Probar lote protegido','httpRequest',{'method':'POST','url':'={{ "https://sofiafreijo.app.n8n.cloud/webhook/lincoln-llm-guard/v1/"+$json.path }}','authentication':'genericCredentialType','genericAuthType':'httpHeaderAuth','sendHeaders':True,'headerParameters':{'parameters':[{'name':'X-Lincoln-Case','value':'={{ $json.case_id }}'}]},'sendBody':True,'contentType':'raw','rawContentType':'application/json','body':'={{ JSON.stringify($json.body) }}','options':{'timeout':20000,'response':{'response':{'fullResponse':True,'neverError':True,'responseFormat':'json'}},'batching':{'batch':{'batchSize':3,'batchInterval':0}}}},4.2)
add('Verificar resultados','code',{'jsCode':"const rr=$input.all().map(i=>i.json);const admit=rr.filter(r=>r.statusCode===200&&r.body?.admitido===true),dupe=rr.filter(r=>r.statusCode===409&&r.body?.error?.code==='DUPLICADO'),cost=rr.filter(r=>r.statusCode===409&&r.body?.error?.code==='LIMITE_COSTO');if(rr.length!==3||admit.length!==1||dupe.length!==1||cost.length!==1)throw Error('No se acreditaron los tres controles');return [{json:{ok:true,admisiones:1,duplicados_bloqueados:1,corte_costo_previo:true,resultados:rr.map(r=>({status:r.statusCode,code:r.body?.error?.code??'ADMITIDO'})),fixtures:'Once reservas sintéticas, no llamadas API ni consumo real.',alcance:'Mismo lote HTTP de tres peticiones; no certifica toda concurrencia posible.'}}];"})
for n in w['nodes']:
 if n['parameters'].get('jsCode'):compile('pass','x','exec')
(R/'exports/Lincoln_Prueba_Guard_Negativa_PUBLICO.json').write_text(json.dumps(w,ensure_ascii=False,indent=2))
print({'nodes':len(w['nodes']),'active':False})
