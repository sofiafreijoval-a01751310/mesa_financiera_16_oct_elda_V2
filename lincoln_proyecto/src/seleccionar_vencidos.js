function seleccionarVencidos(rows,ahora=Date.now()){
 if(!Number.isFinite(ahora))throw Error('Reloj inválido');
 return rows.flatMap(r=>{
  if(!Number.isInteger(r.id)||r.estado!=='PENDIENTE_APROBACION'||r.decision_id||!/^LIN-\d+-\d+$/.test(r.caso_id)||!/^\d+$/.test(String(r.version_propuesta)))return [];
  const vence=Date.parse(r.vence_en);if(!Number.isFinite(vence)||vence>ahora)return [];
  let p;try{p=JSON.parse(r.propuesta_json);}catch{return [];}
  if(p.caso_original?.modo!=='SIMULADO'||p.caso_original?.caso_id!==r.caso_id||p.resultado?.caso_id!==r.caso_id||p.aprobacion_humana===true||p.modifica_presupuesto!==false)return [];
  const decision_id='VENCIMIENTO:'+r.caso_id+':'+r.version_propuesta;
  p.vencimiento={decision_id,fecha:new Date(ahora).toISOString(),estado:'VENCIDO',modifica_presupuesto:false,aprobacion_humana:false};
  p.resultado.estado='VENCIDO';
  return [{...r,estado:'VENCIDO',decision_id,propuesta_original:r.propuesta_json,propuesta_json:JSON.stringify(p)}];
 });
}
return seleccionarVencidos($input.all().map(i=>i.json)).map(json=>({json}));
