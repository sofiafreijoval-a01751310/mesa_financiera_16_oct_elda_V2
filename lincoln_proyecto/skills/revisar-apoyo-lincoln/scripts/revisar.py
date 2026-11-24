#!/usr/bin/env python3
"""Revisión determinista sin red ni llamadas a modelos."""
import argparse
import copy
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def money(value):
    if isinstance(value, bool):
        raise ValueError('Monto booleano')
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError('Monto no numérico')
    if not result.is_finite() or result < 0 or result != result.quantize(Decimal('.01')):
        raise ValueError('Monto debe ser finito, no negativo y con máximo dos decimales')
    return result

def expected(case):
    if not isinstance(case,dict): raise ValueError('Caso debe ser objeto JSON')
    if not re.fullmatch(r'LIN-\d+-\d+', str(case.get('caso_id', ''))):
        raise ValueError('Folio inválido')
    if case.get('modo') != 'SIMULADO':
        raise ValueError('Solo simulación')
    if not isinstance(case.get('propuesta'),dict): raise ValueError('Propuesta debe ser objeto JSON')
    data = case['datos_verificados']
    if not isinstance(data,dict): raise ValueError('Datos verificados deben ser objeto JSON')
    if data['caso_id'] != case['caso_id'] or not all(isinstance(data.get(k),str) and data[k].strip() for k in ('fuente','version')):
        raise ValueError('Fuente/versión/folio insuficiente')
    if not re.fullmatch(r'D(0[1-9]|1[0-9])', str(data.get('distribuidor_id',''))):
        raise ValueError('Distribuidor inválido')
    inv, balance = money(case['inversion_mxn']), money(data['saldo_mxn'])
    if inv <= 0:
        raise ValueError('Inversión debe ser positiva')
    support = min((inv/2).quantize(Decimal('.01'),rounding=ROUND_DOWN),balance)
    return {'caso_id':case['caso_id'],'apoyo_mxn':str(support),
            'aportacion_mxn':str(support),'inversion_ajustada_mxn':str(2*support),
            'saldo_proyectado_mxn':str(balance-support),
            'requiere_aceptacion_alcance':2*support<inv,
            'estado':'PENDIENTE_APROBACION','modifica_presupuesto':False}

def review(case):
    errors=[]
    desired=None
    try:
        desired=expected(case)
        proposal=case.get('propuesta',{})
        for key,value in desired.items():
            if key.endswith('_mxn'):
                if money(proposal.get(key))!=money(value): errors.append(key)
            elif type(proposal.get(key)) is not type(value) or proposal.get(key)!=value:
                errors.append(key)
    except (KeyError,TypeError,ValueError,InvalidOperation) as exc:
        errors.append('ENTRADA: '+str(exc))
    return {'ok':not errors,'errores':errors,'esperado':desired,
            'skill':'revisar-apoyo-lincoln','version_skill':'1.0.1',
            'skill_sha256':hashlib.sha256((ROOT/'SKILL.md').read_bytes()).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'contrato_sha256':hashlib.sha256((ROOT/'references/contrato.json').read_bytes()).hexdigest()}

def run_loop(case,max_iterations=3,seconds=10):
    if not isinstance(max_iterations,int) or isinstance(max_iterations,bool) or not 1<=max_iterations<=3:
        raise ValueError('Máximo tres revisiones')
    if not 0<seconds<=10: raise ValueError('Tiempo máximo diez segundos')
    current=copy.deepcopy(case)
    start=time.monotonic()
    trace=[]
    for iteration in range(1,max_iterations+1):
        if time.monotonic()-start>=seconds: break
        verdict=review(current)
        trace.append({'fecha_utc':datetime.now(timezone.utc).isoformat(),
            'caso_id':current.get('caso_id'),'iteracion':iteration,
            'version_propuesta_local':iteration,'dictamen':verdict,
            'propuesta':copy.deepcopy(current.get('propuesta')),
            'llamadas_modelo':0,'costo_api_usd':'0'})
        if verdict['ok'] or verdict['esperado'] is None: break
        if iteration<max_iterations: current.setdefault('propuesta',{}).update(copy.deepcopy(verdict['esperado']))
    return {'ok':bool(trace and trace[-1]['dictamen']['ok']),
            'estado_loop':'CONVERGIO' if trace and trace[-1]['dictamen']['ok'] else 'ESCALAR',
            'caso':current,'traza':trace}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('case',type=Path)
    parser.add_argument('--loop',action='store_true')
    parser.add_argument('--trace',type=Path)
    args=parser.parse_args()
    try:
        case=json.loads(args.case.read_text(),parse_constant=lambda x:(_ for _ in ()).throw(ValueError('JSON no finito')))
        result=run_loop(case) if args.loop else review(case)
        if args.trace: args.trace.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in result.get('traza',[])))
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['ok'] else 2
    except (ValueError,TypeError,OSError) as exc:
        print(json.dumps({'ok':False,'error':str(exc)}))
        return 2
if __name__=='__main__': raise SystemExit(main())
