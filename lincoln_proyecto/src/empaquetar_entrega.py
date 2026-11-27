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
PDF=OUT/'pdf/Informe_Lincoln.pdf'
GUIDE=OUT/'pdf/Guia_Entrega_y_Grabacion.pdf'
ZIP=OUT/'Freijo_Valdovinos_Sofia_AI_Tools_ProyectoFinal.zip'


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def main():
    data=PDF.read_bytes()
    guide_data=GUIDE.read_bytes()
    if not guide_data.startswith(b'%PDF-'):raise ValueError('Falta guía de entrega')
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
    manifest={'proyecto':'Lincoln | Apoyos a Distribuidores','estado':'PAQUETE_ENTREGA_CON_LIMITACIONES_DECLARADAS: faltan video personal y pruebas de matriz señaladas','repositorio':repo,'commit':commit,'archivos_git_verificados':len(files),'archivos':files,'pdf_derivado':{'ruta':PDF.name,'sha256':hashlib.sha256(data).hexdigest()},'anexos_derivados':[{'ruta':GUIDE.name,'sha256':hashlib.sha256(guide_data).hexdigest()}],'validacion':'Generación depende del job validar satisfactorio; no se llama a modelos','actions_run':run,'exclusiones':['Sin respaldo privado ni credenciales locales','El contenido fuente se lee del commit, no de archivos locales modificados por pruebas']}
    OUT.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
        for name,raw in payload:z.writestr(name,raw)
        z.writestr(PDF.name,data)
        z.writestr(GUIDE.name,guide_data)
        z.writestr('MANIFIESTO.json',json.dumps(manifest,ensure_ascii=False,indent=2))
        z.writestr('LEEME_ENTREGA.txt','Proyecto Lincoln - PAQUETE PARA ENTREGA CON LIMITACIONES DECLARADAS.\nAbrir Informe_Lincoln.pdf, Guia_Entrega_y_Grabacion.pdf y repositorio/lincoln_proyecto/docs/ENTREGA_FINAL.md.\n140: entrada nueva Telegram, revisión V1/V2 y respuesta confirmada.123:11llamadas conciliadas.136: corte previo y lote duplicado bloqueados.\nPendientes: video personal, cierre humano del mismo caso nuevo y pruebas indicadas en tests/pruebas.csv. No declarar100% de la rúbrica.\nEl manifiesto identifica commit y fuentes exactas; nunca incluye credenciales privadas.\n')
    with zipfile.ZipFile(ZIP) as z:
        if z.testzip() is not None:raise ValueError('ZIP corrupto')
    print(json.dumps({'zip':str(ZIP),'bytes':ZIP.stat().st_size,'commit':commit,'archivos_git':len(files),'pdf_paginas':10}))

if __name__=='__main__':main()
