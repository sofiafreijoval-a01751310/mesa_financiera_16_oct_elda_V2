const assert=require('node:assert/strict'),fs=require('node:fs');
const source=fs.readFileSync(require('node:path').join(__dirname,'../src/n8n_v07/admission.js'),'utf8');
const admission=new Function('$input','$',source);
const original={caso_id:'LIN-900001-1',canal:'telegram',autorizado:true,chat_id:'SINTETICO'};
function run(response){return admission({first:()=>({json:response})},()=>({first:()=>({json:original})}))[0].json;}
let tests=0;function test(name,fn){fn();tests++;}
test('Solo admisión positiva del mismo folio permite modelos',()=>{
 assert.equal(run({statusCode:200,body:{ok:true,admitido:true,caso_id:original.caso_id}}).control_admitido,true);
});
for(const response of [{statusCode:409,body:{ok:false}}, {error:'API key SECRETO_NO_DIVULGAR'},
 {statusCode:200,body:{ok:true,admitido:true,caso_id:'LIN-900002-1'}},
 {statusCode:200,body:{ok:true,admitido:'true',caso_id:original.caso_id}}]){
 test('Fallo, duplicado o respuesta ambigua bloquean sin divulgar errores',()=>{
   const r=run(response);assert.equal(r.control_admitido,false);
   assert.equal(JSON.stringify(r).includes('SECRETO_NO_DIVULGAR'),false);
 });
}
const w=require('../exports/Lincoln_Apoyos_v07_CANDIDATO_PUBLICO.json');
test('Una denegación no tiene camino al modelo ni al registro de caso',()=>{
 const reachable=new Set(),stack=[w.connections['¿Caso admitido?'].main[1][0].node];
 while(stack.length){const n=stack.pop();if(reachable.has(n))continue;reachable.add(n);
  for(const edges of Object.values(w.connections[n]??{}))for(const group of edges)for(const e of group)stack.push(e.node);
 }
 assert(!reachable.has('Orquestador Lincoln'));assert(!reachable.has('Guardar caso Lincoln'));
});
test('Los cinco roles tienen el modelo único y cero reintentos automáticos',()=>{
 const models=w.nodes.filter(n=>n.type.endsWith('.lmChatOpenAi'));assert.equal(models.length,5);
 for(const n of models){assert.equal(n.parameters.model.value,'gpt-4o-mini-2024-07-18');assert.equal(n.parameters.options.maxRetries,0);assert(!n.credentials);}
});
test('Fallo del modelo devuelve DETENIDO sin propagar información interna',()=>{
 const n=w.nodes.find(n=>n.name==='Validar contrato de salida');
 const validate=new Function('$input','$',n.parameters.jsCode);
 const out=validate({all:()=>[{json:{error:'SECRETO_NO_DIVULGAR'}}]},()=>({first:()=>({json:original})}));
 const r=JSON.parse(out[0].json.output);assert.equal(r.estado,'DETENIDO');assert.equal(r.caso_id,original.caso_id);
 assert(!JSON.stringify(r).includes('SECRETO_NO_DIVULGAR'));assert.equal(out[0].json.requiere_revision,false);
});
test('El candidato se conserva inactivo y sin datos fijados',()=>{assert.equal(w.active,false);assert.deepEqual(w.pinData,{});});
console.log('PASS: '+tests+' pruebas del adaptador; no equivalen a integración viva.');
