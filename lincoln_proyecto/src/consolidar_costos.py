"""Consolida uso observado; no inventa etapas, facturas, caché ni costos desconocidos."""
import csv
from pathlib import Path
from decimal import Decimal
R=Path(__file__).resolve().parents[1]
fields=['fecha_hora','caso_id','llamada_id','etapa','agente','proveedor','modelo_version','tokens_entrada','tokens_salida','tokens_cache','duracion_voz_seg','unidad_cobro','tarifa_entrada_usd_millon','tarifa_salida_usd_millon','costo_usd','moneda','estado_llamada','resultado_caso','reintento','origen','referencia','nota']
rows=[]
result={'LIN-87-1':'DETENIDO_FORMATO','LIN-92-1':'DETENIDO_FORMATO','LIN-97-1':'DETENIDO_ESQUEMA','LIN-110-1':'DETENIDO_CONTRATO','LIN-123-1':'PENDIENTE_APROBACION'}
for r in csv.DictReader((R/'costos/consumo_proxy_27nov.csv').open()):
 rows.append(dict(fecha_hora=r['creada_utc'],caso_id=r['caso_id'],llamada_id=r['peticion_n8n'],etapa='LLM_NO_ATRIBUIDA',agente='NO_ATRIBUIDO_POR_LEDGER',proveedor='OpenAI',modelo_version=r['modelo'],tokens_entrada=r['prompt_tokens'],tokens_salida=r['completion_tokens'],tokens_cache='DESCONOCIDO_SIN_DESCUENTO',duracion_voz_seg='NO_APLICA',unidad_cobro='tokens',tarifa_entrada_usd_millon='0.15',tarifa_salida_usd_millon='0.60',costo_usd=r['costo_usd_tarifa_estandar'],moneda='USD',estado_llamada=r['estado'],resultado_caso=result.get(r['caso_id'],'DIAGNOSTICO'),reintento='0_AUTOMATICO',origen='USAGE_MEDIDO_X_TARIFA_ESTANDAR_NO_FACTURA',referencia='consumo_proxy_27nov.csv',nota='La etapa/agente no constan en ledger; no inferidos. Excluye fixtures de reservas sintéticas y plataformas.'))
for r in csv.DictReader((R/'costos/voz_observada_26nov.csv').open()):
 common=dict(fecha_hora=r['fecha_local'],caso_id=r['caso_id'],llamada_id='VOZ_V5_26NOV',etapa='VOZ',agente='Interfaz ElevenLabs',proveedor='ElevenLabs',modelo_version=r['modelo'],tokens_entrada='DESCONOCIDO',tokens_salida='DESCONOCIDO',tokens_cache='DESCONOCIDO',duracion_voz_seg=r['duracion_segundos'],moneda='USD',estado_llamada='CONSULTA_EXITOSA',resultado_caso='LECTURA_APROBADO_SIMULADO',reintento='DESCONOCIDO',origen='PANEL_PROVEEDOR_NO_FACTURA',referencia='voz_observada_26nov.csv')
 rows.append({**common,'unidad_cobro':'subtotal_LLM_panel','costo_usd':r['llm_usd_mostrado'],'nota':'Subtotal LLM mostrado para4turnos. No sumar a conversión del total630créditos sin conciliar inclusión.'})
 rows.append({**common,'llamada_id':'VOZ_V5_26NOV_PLATAFORMA','modelo_version':'plataforma','unidad_cobro':'511_creditos_plataforma','costo_usd':'DESCONOCIDO','nota':'Total630créditos incluye511plataforma+119LLM. Sin conversión monetaria inventada.'})
for stage in ['DESARROLLO_CHATGPT_CODEX','N8N_CLOUD','GITHUB_ACTIONS_PAGES']:
 rows.append(dict(fecha_hora='2026-11-27_CORTE',caso_id='INVERSION_DESARROLLO_O_PLATAFORMA',llamada_id='NO_DISPONIBLE',etapa=stage,agente='NO_APLICA',proveedor=stage,modelo_version='NO_APLICA_O_NO_REGISTRADO',tokens_entrada='NO_APLICA_O_DESCONOCIDO',tokens_salida='NO_APLICA_O_DESCONOCIDO',unidad_cobro='plan_o_uso_no_conciliado',costo_usd='DESCONOCIDO',moneda='USD',estado_llamada='SIN_FACTURA_CONCILIADA',reintento='NO_APLICA',origen='DESCONOCIDO',referencia='../docs/costos.md',nota='No reportar cero; separar gasto de desarrollo, plataforma y operación.'))
with (R/'costos/costos.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
summary=[]
for case in sorted(set(r['caso_id']for r in rows if r['proveedor']=='OpenAI')):
 rr=[r for r in rows if r['caso_id']==case and r['proveedor']=='OpenAI'];summary.append(dict(caso_id=case,llamadas=len(rr),tokens_entrada=sum(int(r['tokens_entrada'])for r in rr),tokens_salida=sum(int(r['tokens_salida'])for r in rr),usd_tarifa_estandar=str(sum(Decimal(r['costo_usd'])for r in rr)),resultado=result.get(case,'DIAGNOSTICO'),alcance='LLM_SOLAMENTE_NO_FACTURA'))
for case in ['LIN-56-1','LIN-69-1','LIN-72-1','LIN-140-1']:
 summary.append(dict(caso_id=case,llamadas='DESCONOCIDO_EN_ESTE_CSV',tokens_entrada='DESCONOCIDO',tokens_salida='DESCONOCIDO',usd_tarifa_estandar='DESCONOCIDO',resultado='EVALUACION_REVISADA',alcance='TRAZA_EXISTENTE; NO_INVENTAR_USAGE_NI_FACTURA'))
with (R/'costos/resumen_por_caso.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
print({'filas_costos':len(rows),'casos_resumen':len(summary),'etapas_no_atribuidas':'explícitas','no_invoca_apis':True})
