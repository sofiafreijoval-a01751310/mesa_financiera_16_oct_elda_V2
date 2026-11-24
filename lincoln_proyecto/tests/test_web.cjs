const assert=require('assert/strict');const fs=require('fs');const path=require('path');const app=require('../web/app.js');
const d=JSON.parse(fs.readFileSync(path.join(__dirname,'../web/data/panel.json'),'utf8'));const cases=d.casos;
const checks=[];function test(name,f){f();checks.push(name);}
test('KPI reconciliados con dos casos de negocio',()=>{const k=app.metrics(cases,d.presupuesto_nacional_mxn);assert.equal(k.approved,200000);assert.equal(k.share,.04);assert.equal(k.rate,.5);assert.equal(k.timeN,2);assert(Math.abs(k.minutes-20.973)<.01);});
test('Fixture de vencimiento no afecta KPI',()=>assert.deepEqual(app.metrics(cases,5000000),app.metrics(cases.filter(x=>!x.fixture),5000000)));
test('Vacío no se presenta como cero',()=>{const k=app.metrics([],5000000);assert.equal(k.approved,null);assert.equal(k.minutes,null);assert.equal(k.rate,null);});
test('Filtro de estado conserva denominador correcto',()=>{const r=app.filterRows(cases,{state:'RECHAZADO'});assert.equal(r.length,1);assert.equal(app.metrics(r,5000000).rate,0);});
test('Búsqueda no inventa registros',()=>assert.equal(app.filterRows(cases,{folio:'NO-EXISTE'}).length,0));
test('Consulta de folio ignora mayúsculas',()=>assert.equal(app.filterRows(cases,{folio:'lin-34-1'}).length,1));
test('Caso completo de simulador',()=>assert.deepEqual(app.support(400000,650000),{amount:200000,dealer:200000,total:400000,balance:450000,adjust:false}));
test('Saldo insuficiente exige reducción de alcance',()=>assert.deepEqual(app.support(400000,62500),{amount:62500,dealer:62500,total:125000,balance:0,adjust:true}));
test('Simulador rechaza no finitos, negativos, booleanos y milésimas',()=>{for(const x of [Infinity,NaN,-1,0,true,.001])assert.throws(()=>app.support(x,650000));assert.throws(()=>app.support(400000,1.001));});
test('Centavo impar no rompe 50/50',()=>assert.equal(app.support(.01,100).total,0));
test('Estado desactualizado es explícito',()=>assert.equal(app.dataState({...d,exportado_utc:'2026-01-01T00:00:00Z'},Date.parse('2026-11-24T00:00:00Z')),'stale'));
test('Estado sin datos y error de esquema',()=>{assert.equal(app.dataState({...d,casos:[]},Date.parse(d.exportado_utc)+1),'empty');assert.throws(()=>app.dataState({schema_version:99}));});
fs.writeFileSync(path.join(__dirname,'../evidencias/web_pruebas.json'),JSON.stringify({alcance:'Pruebas de funciones y estados web; completar QA visual de navegador',total:checks.length,passed:checks.length,checks},null,2));console.log('PASS: '+checks.length+' pruebas web.');
