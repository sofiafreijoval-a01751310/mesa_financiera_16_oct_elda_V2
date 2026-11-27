"""Empaqueta exclusivamente archivos del commit y el PDF generado, sin credenciales locales."""
import hashlib
import json
import os
import re
import subprocess
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output'
PDF=OUT/'pdf/Informe_Lincoln_Revision.pdf'
ZIP=OUT/'Freijo_Valdovinos_Sofia_AI_Tools_ProyectoFinal_REVISION.zip'


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def main():
    data=PDF.read_bytes()
    if not data.startswith(b'%PDF-') or len(re.findall(rb'/Type\s*/Page\b',data))!=10:
        raise ValueError('PDF ausente o distinto de diez páginas')
    names=git('ls-files','-z').decode().strip('\0').split('\0')
    commit=git('rev-parse','HEAD').decode().strip()
    files=[];payload=[]
    for name in names:
        if not name or name.startswith('/') or '..' in Path(name).parts:
            raise ValueError('Ruta no admisible')
        raw=git('show','HEAD:'+name)
        digest=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        files.append({'ruta':'repositorio/'+name,'git_blob_sha1':digest,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
        payload.append(('repositorio/'+name,raw))
    repo=os.environ.get('GITHUB_REPOSITORY','sofiafreijoval-a01751310/mesa_financiera_16_oct_elda_V2')
    run=os.environ.get('GITHUB_RUN_ID','')
    manifest={'proyecto':'Lincoln | Apoyos a Distribuidores','estado':'REVISION: pendientes nueva entrada Telegram, matriz restante, carga amplia, factura total y video','repositorio':repo,'commit':commit,'archivos_git_verificados':len(files),'archivos':files,'pdf_derivado':{'ruta':PDF.name,'sha256':hashlib.sha256(data).hexdigest()},'validacion':'Generación depende del job validar satisfactorio; no se llama a modelos','actions_run':run,'exclusiones':['Sin respaldo privado ni credenciales locales','El contenido fuente se lee del commit, no de archivos locales modificados por pruebas']}
    OUT.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
        for name,raw in payload:z.writestr(name,raw)
        z.writestr(PDF.name,data)
        z.writestr('MANIFIESTO.json',json.dumps(manifest,ensure_ascii=False,indent=2))
        z.writestr('LEEME_ENTREGA.txt','Proyecto Lincoln - VERSION DE REVISION.\nAbrir Informe_Lincoln_Revision.pdf y repositorio/lincoln_proyecto/docs/cierre_y_evidencias.md.\nCaso76 consultado por voz y aprobado por decisión humana77; reflexión individual integrada.\n123: evaluación completa vía proxy,11llamadas conciliadas y V1/V2 correctas.136: corte por cota y lote duplicado bloqueados. V07 nativa publicada. Pendientes: nueva entrada Telegram, matriz restante, carga amplia, factura total y video personal.\nEl manifiesto identifica el commit y los archivos. No sustituye la entrega de la estudiante.\n')
    with zipfile.ZipFile(ZIP) as z:
        if z.testzip() is not None:raise ValueError('ZIP corrupto')
    print(json.dumps({'zip':str(ZIP),'bytes':ZIP.stat().st_size,'commit':commit,'archivos_git':len(files),'pdf_paginas':10}))

if __name__=='__main__':main()
