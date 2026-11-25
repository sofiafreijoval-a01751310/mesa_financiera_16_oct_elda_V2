"""Construye una copia candidata; nunca llama n8n ni activa el bot."""
import json,copy,uuid,re,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'exports/Lincoln_Workflow_Telegram_Aprobacion_v03.json'
w=json.loads(SOURCE.read_text());w=copy.deepcopy(w)
for key in ['id','versionId','meta','nodeGroups','tags']:w.pop(key,None)
w['name']='Lincoln | Apoyos a Distribuidores | Revision v04';w['active']=False;w['pinData']={};w['settings']['availableInMCP']=False
nodes={n['name']:n for n in w['nodes']}
core=(ROOT/'src/n8n_v04/calculo.js').read_text()
nodes['calcular_propuesta']['parameters']['jsCode']=core+'''\nlet d=query;try{if(typeof d==='string')d=JSON.parse(d);if(d&&typeof d.datos==='string')d=JSON.parse(d.datos);}catch{return JSON.stringify({ok:false,errores:['JSON inválido']});}return JSON.stringify(calcularPropuesta(d));'''
p=nodes['calcular_propuesta']['parameters'];schema=json.loads(p['inputSchema']);schema['additionalProperties']=False
for k in ['inversion_total_mxn','asignacion_mxn','disponible_mxn']:schema['properties'][k].update({'minimum':0,'maximum':100000000,'multipleOf':0.01})
schema['properties']['inversion_total_mxn']['exclusiveMinimum']=0;schema['properties']['asignacion_mxn']['exclusiveMinimum']=0
schema['properties']['ventas']['required']=['Corsair','Nautilus','Aviator','Navigator'];schema['properties']['ventas']['additionalProperties']=False
for v in schema['properties']['ventas']['properties'].values():v.update({'type':'integer','minimum':0})
m=schema['properties']['mercado'];m.update({'minItems':4,'maxItems':4});m['items']['required']=list(m['items']['properties']);m['items']['properties']['modelo']['enum']=['Corsair','Nautilus','Aviator','Navigator'];m['items']['properties']['volumen_2025'].update({'type':'integer','minimum':0});m['items']['properties']['penetracion_pct'].update({'minimum':0,'maximum':100});m['items']['properties']['crecimiento_real_pct']['minimum']=-100
p['inputSchema']=json.dumps(schema,ensure_ascii=False,indent=2)
# Las herramientas consultan siempre el ID canónico, sin aceptar el parámetro del modelo.
for name in ['consultar_ventas','consultar_presupuesto','consultar_mercado']:
 p=nodes[name]['parameters'];p['filters']['conditions'][0]['keyValue']='={{ $("Inicializar caso").first().json.distribuidor_id ?? "SIN_DISTRIBUIDOR" }}'
 p['limit']=5 if name=='consultar_mercado' else 2
# No expone IDs arbitrarios ni la solicitud cruda en las herramientas de fuente.
extra='''\nCONTRATO V04: La salida final conserva además los cuatro OBJETOS completos: solicitud_validada, datos_verificados, propuesta y revision. Todos deben conservar el folio canónico. No resumir esos cuatro bloques. El campo resultado sigue siendo un resumen de máximo 300 palabras. Sin esos objetos el servidor detiene el registro. El control determinista posterior consulta nuevamente las fuentes, verifica y corrige solo cifras derivadas. No afirmar reserva, deduplicación ni gasto real. Una revisión válida no aprueba presupuesto.'''
nodes['Orquestador Lincoln']['parameters']['options']['systemMessage']+=extra
nodes['Orquestador Lincoln']['parameters']['options']['systemMessage']=nodes['Orquestador Lincoln']['parameters']['options']['systemMessage'].replace('La respuesta final debe tener máximo 300 palabras','El campo resultado debe tener máximo 300 palabras').replace('No copies todos los bloques completos en la respuesta final.','Conserva los cuatro bloques completos en la salida estructurada.')
# Corrige la aritmética, sin fingir que el límite nominal es un tope de gasto.
nodes['agente_3_propuesta']['parameters']['options']['systemMessage']+='\nV04: importa solo números JSON finitos. En centavos impares, redondear el apoyo hacia abajo y mantener aportaciones iguales; el centavo no elegible requiere aceptación del ajuste. No declares saldo aprobado ni gasto de IA medido.'
# Comando explícito de aceptación de alcance.
p=nodes['Validar entrada Telegram']['parameters'];s=p['jsCode'];s=s.replace('([1-9]\\d*)$/i','([1-9]\\d*)(?:\\s+(ACEPTAR_AJUSTE))?$/i');s=s.replace('decision_id:String(e.update_id??"")','acepta_ajuste:c[1].toLowerCase()==="aprobar"&&Boolean(c[4]),decision_id:String(e.update_id??"")');s=s.replace('Incluye el folio y la versión recibidos.','Para aceptar una reducción: /aprobar FOLIO VERSION ACEPTAR_AJUSTE. Incluye el folio y la versión recibidos.');p['jsCode']=s
p=nodes['Validar decisión humana']['parameters'];s=p['jsCode'];needle='const estado=vencido?'
addition='''if(!vencido&&d.accion==='aprobar'){
 const resultado=p.resultado,control=resultado?.control_determinista;
 if(control?.ok!==true||control.version!=='0.4'||!Array.isArray(control.traza)||!control.traza.length||control.traza.at(-1).ok!==true)return [{json:{...base,respuesta:'La propuesta no tiene revisión determinista v04. Solicita una nueva evaluación.'}}];
 const q=resultado.propuesta?.resultado;
 if(!q||q.modifica_presupuesto!==false||q.estado_aprobacion!=='PENDIENTE_APROBACION_HUMANA')throw Error('Propuesta financiera inválida');
 if(q.requiere_aceptacion_ajuste&&d.acepta_ajuste!==true)return [{json:{...base,respuesta:'Confirma expresamente el alcance reducido: /aprobar '+r.caso_id+' '+r.version_propuesta+' ACEPTAR_AJUSTE'}}];
}
'''
s=s.replace(needle,addition+needle).replace('accion:vencido?"vencimiento":d.accion','acepta_ajuste:d.acepta_ajuste===true,accion:vencido?"vencimiento":d.accion');p['jsCode']=s
# El registro conserva el contrato completo y la traza revisada.
p=nodes['Preparar registro del caso']['parameters'];s=p['jsCode'];needle='const version=resultado.estado'
s=s.replace(needle,'if(resultado.estado==="PENDIENTE_APROBACION"&&(resultado.control_determinista?.ok!==true||resultado.control_determinista?.version!=="0.4"))throw new Error("Falta revisión determinista v04");\n '+needle);p['jsCode']=s
# Nodos sobre el camino real previo al registro.
def add(name,type,params,pos,version=2,**flags):
 n={'parameters':params,'id':str(uuid.uuid5(uuid.NAMESPACE_URL,'lincoln-v04/'+name)),'name':name,'type':type,'typeVersion':version,'position':pos,**flags};w['nodes'].append(n);nodes[name]=n

