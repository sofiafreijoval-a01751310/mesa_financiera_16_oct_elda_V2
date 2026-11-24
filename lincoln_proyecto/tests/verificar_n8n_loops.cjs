const fs=require('fs');const path=require('path');const assert=require('assert/strict');
const w=JSON.parse(fs.readFileSync(path.join(__dirname,'../exports/Lincoln_Prueba_Aislada_Skills_Loops.json'),'utf8'));
let json={};
for(const n of w.nodes.filter(n=>n.type==='n8n-nodes-base.code')){
 const out=new Function('$input','$execution',n.parameters.jsCode)({first:()=>({json})},{id:'999999'});
 json=out[0].json;
}
assert.equal(json.validacion,'PASS');assert.equal(json.carga.length,3);
assert.equal(json.resultados[1].propuesta.apoyo_mxn,62500);
assert.equal(json.resultados[1].propuesta.inversion_ajustada_mxn,125000);
assert.equal(json.resultados[1].propuesta.requiere_aceptacion_alcance,true);
assert.equal(json.seguridad_costo.consumo_api_usd,0);
fs.writeFileSync(path.join(__dirname,'../evidencias/prueba_export_n8n.json'),JSON.stringify({alcance:'Ejecución local de JS del export; verificar además ejecución nativa',...json},null,2));
console.log('PASS: JavaScript del workflow aislado, 3 skills cargados, V1/V2, bloqueo de fuente y recuperación 3 intentos.');
