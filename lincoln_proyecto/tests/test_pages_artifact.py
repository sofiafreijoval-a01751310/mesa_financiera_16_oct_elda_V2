import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from esperar_artefacto_pages import esperar

class ArtifactTests(unittest.TestCase):
    def test_eventual_visibility(self):
        responses=iter([{'artifacts':[]},{'artifacts':[{'id':7,'name':'github-pages','expired':False}]}]);pauses=[]
        self.assertEqual(esperar(lambda:next(responses),dormir=pauses.append),{'artifact_id':7,'intentos':2})
        self.assertEqual(pauses,[2])
    def test_missing_artifact_stops_after_bound(self):
        calls=[]
        def fetch():calls.append(1);return {'artifacts':[]}
        with self.assertRaises(RuntimeError):esperar(fetch,intentos=3,pausa=0,dormir=lambda _:None)
        self.assertEqual(len(calls),3)
    def test_ambiguous_or_expired_artifact(self):
        item={'id':7,'name':'github-pages','expired':False}
        with self.assertRaises(ValueError):esperar(lambda:{'artifacts':[item,item]},intentos=1)
        with self.assertRaises(RuntimeError):esperar(lambda:{'artifacts':[dict(item,expired=True)]},intentos=1)
    def test_auth_error_never_retried(self):
        calls=[]
        def denied():calls.append(1);raise PermissionError('Acceso denegado')
        with self.assertRaises(PermissionError):esperar(denied,dormir=lambda _:None)
        self.assertEqual(len(calls),1)
