import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]
b=json.loads((p/'datos/base_proyecto.json').read_text())
m=json.loads((p/'datos/mercado_pma.json').read_text())
r=b['distribuidores']
assert len(r)==19 and len({d['distribuidor_id'] for d in r})==19
assert sum(d['ventas_2025'] for d in r)==2000
assert sum(d['asignacion_mxn'] for d in r)==5000000
assert max(r,key=lambda d:d['ventas_2025'])['nombre']=='Lincoln Monterrey'
assert min(r,key=lambda d:d['ventas_2025'])['nombre']=='Lincoln Chiapas'
for d in r:
 assert sum(d['ventas_por_nameplate'].values())==d['ventas_2025']
 assert d['asignacion_mxn']==d['ventas_2025']*2500
 assert d['disponible_mxn']==d['asignacion_mxn']-d['aprobado_mxn']-d['reservado_mxn']
 assert len([v for v in m if v['distribuidor_id']==d['distribuidor_id']])==4
for v in m:
 d=next(d for d in r if d['distribuidor_id']==v['distribuidor_id'])
 assert v['ventas_lincoln_2025']==d['ventas_por_nameplate'][v['nameplate_referencia']]
 assert v['unidades_segmento_2025']>=v['ventas_lincoln_2025']
 assert abs(v['crecimiento_pct']-(v['unidades_segmento_2025']/v['unidades_segmento_2024']-1)*100)<0.0001
print('APROBADO: 19 distribuidores, 2000 unidades, MXN 5000000 y 76 registros de mercado consistentes.')
