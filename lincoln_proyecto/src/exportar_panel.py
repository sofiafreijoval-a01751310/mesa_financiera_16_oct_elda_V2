"""Exportación estática de proyección autorizada; nunca publicar tablas privadas completas."""
import argparse,json,hashlib
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS={'caso_id','modo','distribuidor_id','estado','version','apoyo_mxn','creado_utc','decidido_utc','fixture','fuente','version_fuente'}
def exportar(source,exportado=None):
    rows=json.loads(source.read_text())
    if not isinstance(rows,list):raise ValueError('Se requiere proyección autorizada, no tabla privada')
    for r in rows:
        if set(r)!=FIELDS:raise ValueError('Campos no autorizados o incompletos; no publicar')
        if r['modo']!='SIMULADO':raise ValueError('Solo datos ficticios')
    base=json.loads((ROOT/'datos/base_proyecto.json').read_text())
    return {'schema_version':1,'modo':'SIMULADO','exportado_utc':exportado or datetime.now(timezone.utc).isoformat(),'fuente':'lincoln_casos · proyección autorizada manual','version_fuente':'0.1','actualizacion':'Exportación manual reproducible seguida de commit y Actions. No es tiempo real.','presupuesto_nacional_mxn':base['presupuesto_nacional_mxn'],'ventas_nacionales_2025':base['ventas_nacionales_2025'],'distribuidores':[{'id':d['distribuidor_id'],'nombre':d['nombre'],'ventas_2025':d['ventas_2025'],'asignacion_mxn':d['asignacion_mxn'],'disponible_base_mxn':d['disponible_mxn']} for d in base['distribuidores']],'casos':rows,'base_nota':'Asignaciones iniciales sintéticas v0.1; la simulación no consulta saldo operativo en tiempo real.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=ROOT/'datos/panel_proyeccion_autorizada.json');p.add_argument('--exportado-utc');a=p.parse_args()
    out=ROOT/'web/data/panel.json';out.write_text(json.dumps(exportar(a.source,a.exportado_utc),ensure_ascii=False,indent=2));print('Exportación pública generada sin campos privados.')