def edge(src,dst,branch=0):
 main=w['connections'].setdefault(src,{}).setdefault('main',[])
 while len(main)<=branch:main.append([])
 main[branch]=[{'node':dst,'type':'main','index':0}]

def iff(expr):return {'conditions':{'options':{'caseSensitive':True,'leftValue':'','typeValidation':'strict','version':2},'conditions':[{'id':str(uuid.uuid4()),'leftValue':expr,'rightValue':True,'operator':{'type':'boolean','operation':'true','singleValue':True}}],'combinator':'and'},'options':{}}
add('Validar contrato de salida','n8n-nodes-base.code',{'jsCode':(ROOT/'src/n8n_v04/contrato.js').read_text()},[1700,0])
add('¿Revisar cifras?','n8n-nodes-base.if',iff('={{ $json.requiere_revision === true }}'),[1920,0],2.4)
for i,(tool,name) in enumerate([('consultar_ventas','Fuente ventas para revisión'),('consultar_presupuesto','Fuente presupuesto para revisión'),('consultar_mercado','Fuente mercado para revisión')]):
 old=nodes[tool]['parameters'];params={k:copy.deepcopy(old[k]) for k in ['operation','dataTableId','matchType','filters','limit']};params['returnAll']=False
 add(name,'n8n-nodes-base.dataTable',params,[2140+i*220,0],1.1,alwaysOutputData=True,executeOnce=True)
add('Loop revisión determinista','n8n-nodes-base.code',{'jsCode':core+'\n'+(ROOT/'src/n8n_v04/revision.js').read_text()},[2800,0])
edge('Orquestador Lincoln','Validar contrato de salida');edge('Validar contrato de salida','¿Revisar cifras?');edge('¿Revisar cifras?','Fuente ventas para revisión',0);edge('¿Revisar cifras?','Preparar registro del caso',1)
edge('Fuente ventas para revisión','Fuente presupuesto para revisión');edge('Fuente presupuesto para revisión','Fuente mercado para revisión');edge('Fuente mercado para revisión','Loop revisión determinista');edge('Loop revisión determinista','Preparar registro del caso')
add('¿Responder por Telegram?','n8n-nodes-base.if',iff('={{ $("Inicializar caso").first().json.canal === "telegram" }}'),[3460,0],2.4)
edge('Guardar caso Lincoln','¿Responder por Telegram?');edge('¿Responder por Telegram?','Enviar resultado Lincoln')
# Retira rutas de MCP del workflow candidato; las credenciales existentes son referencias privadas.
private=ROOT.parent/'output/Lincoln_Apoyos_v04_PARA_IMPORTAR.json';private.parent.mkdir(exist_ok=True);private.write_text(json.dumps(w,ensure_ascii=False,indent=2))
public=copy.deepcopy(w)
authorized=re.search(r'USUARIO_AUTORIZADO = \"([^\"]+)\"',nodes['Validar entrada Telegram']['parameters']['jsCode']).group(1)
for n in public['nodes']:
 n.pop('credentials',None)
 if n['type'] in ['n8n-nodes-base.dataTable','n8n-nodes-base.dataTableTool']:
  rid=n['parameters'].get('dataTableId',{});n['parameters']['dataTableId']={'__rl':True,'value':'CONFIGURAR_TABLA_'+rid.get('cachedResultName','CASOS'),'mode':'id'}
 s=json.dumps(n,ensure_ascii=False);s=s.replace(authorized,'1000000001');n.clear();n.update(json.loads(s))
(ROOT/'exports/Lincoln_Apoyos_v04_PUBLICO.json').write_text(json.dumps(public,ensure_ascii=False,indent=2))
print(json.dumps({'nodos':len(w['nodes']),'activo':w['active'],'archivo_privado':str(private),'sha256_original':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},ensure_ascii=False))
