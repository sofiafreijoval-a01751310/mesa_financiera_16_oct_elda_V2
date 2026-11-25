const original=$('Inicializar caso').first().json;
return $input.all().map((item,index)=>{
 let r;try{r=typeof item.json.output==='string'?JSON.parse(item.json.output):item.json.output;}catch{throw Error('Respuesta no es JSON válido');}
 if(!r||typeof r!=='object'||Array.isArray(r)||r.caso_id!==original.caso_id||r.agente!=='orquestador'||!['PENDIENTE_APROBACION','REQUIERE_ACLARACION','DETENIDO'].includes(r.estado))throw Error('Contrato de salida inválido');
 if(typeof r.resultado!=='string'||r.resultado.length>3000)throw Error('Resumen inválido');
 if(r.estado==='PENDIENTE_APROBACION'){
  const bloques=[['solicitud_validada','agente_1_solicitud','VALIDADO'],['datos_verificados','agente_2_datos','DATOS_VERIFICADOS'],['propuesta','agente_3_propuesta','PROPUESTA_GENERADA'],['revision','agente_4_revision','APROBAR_REVISION']];
  for(const [campo,agente,estado]of bloques){const b=r[campo];if(!b||b.caso_id!==original.caso_id||b.agente!==agente||b.estado!==estado||!b.resultado||typeof b.resultado!=='object')throw Error('Falta bloque íntegro '+campo);}
  const s=r.solicitud_validada.resultado;
  if(s.distribuidor_id!==original.distribuidor_id||!/^D(0[1-9]|1[0-9])$/.test(s.distribuidor_id))throw Error('Distribuidor inconsistente');
  if(!Array.isArray(s.campos_faltantes)||s.campos_faltantes.length||!Array.isArray(s.preguntas)||s.preguntas.length)throw Error('Solicitud incompleta');
  if(s.moneda!=='MXN'||typeof s.tipo_evento!=='string'||!s.tipo_evento.trim()||typeof s.objetivo_comercial!=='string'||!s.objetivo_comercial.trim())throw Error('Falta moneda/formato/objetivo');
  if(!/^\d{4}-\d{2}-\d{2}$/.test(s.fecha_evento)||!Number.isFinite(Date.parse(s.fecha_evento+'T12:00:00Z'))||new Date(s.fecha_evento+'T12:00:00Z').toISOString().slice(0,10)!==s.fecha_evento)throw Error('Fecha inválida');
  if(!['Corsair','Nautilus','Aviator','Navigator'].includes(s.nameplate_solicitado)||!Number.isSafeInteger(s.asistentes)||s.asistentes<=0)throw Error('Modelo/asistentes inválidos');
  if(!Number.isInteger(s.edad_min)||!Number.isInteger(s.edad_max)||s.edad_min<35||s.edad_max>60||s.edad_min>s.edad_max||!Array.isArray(s.nse)||!s.nse.length)throw Error('Audiencia fuera del ejercicio');
  if(s.nse.some(x=>typeof x!=='string'||!x.split('/').every(y=>['A','A+','B+'].includes(y.trim()))))throw Error('NSE fuera del ejercicio');
 }
 return {json:{output:JSON.stringify(r),requiere_revision:r.estado==='PENDIENTE_APROBACION'},pairedItem:{item:index}};
});
