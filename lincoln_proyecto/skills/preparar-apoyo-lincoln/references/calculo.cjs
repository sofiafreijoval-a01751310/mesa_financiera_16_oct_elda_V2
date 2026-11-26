// Importes en centavos; nunca convierte strings, booleanos o no finitos a dinero.
function dinero(valor, nombre, positivo=false) {
 if(typeof valor!=='number'||!Number.isFinite(valor)||valor<0||(positivo&&valor===0)||valor>100000000||Math.abs(valor*100-Math.round(valor*100))>1e-6) throw Error(nombre+': importe inválido');
 return Math.round(valor*100);
}
function entero(valor,nombre){if(!Number.isSafeInteger(valor)||valor<0)throw Error(nombre+': entero no negativo requerido');return valor;}
function calcularPropuesta(d){
 try {
 if(!d||typeof d!=='object'||Array.isArray(d))throw Error('Entrada debe ser objeto');
 const modelos=['Corsair','Nautilus','Aviator','Navigator'];
 const inv=dinero(d.inversion_total_mxn,'inversion_total_mxn',true),asig=dinero(d.asignacion_mxn,'asignacion_mxn',true),disp=dinero(d.disponible_mxn,'disponible_mxn');
 if(disp>asig)throw Error('Saldo mayor que asignación');
 if(typeof d.tratamiento_iva!=='string'||d.tratamiento_iva.trim().toLowerCase().replaceAll('_',' ')!=='antes de iva')throw Error('Inversión debe expresarse antes de IVA');
 const ventas={};for(const m of modelos)ventas[m]=entero(d.ventas?.[m]??d.ventas?.[m.toLowerCase()],m);
 if(Object.values(ventas).reduce((a,b)=>a+b,0)<=0)throw Error('Ventas insuficientes');
 if(!Array.isArray(d.mercado)||d.mercado.length!==4)throw Error('Se requieren cuatro segmentos');
 const vistos=new Set(),mercado=d.mercado.map(x=>{
 if(!x||!modelos.includes(x.modelo)||vistos.has(x.modelo))throw Error('Segmento desconocido o duplicado');vistos.add(x.modelo);
 if(typeof x.categoria!=='string'||!x.categoria.trim())throw Error('Categoría ausente');
 entero(x.volumen_2025,'volumen_2025');
 if(typeof x.crecimiento_real_pct!=='number'||!Number.isFinite(x.crecimiento_real_pct)||x.crecimiento_real_pct< -100)throw Error('Crecimiento inválido');
 if(typeof x.penetracion_pct!=='number'||!Number.isFinite(x.penetracion_pct)||x.penetracion_pct<0||x.penetracion_pct>100)throw Error('Penetración inválida');
 return {modelo:x.modelo,categoria:x.categoria,volumen_2025:x.volumen_2025,crecimiento_real_pct:x.crecimiento_real_pct,penetracion_pct:x.penetracion_pct};
 });
 const apoyo=Math.min(Math.floor(inv/2),disp),ajuste=2*apoyo<inv,max=Math.max(...Object.values(ventas)),fortaleza=modelos.filter(m=>ventas[m]===max);
 const positivos=mercado.filter(x=>x.crecimiento_real_pct>0),crec=positivos.length?Math.max(...positivos.map(x=>x.crecimiento_real_pct)):null,op=positivos.filter(x=>x.crecimiento_real_pct===crec);
 return {ok:true,errores:[],inversion_total_mxn:inv/100,inversion_elegible_mxn:inv/100,apoyo_teorico_mxn:Math.floor(inv/2)/100,apoyo_lincoln_mxn:apoyo/100,aportacion_distribuidor_mxn:apoyo/100,asignacion_mxn:asig/100,saldo_disponible_actual_mxn:disp/100,saldo_proyectado_mxn:(disp-apoyo)/100,saldo_suficiente:disp>=Math.floor(inv/2),inversion_ajustada_mxn:ajuste?2*apoyo/100:null,requiere_aceptacion_ajuste:ajuste,fortaleza:{modelos:fortaleza,ventas_2025:max,empate:fortaleza.length>1},oportunidad:{segmentos:op,empate:op.length>1},fortaleza_y_oportunidad_coinciden:fortaleza.length===1&&op.length===1&&fortaleza[0]===op[0].modelo,estado_aprobacion:'PENDIENTE_APROBACION_HUMANA',modifica_presupuesto:false};
 }catch(e){return {ok:false,errores:[e.message]};}
}
module.exports={calcularPropuesta,dinero};
