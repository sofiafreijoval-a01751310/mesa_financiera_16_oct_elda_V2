function conservarSalidas(r,steps,caso){
 if(!r||r.estado!=='PENDIENTE_APROBACION')return r;
 if(!Array.isArray(steps)||steps.length>12)throw Error('Traza de herramientas ausente');
 const roles=[['solicitud_validada','agente_1_solicitud','VALIDADO'],['datos_verificados','agente_2_datos','DATOS_VERIFICADOS'],['propuesta','agente_3_propuesta','PROPUESTA_GENERADA'],['revision','agente_4_revision','APROBAR_REVISION']];
 function decode(value){for(let i=0;i<5;i++){if(typeof value==='string'){value=JSON.parse(value);continue;}if(Array.isArray(value)&&value.length===1){value=value[0];continue;}if(value&&typeof value==='object'&&Object.hasOwn(value,'output')){value=value.output;continue;}return value;}throw Error('Observacion invalida');}
 const out={...r};let previous=-1;
 for(const [field,tool,state]of roles){let index=-1;for(let i=0;i<steps.length;i++)if(steps[i]?.action?.tool===tool)index=i;
  if(index<=previous)throw Error('Secuencia de herramientas incompleta');
  const b=decode(steps[index].observation);
  if(!b||b.caso_id!==caso||b.agente!==tool||b.estado!==state||!b.resultado||typeof b.resultado!=='object'||Array.isArray(b.resultado))throw Error('Salida de herramienta invalida');
  out[field]=b;previous=index;
 }
 out.transferencia_verificada='SALIDAS_HERRAMIENTAS_MISMO_CASO';return out;
}
