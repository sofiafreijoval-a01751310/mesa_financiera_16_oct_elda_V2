"""Carga dos SKILL.md reales y genera candidatos inactivos; no contacta servicios."""
import copy,hashlib,json,uuid
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def node(name,typ,p,pos,ver=2):return dict(name=name,type=typ,parameters=p,position=pos,typeVersion=ver,id=str(uuid.uuid5(uuid.NAMESPACE_URL,'lincoln-v05/'+name)))
def edge(w,a,b):w['connections'][a]={'main':[[dict(node=b,type='main',index=0)]]}
metadata=[]
for name,role in [('preparar-apoyo-lincoln','agente_3_propuesta'),('revisar-apoyo-lincoln','agente_4_revision')]:
 p=R/'skills'/name/'SKILL.md';s=p.read_text();metadata.append(dict(nombre=name,agente=role,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),carga='ARCHIVO_EMBEBIDO_AL_CONSTRUIR_EXPORT',instrucciones=s))
for private in [False,True]:
 src=R.parent/'output/Lincoln_Apoyos_v04_PARA_IMPORTAR.json' if private else R/'exports/Lincoln_Apoyos_v04_PUBLICO.json'
 if not src.exists():continue
 w=json.loads(src.read_text());w['name']='Lincoln | Apoyos a Distribuidores | Skills v05';w['active']=False;w['pinData']={}
 for n in w['nodes']:
  for m in metadata:
   if n['name']==m['agente']:
    n['parameters']['options']['systemMessage']+='\nSKILL CARGADO DESDE ARCHIVO; SHA256 '+m['sha256']+'\n'+m['instrucciones']+'\nADAPTACION N8N CLOUD: aplica estas reglas al caso actual. No ejecutes CLI ni leas archivos locales desde Cloud. Usa las herramientas conectadas y conserva el contrato JSON original del agente. Incluye skills_cargados con nombre y sha256; no inventes ejecución de scripts.'
 meta=[{k:v for k,v in x.items() if k!='instrucciones'} for x in metadata]
 w['nodes'].append(node('Registrar skills cargados','n8n-nodes-base.code',{'jsCode':'const skills='+json.dumps(meta,ensure_ascii=False)+';return $input.all().map((i,index)=>({json:{...i.json,skills_cargados:skills},pairedItem:{item:index}}));'},[800,-160]))
 edge(w,'Inicializar caso','Registrar skills cargados');edge(w,'Registrar skills cargados','Orquestador Lincoln')
 dest=R.parent/'output/Lincoln_Apoyos_v05_PARA_IMPORTAR.json' if private else R/'exports/Lincoln_Apoyos_v05_PUBLICO.json';dest.write_text(json.dumps(w,ensure_ascii=False,indent=2))
# Vencimiento: comparación de la instantánea completa al actualizar evita sobrescribir decisiones concurrentes.
base=json.loads((R/'exports/Lincoln_Apoyos_v04_PUBLICO.json').read_text());old=next(n for n in base['nodes'] if n['name']=='Guardar decisión humana')
read=node('Leer pendientes','n8n-nodes-base.dataTable',{'operation':'get','dataTableId':old['parameters']['dataTableId'],'returnAll':True,'matchType':'allConditions','filters':{'conditions':[{'keyName':'estado','keyValue':'PENDIENTE_APROBACION'}]}},[240,0],1.1)
prepare=node('Seleccionar vencidos simulados','n8n-nodes-base.code',{'jsCode':(R/'src/seleccionar_vencidos.js').read_text()},[480,0])
update=copy.deepcopy(old);update.update(name='Marcar vencimiento condicional',id=str(uuid.uuid4()),position=[720,0]);p=update['parameters'];p['filters']['conditions']=[{'keyValue':'={{ $json.id }}'},{'keyName':'caso_id','keyValue':'={{ $json.caso_id }}'},{'keyName':'version_propuesta','keyValue':'={{ $json.version_propuesta }}'},{'keyName':'estado','keyValue':'PENDIENTE_APROBACION'},{'keyName':'decision_id','condition':'isEmpty'},{'keyName':'propuesta_json','keyValue':'={{ $json.propuesta_original }}'},{'keyName':'vence_en','keyValue':'={{ $json.vence_en }}'}]
sched=dict(name='Lincoln | Revision programada de vencimientos',active=False,nodes=[node('Cada cinco minutos','n8n-nodes-base.scheduleTrigger',{'rule':{'interval':[{'field':'minutes','minutesInterval':5}]}},[0,0],1.2),node('Prueba manual','n8n-nodes-base.manualTrigger',{},[0,180],1),read,prepare,update],connections={},settings={'executionOrder':'v1','timezone':'America/Mexico_City'},pinData={})
for a,b in [('Cada cinco minutos','Leer pendientes'),('Prueba manual','Leer pendientes'),('Leer pendientes','Seleccionar vencidos simulados'),('Seleccionar vencidos simulados','Marcar vencimiento condicional')]:edge(sched,a,b)
(R/'exports/Lincoln_Vencimientos_Programados_PUBLICO.json').write_text(json.dumps(sched,ensure_ascii=False,indent=2))
print('Generados candidatos v05 y tarea cada 5 minutos; inactivos, sin llamadas API.')
