const original=$('Inicializar caso').first().json;
const r=JSON.parse($('Validar contrato de salida').first().json.output);
const filas=nombre=>$(nombre).all().map(i=>i.json).filter(x=>x&&Object.keys(x).length);
const ventas=filas('Fuente ventas para revisión'),presupuesto=filas('Fuente presupuesto para revisión'),mercado=filas('Fuente mercado para revisión');
function bloquear(motivo){r.estado='DETENIDO';r.resultado='Resultado simulado. Propuesta detenida: '+motivo;r.advertencias=['No se aprobó ni reservó presupuesto.'];r.control_determinista={ok:false,errores:[motivo],traza:[]};return [{json:{output:JSON.stringify(r)}}];}
if(ventas.length!==1||presupuesto.length!==1||mercado.length!==4)return bloquear('Fuente ausente o duplicada.');
for(const x of [...ventas,...presupuesto,...mercado])if(x.distribuidor_id!==original.distribuidor_id||x.fuente!=='SINTETICA_ACADEMICA'||String(x.version)!=='0.1')return bloquear('Distribuidor, fuente o versión no autorizados.');
const v=ventas[0],b=presupuesto[0];
if(String(v.periodo)!=='2025'||String(b.ejercicio)!=='2026'||mercado.some(x=>String(x.periodo)!=='2025'||String(x.periodo_base)!=='2024'))return bloquear('Periodo de fuente incorrecto.');
const s=r.solicitud_validada.resultado;
let calculo;try{
 const a=dinero(b.asignacion_mxn,'asignación',true),ap=dinero(b.aprobado_mxn,'aprobado'),re=dinero(b.reservado_mxn,'reservado'),dis=dinero(b.disponible_mxn,'disponible');
 if(a-ap-re!==dis)throw Error('Saldo de fuente no reconcilia');
 const total=['corsair','nautilus','aviator','navigator'].reduce((t,k)=>t+entero(v[k],k),0);
 if(total!==entero(v.total_2025,'total_2025')||total*250000!==a)throw Error('Asignación no reconcilia ventas');
 calculo=calcularPropuesta({inversion_total_mxn:s.inversion_total,tratamiento_iva:s.tratamiento_iva,asignacion_mxn:b.asignacion_mxn,disponible_mxn:b.disponible_mxn,ventas:v,mercado});
 if(!calculo.ok)throw Error(calculo.errores.join('; '));if(calculo.apoyo_lincoln_mxn===0)throw Error('No hay saldo para un apoyo positivo');
}catch(e){return bloquear(e.message);}
const fuentes=[{herramienta:'lectura_servidor_ventas',tabla:'lincoln_ventas_2025',distribuidor_id:original.distribuidor_id,fuente:v.fuente,version:String(v.version),filas:1,periodo:'2025'},{herramienta:'lectura_servidor_presupuesto',tabla:'lincoln_presupuesto_2026',distribuidor_id:original.distribuidor_id,fuente:b.fuente,version:String(b.version),filas:1,periodo:'2026'},{herramienta:'lectura_servidor_mercado',tabla:'lincoln_mercado_pma',distribuidor_id:original.distribuidor_id,fuente:mercado[0].fuente,version:String(mercado[0].version),filas:4,periodo:'2025'}];
const traza=[],inicio=Date.now();let propuesta=r.propuesta.resultado;
for(let vuelta=1;vuelta<=3;vuelta++){
 if(Date.now()-inicio>=10000)return bloquear('Tiempo de revisión agotado');
 const errores=[];for(const [k,value]of Object.entries(calculo))if(JSON.stringify(propuesta.calculo?.[k])!==JSON.stringify(value))errores.push(k);
 if(propuesta.modifica_presupuesto!==false||propuesta.estado_aprobacion!=='PENDIENTE_APROBACION_HUMANA')return bloquear('La propuesta declara aprobación o cambio de presupuesto');
 if(propuesta.requiere_aceptacion_ajuste!==calculo.requiere_aceptacion_ajuste)errores.push('requiere_aceptacion_ajuste');
 traza.push({caso_id:original.caso_id,version_propuesta:vuelta,vuelta,ok:!errores.length,errores,
   calculo_evaluado:JSON.parse(JSON.stringify(propuesta.calculo??null)),
   requiere_aceptacion_ajuste:propuesta.requiere_aceptacion_ajuste,
   llamadas_modelo:0,costo_api_usd:0});
 if(!errores.length){
  r.propuesta.resultado=propuesta;r.fuentes=fuentes;r.control_determinista={ok:true,version:'0.4',traza,version_propuesta:traza.length,limite_revisiones:3,limite_segundos:10,duracion_ms:Date.now()-inicio,llamadas_modelo:0,costo_api_usd:0,alcance_costo:'SOLO_ESTE_NODO_DETERMINISTA; NO_INCLUYE_LLM_PREVIOS_NI_INFRAESTRUCTURA',aprobacion_humana:false,modifica_presupuesto:false};
  const importe=n=>n.toFixed(2)+' MXN';
  r.resultado='Resultado simulado. '+original.distribuidor_id+'; inversión solicitada '+importe(calculo.inversion_total_mxn)+' antes de IVA. Apoyo Lincoln '+importe(calculo.apoyo_lincoln_mxn)+' y aportación distribuidor '+importe(calculo.aportacion_distribuidor_mxn)+'. Saldo proyectado '+importe(calculo.saldo_proyectado_mxn)+'. Fortaleza: '+calculo.fortaleza.modelos.join(', ')+'. Oportunidad de crecimiento del PMA simulado: '+(calculo.oportunidad.segmentos.map(x=>x.modelo).join(', ')||'sin crecimiento positivo')+'. Fuentes sintéticas v0.1. '+(calculo.requiere_aceptacion_ajuste?'Alcance reducido a '+importe(2*calculo.apoyo_lincoln_mxn)+': requiere ACEPTAR_AJUSTE al aprobar.':'Pendiente de decisión humana.')+' No se reserva presupuesto.';
  return [{json:{output:JSON.stringify(r)}}];
 }
 if(vuelta===3)return bloquear('No convergió la revisión');
 propuesta={...propuesta,calculo:JSON.parse(JSON.stringify(calculo)),requiere_aceptacion_ajuste:calculo.requiere_aceptacion_ajuste};
}
return bloquear('Revisión incompleta');
