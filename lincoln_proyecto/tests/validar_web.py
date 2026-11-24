"""Puerta de publicación: esquema público, reconciliación, privacidad y recursos."""
import json,re,math
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];WEB=ROOT/'web'
def validate():
    d=json.loads((WEB/'data/panel.json').read_text())
    assert set(d)=={'schema_version','modo','exportado_utc','fuente','version_fuente','actualizacion','presupuesto_nacional_mxn','ventas_nacionales_2025','distribuidores','casos','base_nota'}
    assert d['schema_version']==1 and d['modo']=='SIMULADO'
    datetime.fromisoformat(d['exportado_utc'].replace('Z','+00:00'))
    assert d['presupuesto_nacional_mxn']==5000000 and d['ventas_nacionales_2025']==2000,'Bolsa o ventas nacionales incoherentes'
    dealers=d['distribuidores'];assert len(dealers)==19 and len({x['id'] for x in dealers})==19
    assert sum(x['asignacion_mxn'] for x in dealers)==d['presupuesto_nacional_mxn'],'Asignaciones no reconciliadas'
    assert sum(x['ventas_2025'] for x in dealers)==d['ventas_nacionales_2025']
    for x in dealers:
        assert set(x)=={'id','nombre','ventas_2025','asignacion_mxn','disponible_base_mxn'}
        assert re.fullmatch(r'D(0[1-9]|1[0-9])',x['id'])
        assert x['asignacion_mxn']==x['ventas_2025']*2500
        assert 0<=x['disponible_base_mxn']<=x['asignacion_mxn']
    expected={'caso_id','modo','distribuidor_id','estado','version','apoyo_mxn','creado_utc','decidido_utc','fixture','fuente','version_fuente'}
    assert len({x['caso_id'] for x in d['casos']})==len(d['casos']),'Duplicación de folios'
    for c in d['casos']:
        assert set(c)==expected,'Campo privado o desconocido en caso'
        assert re.fullmatch(r'LIN-\d+-\d+',c['caso_id']) and c['modo']=='SIMULADO'
        assert type(c['version']) is int and c['version']>0 and type(c['fixture']) is bool
        assert c['estado'] in ['APROBADO_SIMULADO','RECHAZADO','VENCIDO','PENDIENTE_APROBACION','REQUIERE_ACLARACION','DETENIDO']
        assert c['fixture'] or c['distribuidor_id'] in {x['id'] for x in dealers}
        if c['estado']=='APROBADO_SIMULADO':assert type(c['apoyo_mxn']) in [int,float] and math.isfinite(c['apoyo_mxn']) and c['apoyo_mxn']>=0
        for key in ['creado_utc','decidido_utc']:
            if c[key] is not None:datetime.fromisoformat(c[key].replace('Z','+00:00'))
    for file in WEB.rglob('*'):
        if not file.is_file():continue
        text=file.read_text()
        assert not re.search(r'\b\d{8,12}:[A-Za-z0-9_-]{30,}\b',text),'Token Telegram en sitio'
        assert not re.search(r'\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{30,}',text),'API key en sitio'
        assert not any(x in text for x in ['8767528799','chat_id','propuesta_json','X-Lincoln-Key','webhook-test','sofiafreijo.app.n8n.cloud']),'Dato privado en sitio'
    class Links(HTMLParser):
        def handle_starttag(self,tag,attrs):
            a=dict(attrs)
            for key in ['src','href']:
                value=a.get(key,'')
                if value and not value.startswith(('#','https:','http:','mailto:')):
                    assert (WEB/value.split('?')[0]).is_file(),'Recurso inexistente: '+value
    Links().feed((WEB/'index.html').read_text())
    print('PASS: esquema público, 19 distribuidores, totales, casos, privacidad y recursos web.')
if __name__=='__main__':validate()
