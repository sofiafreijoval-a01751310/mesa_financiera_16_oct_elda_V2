#!/usr/bin/env python3
import json,sys
from decimal import Decimal
D=Decimal

def nonnegative(x,name):
    n=D(str(x))
    if not n.is_finite() or n<0: raise ValueError(name+' debe ser finito y no negativo')
    return n

def main(p):
    scenarios=p['scenarios']; models=p['models']; base=p['baseline']
    if not scenarios or not models: raise ValueError('Faltan escenarios o modelos')
    fx=nonnegative(p['fx'],'fx')
    if fx==0 or not p['fx_source'] or not p['fx_date']: raise ValueError('Falta tasa/fuente/fecha')
    out=[]
    for s in scenarios:
        ti=nonnegative(s['input_tokens'],'input_tokens');to=nonnegative(s['output_tokens'],'output_tokens')
        if ti!=ti.to_integral_value() or to!=to.to_integral_value():raise ValueError('Tokens deben ser enteros')
        rows=[]
        for m in models:
            if not m['source'] or not m['verified_at']:raise ValueError('Falta fuente/fecha de tarifa')
            pin=nonnegative(m['input_usd_m'],'input_usd_m');pout=nonnegative(m['output_usd_m'],'output_usd_m');fixed=nonnegative(m['fixed_usd_call'],'fixed_usd_call')
            ci=ti*pin/D(1000000);co=to*pout/D(1000000);c=ci+co+fixed
            rows.append({'model':m['name'],'input_usd':ci,'output_usd':co,'fixed_usd':fixed,'usd_call':c,'input_share_pct':ci/c*100 if c else None,'output_share_pct':co/c*100 if c else None,'scales_usd':{str(n):c*n for n in (1000,10000,1000000)},'scales_currency':{str(n):c*n*fx for n in (1000,10000,1000000)}})
        b=next(r['usd_call'] for r in rows if r['model']==base)
        for r in rows:r.update(delta_usd=r['usd_call']-b,delta_pct=(r['usd_call']-b)/b*100 if b else None)
        out.append({'scenario':s['name'],'rows':rows})
    return {'currency':p['currency'],'fx':fx,'fx_source':p['fx_source'],'fx_date':p['fx_date'],'baseline':base,'results':out}
if __name__=='__main__':
    try: print(json.dumps(main(json.load(sys.stdin)),default=str,ensure_ascii=False,indent=2))
    except (KeyError,ValueError,TypeError,StopIteration,ArithmeticError) as e:
        print('Cálculo detenido: faltan datos o son inválidos: '+str(e),file=sys.stderr);sys.exit(2)
