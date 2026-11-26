'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {calcularPropuesta,dinero}=require('../references/calculo.cjs');
const skillText=fs.readFileSync(path.join(__dirname,'../SKILL.md'),'utf8');
const metadata={nombre:'preparar-apoyo-lincoln',version:'1.0.0',sha256:crypto.createHash('sha256').update(skillText).digest('hex')};
function preparar(c){
 const start=Date.now(),folio=typeof c?.caso_id==='string'?c.caso_id:null;
 const output={caso_id:folio,agente:'agente_3_propuesta',estado:'DETENIDO',resultado:{},fuentes:[],advertencias:['Resultado simulado. Sin aprobación ni reserva de presupuesto.'],duracion_ms:0,consumo_ref:folio?'LOCAL_SIN_LLM:'+folio:null,skills_cargados:[{...metadata}]};
 try{
  const object=x=>x&&typeof x==='object'&&!Array.isArray(x);
  if(!object(c)||!/^LIN-\d+-\d+$/.test(folio)||c.modo!=='SIMULADO')throw Error('Caso o modo inválido');
  const a=c.solicitud_validada,b=c.datos_verificados;
  if(!object(a)||!object(b)||a.caso_id!==folio||b.caso_id!==folio||a.agente!=='agente_1_solicitud'||b.agente!=='agente_2_datos'||a.estado!=='VALIDADO'||b.estado!=='DATOS_VERIFICADOS')throw Error('Bloques incompletos o folio inconsistente');
  const s=a.resultado,d=b.resultado;
  if(!object(s)||!object(d)||!/^D(0[1-9]|1[0-9])$/.test(s.distribuidor_id)||s.distribuidor_id!==d.distribuidor_id)throw Error('Distribuidor inconsistente');
  if(s.moneda!=='MXN'||typeof s.tipo_evento!=='string'||!s.tipo_evento.trim()||typeof s.objetivo_comercial!=='string'||!s.objetivo_comercial.trim()||!Array.isArray(s.campos_faltantes)||s.campos_faltantes.length||!Array.isArray(s.preguntas)||s.preguntas.length)throw Error('Solicitud incompleta');
  if(!['Corsair','Nautilus','Aviator','Navigator'].includes(s.nameplate_solicitado)||!Number.isSafeInteger(s.asistentes)||s.asistentes<=0||!Number.isInteger(s.edad_min)||!Number.isInteger(s.edad_max)||s.edad_min<35||s.edad_max>60||s.edad_min>s.edad_max)throw Error('Audiencia o modelo fuera del ejercicio');
  if(!Array.isArray(s.nse)||!s.nse.length||s.nse.some(x=>typeof x!=='string'||!x.split('/').every(y=>['A','A+','B+'].includes(y.trim()))))throw Error('NSE inválido');
  if(typeof s.fecha_evento!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(s.fecha_evento)||!Number.isFinite(Date.parse(s.fecha_evento+'T12:00:00Z'))||new Date(s.fecha_evento+'T12:00:00Z').toISOString().slice(0,10)!==s.fecha_evento)throw Error('Fecha inválida');
  if(!Array.isArray(b.fuentes)||b.fuentes.length!==3||['consultar_ventas','consultar_presupuesto','consultar_mercado'].some(t=>b.fuentes.filter(f=>f.herramienta===t&&f.distribuidor_id===s.distribuidor_id&&f.fuente==='SINTETICA_ACADEMICA'&&f.version==='0.1').length!==1))throw Error('Fuentes autorizadas incompletas o sin versión');
  const v=d.ventas_2025_por_nameplate,p=d.presupuesto_2026;
  const suma=['corsair','nautilus','aviator','navigator'].reduce((n,k)=>n+v?.[k],0);
  if(!Number.isSafeInteger(v?.total_2025)||v.total_2025!==suma||suma<=0||suma>2000)throw Error('Total de ventas incoherente');
  const asig=dinero(p?.asignacion_mxn,'asignación',true),saldo=dinero(p?.disponible_mxn,'saldo'),aprobado=dinero(p?.aprobado_mxn,'aprobado'),reservado=dinero(p?.reservado_mxn,'reservado');
  if(asig!==suma*250000||asig-aprobado-reservado!==saldo)throw Error('Presupuesto no reconcilia con fuente');
  const calculo=calcularPropuesta({inversion_total_mxn:s.inversion_total,tratamiento_iva:s.tratamiento_iva,asignacion_mxn:p.asignacion_mxn,disponible_mxn:p.disponible_mxn,ventas:v,mercado:d.mercado_pma});
  if(!calculo.ok)throw Error(calculo.errores.join('; '));
  output.estado='PROPUESTA_GENERADA';output.resultado={calculo,requiere_aceptacion_ajuste:calculo.requiere_aceptacion_ajuste,estado_aprobacion:'PENDIENTE_APROBACION_HUMANA',modifica_presupuesto:false};output.fuentes=structuredClone(b.fuentes);
 }catch(e){output.resultado={errores:[e.message]};}
 output.duracion_ms=Date.now()-start;return output;
}
module.exports={preparar,metadata};
if(require.main===module){try{const r=preparar(JSON.parse(fs.readFileSync(process.argv[2],'utf8')));console.log(JSON.stringify(r,null,2));if(r.estado==='DETENIDO')process.exitCode=2;}catch(e){console.error('Entrada JSON inválida: '+e.message);process.exitCode=2;}}
