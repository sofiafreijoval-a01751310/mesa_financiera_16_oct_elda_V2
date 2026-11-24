"""Casos sintéticos: ejecuta instrucciones del skill y conserva trazas verificables."""
import hashlib
import importlib.util
import json
from pathlib import Path
from guardianes import Guardianes
from loop_servicio import recuperar
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/revisar-apoyo-lincoln'
spec=importlib.util.spec_from_file_location('revisor',SKILL/'scripts/revisar.py')
reviewer=importlib.util.module_from_spec(spec);spec.loader.exec_module(reviewer)

def main():
    out=ROOT/'evidencias';out.mkdir(exist_ok=True)
    base=json.loads((ROOT/'datos/base_proyecto.json').read_text())
    registry={d['distribuidor_id']:d for d in base['distribuidores']}
    scenarios=[('LIN-101-1','D01','400000',False),('LIN-102-1','D03','400000',False),
               ('LIN-103-1','D08','500000',False),('LIN-104-1','D01','400000',True)]
    summary=[]
    manifest={'skill':'revisar-apoyo-lincoln','version':'1.0.1','loaded_from':'skills/revisar-apoyo-lincoln/SKILL.md',
              'sha256':hashlib.sha256((SKILL/'SKILL.md').read_bytes()).hexdigest(),
              'execution':'local determinista; no integración viva n8n'}
    # Cargar instrucciones reales antes de ejecutar su recurso; no basta mencionar su nombre.
    instructions=(SKILL/'SKILL.md').read_text()
    assert instructions.startswith('---') and 'scripts/revisar.py' in instructions
    for case_id,dealer,investment,invalid in scenarios:
        data=registry[dealer]
        case={'caso_id':case_id,'modo':'SIMULADO','inversion_mxn':investment,
              'datos_verificados':{'caso_id':case_id,'distribuidor_id':dealer,'fuente':'base_proyecto',
                  'version':'' if invalid else base['version'],'saldo_mxn':str(data['disponible_mxn'])},'propuesta':{}}
        (ROOT/'fixtures'/f'{case_id}.json').write_text(json.dumps(case,ensure_ascii=False,indent=2))
        result=reviewer.run_loop(case)
        (out/f'{case_id}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
        (out/f'{case_id}.jsonl').write_text(''.join(json.dumps(t,ensure_ascii=False)+'\n' for t in result['traza']))
        summary.append({'caso_id':case_id,'distribuidor':data['nombre'],'estado_loop':result['estado_loop'],
                        'revisiones':len(result['traza']),'costo_api_usd':'0','integral_n8n':False})
    # Loop 2: errores de transporte controlados. Sin llamadas a red reales.
    ledger=out/'demo_ledger.sqlite'
    if ledger.exists():ledger.unlink()
    guard=Guardianes(ledger);attempts=[];trace=[]
    def query():
        attempts.append(1)
        if len(attempts)<3:raise TimeoutError('Fallo transitorio simulado')
        return {'caso_id':'LIN-201-1','estado':'PENDIENTE_APROBACION'}
    result=recuperar(query,guard,'LIN-201-1','DEMO','demo-201',trace,allowed_user='DEMO')
    (out/'loop_recuperacion.json').write_text(json.dumps({'simulacion_fallos':True,'resultado':result,'traza':trace},indent=2))
    # Reservas conservadoras; cero gasto API local comprobado por ejecución sin clientes.
    for i in range(1,4):guard.reconcile(f'demo-201:{i}','0')
    (out/'skills_ejecutados.json').write_text(json.dumps({'reviewer':manifest,'casos':summary},ensure_ascii=False,indent=2))
    print(json.dumps({'casos':summary,'loop_recuperacion':result['estado'],'intentos':len(trace)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
