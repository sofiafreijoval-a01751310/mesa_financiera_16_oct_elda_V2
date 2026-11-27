"""Versiona la revisión determinista y sus resultados; no contacta servicios."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for private in [False,True]:
    source=ROOT.parent/'output/Lincoln_Apoyos_v05_PARA_IMPORTAR.json' if private else ROOT/'exports/Lincoln_Apoyos_v05_PUBLICO.json'
    if not source.exists():continue
    w=json.loads(source.read_text())
    w['name']='Lincoln | Apoyos a Distribuidores | Revisión versionada v06'
    w['active']=False;w['pinData']={}
    for n in w['nodes']:
        if n['name']=='Loop revisión determinista':
            n['parameters']['jsCode']=(ROOT/'src/n8n_v04/calculo.js').read_text()+'\n'+(ROOT/'src/n8n_v06/revision.js').read_text()
        if n['name']=='Preparar registro del caso':
            s=n['parameters']['jsCode']
            s=s.replace('const version=resultado.estado===\"PENDIENTE_APROBACION\"?\"1\":\"0\";','''const c=resultado.control_determinista;
 const pendiente=resultado.estado==="PENDIENTE_APROBACION";
 if(pendiente&&(!Number.isInteger(c?.version_propuesta)||c.version_propuesta<1||c.version_propuesta>3||!Array.isArray(c.traza)||c.traza.length!==c.version_propuesta||c.traza.some((t,i)=>t.caso_id!==original.caso_id||t.version_propuesta!==i+1)||c.traza[c.traza.length-1].ok!==true))throw new Error("Versionado de revisión inválido");
 const version=pendiente?String(c.version_propuesta):"0";''')
            s=s.replace('if(version===\"1\" &&','if(pendiente &&')
            n['parameters']['jsCode']=s
        if n['name']=='Enviar resultado Lincoln':
            s=n['parameters']['text']
            s=s.replace(' + " o /rechazar "', ' + (JSON.parse($json.propuesta_json).resultado.propuesta?.resultado?.requiere_aceptacion_ajuste===true ? " ACEPTAR_AJUSTE" : "") + " o /rechazar "')
            n['parameters']['text']=s
    dest=ROOT.parent/'output/Lincoln_Apoyos_v06_PARA_IMPORTAR.json' if private else ROOT/'exports/Lincoln_Apoyos_v06_PUBLICO.json'
    dest.write_text(json.dumps(w,ensure_ascii=False,indent=2))
print('v06 generado inactivo; sin modelos ni envío de mensajes.')
