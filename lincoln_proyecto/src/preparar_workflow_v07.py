"""Prepara un adaptador inactivo; no conecta ni publica servicios."""
import json, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://sofiafreijo.app.n8n.cloud/webhook/lincoln-llm-guard/v1'

def build(source):
    w = json.loads(source.read_text())
    w.update(name='Lincoln | Adaptador OpenAI con admisión | CANDIDATO v07', active=False, pinData={})
    w.pop('id', None)
    w.pop('versionId', None)
    w['settings']['executionTimeout'] = 420
    by_name = {n['name']: n for n in w['nodes']}
    def add(name, typ, parameters, version, **extra):
        n = dict(id=str(uuid.uuid5(uuid.NAMESPACE_URL,'lincoln-v07/'+name)), name=name,
                 type='n8n-nodes-base.'+typ, typeVersion=version,
                 position=[950, -350+len(w['nodes'])*5], parameters=parameters, **extra)
        w['nodes'].append(n)
        return n
    def edge(a,b,out=0):
        outputs=w['connections'].setdefault(a,{'main':[]})['main']
        while len(outputs)<=out: outputs.append([])
        outputs[out].append(dict(node=b,type='main',index=0))
    def condition(name, expression):
        return add(name,'if',{'conditions':{'options':{'caseSensitive':True,'typeValidation':'strict','version':2},
            'conditions':[{'id':str(uuid.uuid5(uuid.NAMESPACE_URL,name)), 'leftValue':'={{ '+expression+' }}',
            'rightValue':True,'operator':{'type':'boolean','operation':'true','singleValue':True}}],
            'combinator':'and'},'options':{}},2.2)
    # Un evento se admite antes de cargar instrucciones o llamar a cualquier agente.
    w['connections']['Inicializar caso']={'main':[[{'node':'Admitir caso en control','type':'main','index':0}]]}
    add('Admitir caso en control','httpRequest',{
        'method':'POST','url':BASE+'/admit', 'authentication':'genericCredentialType',
        'genericAuthType':'httpHeaderAuth','sendHeaders':True,
        'headerParameters':{'parameters':[{'name':'X-Lincoln-Case','value':'={{ $json.caso_id }}'}]},
        'sendBody':True,'contentType':'raw','rawContentType':'application/json',
        'body':'={{ JSON.stringify({case_id:$json.caso_id,event_id:$json.canal==="telegram" ? "telegram:"+String($json.update_id) : "manual:"+String($execution.id)}) }}',
        'options':{'timeout':15000,'redirect':{'redirect':{'followRedirects':False}},
                   'response':{'response':{'fullResponse':True,'neverError':True,'responseFormat':'json'}}}},
        4.2, retryOnFail=False, onError='continueRegularOutput')
    add('Validar admisión','code',{'jsCode':(ROOT/'src/n8n_v07/admission.js').read_text()},2)
    condition('¿Caso admitido?', '$json.control_admitido===true')
    condition('¿Avisar bloqueo por Telegram?', '$json.canal==="telegram" && $json.autorizado===true')
    blocked=add('Responder bloqueo de control','telegram',{
        'chatId':'={{ $("Inicializar caso").first().json.chat_id }}',
        'text':'={{ $json.respuesta_control }}','additionalFields':{'appendAttribution':False}},1.2)
    if by_name.get('Enviar resultado Lincoln',{}).get('credentials'):
        blocked['credentials']=by_name['Enviar resultado Lincoln']['credentials']
    add('Resultado manual bloqueado','code',{'jsCode':'return $input.all();'},2)
    edge('Admitir caso en control','Validar admisión');edge('Validar admisión','¿Caso admitido?')
    edge('¿Caso admitido?','Registrar skills cargados')
    edge('¿Caso admitido?','¿Avisar bloqueo por Telegram?',1)
    edge('¿Avisar bloqueo por Telegram?','Responder bloqueo de control')
    edge('¿Avisar bloqueo por Telegram?','Resultado manual bloqueado',1)
    for n in w['nodes']:
        if n['type'].endswith('.lmChatOpenAi'):
            # La credencial cliente debe usar BASE, nunca la API key real.
            n.pop('credentials',None)
            n['parameters']['model']={'__rl':True,'mode':'id','value':'gpt-4o-mini-2024-07-18'}
            n['parameters']['options'].update(maxTokens=4096,maxRetries=0,timeout=90000)
        if n['name']=='Orquestador Lincoln':
            n['onError']='continueRegularOutput'
            n['parameters']['options']['maxIterations']=12
    contract=by_name['Validar contrato de salida']['parameters']['jsCode']
    by_name['Validar contrato de salida']['parameters']['jsCode']='try {\n'+contract+'\n} catch {\n'+'''const o=$('Inicializar caso').first().json;
return [{json:{output:JSON.stringify({caso_id:o.caso_id,agente:'orquestador',estado:'DETENIDO',resultado:'La evaluación se detuvo por un fallo de integración, control o respuesta inválida. No hay propuesta aprobable. Solicita revisión del sistema.',fuentes:[],advertencias:['CONTROL_O_INTEGRACION_NO_VERIFICADO']}),requiere_revision:false}}];
}'''
    return w

if __name__=='__main__':
    for private in [False,True]:
        source=ROOT.parent/'output/Lincoln_Apoyos_v06_PARA_IMPORTAR.json' if private else ROOT/'exports/Lincoln_Apoyos_v06_PUBLICO.json'
        if not source.exists():continue
        w=build(source)
        dest=ROOT.parent/'output/Lincoln_Apoyos_v07_CANDIDATO_PARA_IMPORTAR.json' if private else ROOT/'exports/Lincoln_Apoyos_v07_CANDIDATO_PUBLICO.json'
        dest.write_text(json.dumps(w,ensure_ascii=False,indent=2))
    print('Adaptador v07 generado inactivo. Faltan credenciales de proxy y verificación viva.')
