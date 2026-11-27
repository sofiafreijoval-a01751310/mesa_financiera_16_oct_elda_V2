// Política del servidor. Importes en nanoUSD (1 USD=1e9); no usa valores de costo del cliente.
const POLICY=Object.freeze({model:'gpt-4o-mini-2024-07-18',contextTokens:128000,maxOutputTokens:4096,inputNanoPerToken:150,outputNanoPerToken:600,capNano:250000000,maxCalls:25,maxCases:100,maxSeconds:360,validUntil:'2026-12-04T00:00:00Z'});
function fail(code){const e=new Error(code);e.code=code;throw e;}
function safeInt(n,max=Number.MAX_SAFE_INTEGER){if(!Number.isSafeInteger(n)||n<0||n>max)fail('LEDGER_INVALIDO');return n;}
function emptyLedger(){return {schema:1,seq:0,cases:[],requests:[]};}
function readLedger(raw){let s;try{s=JSON.parse(raw);}catch{fail('LEDGER_INVALIDO');}
 if(!s||s.schema!==1||!Array.isArray(s.cases)||!Array.isArray(s.requests)||s.cases.length>POLICY.maxCases||s.requests.length>2500)fail('LEDGER_INVALIDO');
 safeInt(s.seq);const seen=new Set(),events=new Set();
 for(const c of s.cases){if(!c||!/^LIN-\d+-\d+$/.test(c.case_id)||seen.has(c.case_id)||typeof c.event_id!=='string'||!c.event_id||events.has(c.event_id)||c.capNano!==POLICY.capNano||!Number.isFinite(Date.parse(c.created)))fail('LEDGER_INVALIDO');seen.add(c.case_id);events.add(c.event_id);}
 const ids=new Set();for(const r of s.requests){if(!r||typeof r.id!=='string'||ids.has(r.id)||!seen.has(r.case_id)||!['RESERVADO','CONCILIADO','INCIERTO'].includes(r.state))fail('LEDGER_INVALIDO');ids.add(r.id);safeInt(r.reservedNano);if(r.actualNano!==null)safeInt(r.actualNano);if(r.state==='CONCILIADO'&&r.actualNano===null)fail('LEDGER_INVALIDO');}
 for(const c of s.cases){const total=s.requests.filter(r=>r.case_id===c.case_id).reduce((a,r)=>a+(r.actualNano??r.reservedNano),0);safeInt(total);if(total>c.capNano&&!s.requests.some(r=>r.case_id===c.case_id&&r.state==='INCIERTO'))fail('LEDGER_INVALIDO');}return s;
}
function quote(){return POLICY.contextTokens*POLICY.inputNanoPerToken+POLICY.maxOutputTokens*POLICY.outputNanoPerToken;}
function normalizeCall(body){
 if(!body||typeof body!=='object'||Array.isArray(body)||JSON.stringify(body).length>300000)fail('ESQUEMA_INVALIDO');
 const allowed=new Set(['model','messages','tools','tool_choice','parallel_tool_calls','temperature','top_p','response_format','stop','frequency_penalty','presence_penalty','seed','max_tokens','max_completion_tokens','stream','stream_options','n','user','service_tier','store']);
 if(Object.keys(body).some(k=>!allowed.has(k))||body.model!==POLICY.model||!Array.isArray(body.messages)||!body.messages.length||body.messages.length>100)fail('ESQUEMA_INVALIDO');
 const messages=body.messages.map(m=>{
  if(!m||!['system','developer','user','assistant','tool'].includes(m.role))fail('SOLO_TEXTO');
  const calls=m.role==='assistant'&&Array.isArray(m.tool_calls)&&m.tool_calls.length>0&&m.tool_calls.length<=10&&m.tool_calls.every(t=>typeof t.id==='string'&&t.id.length>0&&t.type==='function'&&typeof t.function?.name==='string'&&typeof t.function?.arguments==='string');
  if((m.content===undefined||(Array.isArray(m.content)&&m.content.length===0))&&calls)return {...m,content:null};
  if(Array.isArray(m.content)&&m.content.length>0&&m.content.every(p=>p&&p.type==='text'&&typeof p.text==='string'&&Object.keys(p).every(k=>['type','text'].includes(k))))return {...m,content:m.content.map(p=>p.text).join('\n')};
  if(m.content!==null&&typeof m.content!=='string')fail('SOLO_TEXTO_'+m.role+'_'+(Array.isArray(m.content)?'array_'+m.content.length:typeof m.content));
  return m;
 });
 if(body.n!==undefined&&body.n!==1)fail('MULTIPLES_SALIDAS');
 if(body.service_tier!==undefined&&body.service_tier!=='default')fail('TARIFA_NO_AUTORIZADA');
 const max=body.max_completion_tokens??body.max_tokens??POLICY.maxOutputTokens;
 if(!Number.isInteger(max)||max<1||max>POLICY.maxOutputTokens)fail('LIMITE_SALIDA');
 if(body.tools!==undefined&&(!Array.isArray(body.tools)||body.tools.length>10||body.tools.some(t=>t.type!=='function'||typeof t.function?.name!=='string')))fail('HERRAMIENTA_INVALIDA');
 const upstream={...body,messages,stream:false,n:1,service_tier:'default',store:false,max_tokens:max};delete upstream.max_completion_tokens;delete upstream.stream_options;delete upstream.user;
 return {upstream,clientStream:body.stream===true};
}
function plan(raw,req,nowMs){const s=readLedger(raw);if(!Number.isFinite(nowMs)||nowMs>=Date.parse(POLICY.validUntil))fail('REVALIDAR_TARIFAS');
 if(!req||!/^LIN-\d+-\d+$/.test(req.case_id)||typeof req.id!=='string'||!/^\d+$/.test(req.id))fail('CASO_INVALIDO');
 if(req.kind==='admit'){
  if(typeof req.event_id!=='string'||!/^telegram:\d+$|^manual:\d+$/.test(req.event_id))fail('EVENTO_INVALIDO');
  if(s.cases.some(c=>c.event_id===req.event_id))fail('DUPLICADO');
  if(s.cases.some(c=>c.case_id===req.case_id))fail('CASO_YA_ADMITIDO');if(s.cases.length>=POLICY.maxCases)fail('LEDGER_LLENO');
  s.cases.push({case_id:req.case_id,event_id:req.event_id,created:new Date(nowMs).toISOString(),capNano:POLICY.capNano});
 }else if(req.kind==='call'){
  const c=s.cases.find(c=>c.case_id===req.case_id);if(!c)fail('CASO_NO_ADMITIDO');
  if(nowMs-Date.parse(c.created)>=POLICY.maxSeconds*1000)fail('TIEMPO_AGOTADO');
  if(s.requests.some(r=>r.id===req.id))fail('PETICION_DUPLICADA');
  const rows=s.requests.filter(r=>r.case_id===req.case_id);if(rows.some(r=>r.state==='INCIERTO'))fail('CASO_INCIERTO');
  if(rows.length>=POLICY.maxCalls)fail('LIMITE_LLAMADAS');normalizeCall(req.body);
  if(rows.reduce((a,r)=>a+(r.actualNano??r.reservedNano),0)+quote()>c.capNano)fail('LIMITE_COSTO');
  s.requests.push({id:req.id,case_id:req.case_id,state:'RESERVADO',reservedNano:quote(),actualNano:null,model:POLICY.model,created:new Date(nowMs).toISOString()});
 }else fail('OPERACION_INVALIDA');s.seq++;return JSON.stringify(s);
}
function reconcile(raw,req,response,nowMs){const s=readLedger(raw),r=s.requests.find(r=>r.id===req.id&&r.case_id===req.case_id);if(!r||r.state!=='RESERVADO')fail('RESERVA_INVALIDA');
 const u=response?.usage;let valid=response?.model===POLICY.model&&u&&Number.isSafeInteger(u.prompt_tokens)&&u.prompt_tokens>=0&&u.prompt_tokens<=POLICY.contextTokens&&Number.isSafeInteger(u.completion_tokens)&&u.completion_tokens>=0&&u.completion_tokens<=POLICY.maxOutputTokens&&Array.isArray(response.choices)&&response.choices.length===1;
 if(valid){r.actualNano=u.prompt_tokens*POLICY.inputNanoPerToken+u.completion_tokens*POLICY.outputNanoPerToken;r.state=r.actualNano<=r.reservedNano?'CONCILIADO':'INCIERTO';r.prompt_tokens=u.prompt_tokens;r.completion_tokens=u.completion_tokens;r.provider_request_id=String(response.id??'').slice(0,120);r.costType='USAGE_X_TARIFA_ESTANDAR_NO_FACTURA';}
 else r.state='INCIERTO';r.finished=new Date(nowMs).toISOString();s.seq++;return JSON.stringify(s);
}
function responseEnvelope(response,clientStream){if(!clientStream)return {contentType:'application/json',body:JSON.stringify(response)};
 const c=response.choices[0],delta={...c.message};if(delta.tool_calls)delta.tool_calls=delta.tool_calls.map((t,i)=>({...t,index:i}));
 const chunk={id:response.id,object:'chat.completion.chunk',created:response.created,model:response.model,choices:[{index:0,delta,finish_reason:null}]};
 const end={...chunk,choices:[{index:0,delta:{},finish_reason:c.finish_reason??'stop'}]};
 return {contentType:'text/event-stream',body:'data: '+JSON.stringify(chunk)+'\n\ndata: '+JSON.stringify(end)+'\n\ndata: '+JSON.stringify({...chunk,choices:[],usage:response.usage})+'\n\ndata: [DONE]\n\n'};
}
if(typeof module!=='undefined')module.exports={POLICY,emptyLedger,readLedger,quote,normalizeCall,plan,reconcile,responseEnvelope};
