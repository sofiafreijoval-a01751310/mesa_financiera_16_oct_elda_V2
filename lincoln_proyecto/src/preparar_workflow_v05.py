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
  if n['name']=='calcular_propuesta':
   schema=json.loads(n['parameters']['inputSchema'])
   schema['properties']['skills_cargados']={'type':'array','maxItems':2,'description':'Metadatos de transporte n8n. Ignorados por el cálculo financiero.','items':{'type':'object','additionalProperties':False,'required':['nombre','agente','sha256','carga'],'properties':{'nombre':{'type':'string','enum':['preparar-apoyo-lincoln','revisar-apoyo-lincoln']},'agente':{'type':'string','enum':['agente_3_propuesta','agente_4_revision']},'sha256':{'type':'string','pattern':'^[a-f0-9]{64}$'},'carga':{'type':'string','enum':['ARCHIVO_EMBEBIDO_AL_CONSTRUIR_EXPORT']}}}}
   transport={'chat_id':{'type':'string','pattern':'^-?[0-9]{1,20}$'},'update_id':{'type':'integer','minimum':0},'message_id':{'type':'integer','minimum':0},'autorizado':{'type':'boolean'},'ruta':{'type':'string','enum':['PROCESAR']},'respuesta':{'type':'string','maxLength':4000},'decision':{'type':'null'}}
   for key,definition in transport.items():schema['properties'][key]={**definition,'description':'Metadata de transporte n8n; no se usa para cálculo ni autorización.'}
   n['parameters']['inputSchema']=json.dumps(schema,ensure_ascii=False,indent=2)
  if n['name']=='Preparar registro del caso':
   n['parameters']['jsCode']=n['parameters']['jsCode'].replace('caso_original:original,resultado,aprobacion_humana:false','caso_original:original,resultado,skills_configurados:$("Registrar skills cargados").first().json.skills_cargados,evidencia_skills:"INSTRUCCIONES_EMBEBIDAS_EN_PROMPTS; NO_EQUIVALE_A_VALIDACION_DEL_MODELO",aprobacion_humana:false')
  if n['name']=='Validar entrada Telegram':
   branch=''' else if(/^\\/(estado)(?:@\\w+)?(?:\\s|$)/i.test(texto)){
  const c=texto.match(/^\\/estado(?:@\\w+)?\\s+(LIN-\\d+-\\d+)\\s+([1-9]\\d*)$/i);
  if(!c){ruta="RESPONDER";respuesta="Formato: /estado LIN-25-1 1. Incluye folio y versión.";}
  else {ruta="DECIDIR";decision={accion:"estado",caso_id:c[1].toUpperCase(),version:c[2],decision_id:String(e.update_id??"")};}
 }
'''
   n['parameters']['jsCode']=n['parameters']['jsCode'].replace(' else if(/^\\/(aprobar|rechazar)',branch+' else if(/^\\/(aprobar|rechazar)').replace('Para decidir usa /aprobar','Para consultar usa /estado FOLIO VERSION. Para decidir usa /aprobar')
  if n['name']=='Validar decisión humana':
   anchor='if(r.estado!=="PENDIENTE_APROBACION"||r.decision_id)'
   branch='''if(d.accion==="estado"){
 const estados=["PENDIENTE_APROBACION","APROBADO_SIMULADO","RECHAZADO","VENCIDO","REQUIERE_ACLARACION","DETENIDO"];
 if(!estados.includes(r.estado))return [{json:base}];
 const vence=Date.parse(r.vence_en),vencido=r.estado==="PENDIENTE_APROBACION"&&Number.isFinite(vence)&&Date.now()>=vence;
 return [{json:{...base,respuesta:"Consulta de solo lectura. Caso "+r.caso_id+", versión "+r.version_propuesta+", estado registrado: "+r.estado+(vencido?". Su vigencia ya terminó; no puede aprobarse":"")+". Simulación académica; sin cambios de presupuesto."}}];
}
'''
   n['parameters']['jsCode']=n['parameters']['jsCode'].replace(anchor,branch+anchor)
 meta=[{k:v for k,v in x.items() if k!='instrucciones'} for x in metadata]
 w['nodes'].append(node('Registrar skills cargados','n8n-nodes-base.code',{'jsCode':'const skills='+json.dumps(meta,ensure_ascii=False)+';return $input.all().map((i,index)=>({json:{...i.json,skills_cargados:skills},pairedItem:{item:index}}));'},[800,-160]))
 edge(w,'Inicializar caso','Registrar skills cargados');edge(w,'Registrar skills cargados','Orquestador Lincoln')
 dest=R.parent/'output/Lincoln_Apoyos_v05_PARA_IMPORTAR.json' if private else R/'exports/Lincoln_Apoyos_v05_PUBLICO.json';dest.write_text(json.dumps(w,ensure_ascii=False,indent=2))
# Vencimiento: comparación de la instantánea completa al actualizar evita sobrescribir decisiones concurrentes.
base=json.loads((R/'exports/Lincoln_Apoyos_v04_PUBLICO.json').read_text());old=next(n for n in base['nodes'] if n['name']=='Guardar decisión humana')
read=node('Leer pendientes','n8n-nodes-base.dataTable',{'operation':'get','dataTableId':old['parameters']['dataTableId'],'returnAll':True,'matchType':'allConditions','filters':{'conditions':[{'keyName':'estado','keyValue':'PENDIENTE_APROBACION'}]}},[240,0],1.1)
prepare=node('Seleccionar vencidos simulados','n8n-nodes-base.code',{'jsCode':(R/'src/seleccionar_vencidos.js').read_text()},[480,0])
update=copy.deepcopy(old);update.update(name='Marcar vencimiento condicional',id=str(uuid.uuid4()),position=[720,0]);p=update['parameters'];p['filters']['conditions']=[{'keyValue':'={{ $json.id }}'},{'keyName':'caso_id','keyValue':'={{ $json.caso_id }}'},{'keyName':'version_propuesta','keyValue':'={{ $json.version_propuesta }}'},{'keyName':'estado','keyValue':'PENDIENTE_APROBACION'},{'keyName':'decision_id','condition':'isEmpty'},{'keyName':'propuesta_json','keyValue':'={{ $json.propuesta_original }}'},{'keyName':'vence_en','keyValue':'={{ $json.vence_en }}'}]
sched=dict(name='Lincoln | Vencimientos diarios 09h',active=False,nodes=[node('Diario a las 09h','n8n-nodes-base.scheduleTrigger',{'rule':{'interval':[{'field':'cronExpression','expression':'0 9 * * *'}]}},[0,0],1.2),node('Prueba manual','n8n-nodes-base.manualTrigger',{},[0,180],1),read,prepare,update],connections={},settings={'executionOrder':'v1','timezone':'America/Mexico_City','availableInMCP':False},pinData={})
for a,b in [('Diario a las 09h','Leer pendientes'),('Prueba manual','Leer pendientes'),('Leer pendientes','Seleccionar vencidos simulados'),('Seleccionar vencidos simulados','Marcar vencimiento condicional')]:edge(sched,a,b)
(R/'exports/Lincoln_Vencimientos_Programados_PUBLICO.json').write_text(json.dumps(sched,ensure_ascii=False,indent=2))
print('Generados exports reproducibles v05 y tarea diaria 09h; inactivos al importar, sin llamadas API.')
