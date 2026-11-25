"""Espera acotada de visibilidad del artefacto; no omite la validación previa."""
import json
import os
import re
import time
import urllib.request


def esperar(fetch, *, intentos=8, pausa=2, dormir=time.sleep, nombre='github-pages', artifact_id=None):
    if not isinstance(intentos,int) or isinstance(intentos,bool) or not 1<=intentos<=8:
        raise ValueError('Entre uno y ocho intentos')
    if not 0<=pausa<=2:
        raise ValueError('Pausa máxima dos segundos')
    for vuelta in range(1,intentos+1):
        datos=fetch()
        if not isinstance(datos,dict) or not isinstance(datos.get('artifacts'),list):
            raise ValueError('Respuesta de artefactos inválida')
        encontrados=[a for a in datos['artifacts'] if a.get('name')==nombre and a.get('expired') is False and (artifact_id is None or a.get('id')==artifact_id)]
        if len(encontrados)>1:
            raise ValueError('Artefactos github-pages ambiguos')
        if encontrados:
            artifact_id=encontrados[0].get('id')
            if not isinstance(artifact_id,int) or isinstance(artifact_id,bool) or artifact_id<=0:
                raise ValueError('Identificador de artefacto inválido')
            return {'artifact_id':artifact_id,'intentos':vuelta}
        if vuelta<intentos:dormir(pausa)
    raise RuntimeError('Artefacto no visible tras espera acotada; publicación detenida')


def main():
    repo=os.environ['GITHUB_REPOSITORY'];run=os.environ['GITHUB_RUN_ID']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repo) or not re.fullmatch(r'[1-9][0-9]*',run):
        raise ValueError('Repositorio o ejecución inválidos')
    token=os.environ['GH_TOKEN']
    url=f'https://api.github.com/repos/{repo}/actions/runs/{run}/artifacts?per_page=100'
    def fetch():
        req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','Authorization':'Bearer '+token,'X-GitHub-Api-Version':'2022-11-28'})
        # Los errores HTTP, incluidos permiso y cuota, detienen la publicación.
        # Solo se reintenta una respuesta válida en la que el artefacto aún no aparece.
        with urllib.request.urlopen(req,timeout=5) as response:
            return json.load(response)
    nombre=os.environ.get('EXPECTED_ARTIFACT_NAME','github-pages')
    expected_id=os.environ.get('EXPECTED_ARTIFACT_ID','')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+',nombre) or not re.fullmatch(r'[1-9][0-9]*',expected_id):
        raise ValueError('Artefacto esperado inválido')
    print(json.dumps(esperar(fetch,nombre=nombre,artifact_id=int(expected_id))))

if __name__=='__main__':main()
