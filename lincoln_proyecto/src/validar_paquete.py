"""Puerta CI: seguridad y coherencia de lo implementado; no certifica cierre de rúbrica."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
violations=[]
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts or path.suffix in ('.sqlite','.pdf','.png'):continue
    try:text=path.read_text()
    except UnicodeError:continue
    if re.search(r'\b\d{8,12}:[A-Za-z0-9_-]{30,}\b',text):violations.append(str(path.relative_to(ROOT))+': token Telegram')
    if re.search(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}',text):violations.append(str(path.relative_to(ROOT))+': API key')
    if path.name.startswith('.env') and path.name!='.env.example':violations.append('Archivo env privado')
w=json.loads((ROOT/'exports/Lincoln_Workflow_Telegram_Aprobacion_v03.json').read_text())
assert not w.get('active') and not w.get('pinData')
assert all(not n.get('credentials') for n in w['nodes'])
assert len(w['nodes'])==28
voice=json.loads((ROOT/'exports/Lincoln_Consulta_Voz_PUBLICO.json').read_text())
assert voice['active'] is False and not voice['pinData'] and len(voice['nodes'])==4
assert all(not n.get('credentials') for n in voice['nodes'])
assert all(n['parameters'].get('authentication')=='headerAuth' for n in voice['nodes'] if n['type'].endswith('.webhook'))
assert all(n['parameters']['dataTableId']['value']=='CONFIGURAR_TABLA_lincoln_casos' for n in voice['nodes'] if n['type'].endswith('.dataTable'))
for file in (ROOT/'evidencias').glob('LIN-*.json'):
    result=json.loads(file.read_text())
    if result['ok']:
        p=result['caso']['propuesta'];assert p['estado']=='PENDIENTE_APROBACION' and p['modifica_presupuesto'] is False
assert not violations, '\n'.join(violations)
print('PASS: sin patrones de llaves; export inactivo, sin credenciales ni pinData; propuestas no aprueban. Escaneo por patrones, no auditoría exhaustiva.')
