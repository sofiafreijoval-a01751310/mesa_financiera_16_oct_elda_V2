import copy
import importlib.util
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from guardianes import Guardianes,allow_tool,public_case
from loop_servicio import recuperar
SKILL=Path(__import__('os').environ.get('LINCOLN_SKILL_ROOT',str(ROOT/'skills/revisar-apoyo-lincoln')))
spec=importlib.util.spec_from_file_location('revisor',SKILL/'scripts/revisar.py')
revisor=importlib.util.module_from_spec(spec);spec.loader.exec_module(revisor)

def fixture(balance='650000',inv='400000'):
    return {'caso_id':'LIN-101-1','modo':'SIMULADO','inversion_mxn':inv,
        'datos_verificados':{'caso_id':'LIN-101-1','distribuidor_id':'D01','fuente':'base_proyecto','version':'0.1','saldo_mxn':balance},'propuesta':{}}
class ReviewTests(unittest.TestCase):
    def test_correction_and_source_unchanged(self):
        c=fixture();r=revisor.run_loop(c)
        self.assertTrue(r['ok']);self.assertEqual(len(r['traza']),2)
        self.assertEqual(r['caso']['propuesta']['apoyo_mxn'],'200000.00')
        self.assertEqual(c['datos_verificados'],r['caso']['datos_verificados'])
        self.assertEqual(r['caso']['propuesta']['estado'],'PENDIENTE_APROBACION')
    def test_limited(self):
        r=revisor.run_loop(fixture('62500'))
        self.assertTrue(r['ok']);self.assertEqual(r['caso']['propuesta']['inversion_ajustada_mxn'],'125000')
        self.assertTrue(r['caso']['propuesta']['requiere_aceptacion_alcance'])
    def test_infinite_negative_and_boolean(self):
        for bad in ['Infinity','NaN','-1',True,'0.001']:
            with self.subTest(bad=bad):
                r=revisor.run_loop(fixture(inv=bad));self.assertFalse(r['ok']);self.assertEqual(len(r['traza']),1)
    def test_no_source(self):
        c=fixture();c['datos_verificados']['version']='';self.assertFalse(revisor.run_loop(c)['ok'])
    def test_wrong_case(self):
        c=fixture();c['datos_verificados']['caso_id']='LIN-9-1';self.assertFalse(revisor.run_loop(c)['ok'])
    def test_malformed_objects(self):
        for case in [[],None,{'caso_id':'LIN-1-1'},dict(fixture(),propuesta=None)]:
            with self.subTest(case=case):self.assertFalse(revisor.review(case)['ok'])
    def test_extra_fields_preserved(self):
        c=fixture();c['propuesta']={'nota':'No modificar fuente','aceptacion_alcance':False}
        r=revisor.run_loop(c)
        self.assertEqual(r['caso']['propuesta']['nota'],'No modificar fuente')
        self.assertIs(r['caso']['propuesta']['aceptacion_alcance'],False)
    def test_loop_cap(self):
        with self.assertRaises(ValueError):revisor.run_loop(fixture(),4)
        self.assertFalse(revisor.run_loop(fixture(),1)['ok'])
    def test_odd_cent_and_zero_balance(self):
        r=revisor.run_loop(fixture('0','0.01'));self.assertTrue(r['ok'])
        self.assertEqual(r['caso']['propuesta']['apoyo_mxn'],'0.00')
class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'ledger.db';self.g=Guardianes(self.path)
    def tearDown(self):self.tmp.cleanup()
    def admit(self,event,amount='.10'):
        return self.g.admit(event,'LIN-1-1','demo','demo',amount)
    def test_durable_dedup(self):
        self.assertTrue(self.admit('1')['admitido'])
        again=Guardianes(self.path).admit('1','LIN-1-1','demo','demo','.10')
        self.assertEqual(again['motivo'],'DUPLICADO')
    def test_budget(self):
        self.admit('1');self.admit('2');self.assertEqual(self.admit('3')['motivo'],'LIMITE_COSTO')
    def test_auth(self):
        with self.assertRaises(PermissionError):self.g.admit('1','LIN-1-1','other','demo','.01')
    def test_cap_immutable(self):
        self.admit('1')
        with self.assertRaises(ValueError):self.g.admit('2','LIN-1-1','demo','demo','.10','100')
    def test_concurrent_duplicates(self):
        with ThreadPoolExecutor(8) as ex:r=list(ex.map(lambda _:self.admit('same'),range(8)))
        self.assertEqual(sum(x['admitido'] for x in r),1)
    def test_concurrent_budget(self):
        with ThreadPoolExecutor(8) as ex:r=list(ex.map(lambda i:self.admit(str(i)),range(8)))
        self.assertEqual(sum(x['admitido'] for x in r),2)
    def test_reconcile(self):
        self.admit('1');self.assertEqual(self.g.reconcile('1','.02'),'CONCILIADO')
        with self.assertRaises(ValueError):self.g.reconcile('1','.02')
    def test_excess_recorded(self):
        self.admit('1');self.assertEqual(self.g.reconcile('1','.30'),'COTA_EXCEDIDA')
        self.assertFalse(self.admit('2')['admitido'])
    def test_excess_invalidates_bounds_below_case_cap(self):
        self.admit('1')
        self.assertEqual(self.g.reconcile('1','.11'),'COTA_EXCEDIDA')
        # USD .11 + .01 cabe en .25, pero la cota dejó de ser confiable.
        self.assertEqual(self.admit('2','.01')['motivo'],'COTA_INVALIDADA')
    def test_invalidated_bounds_survive_restart_and_concurrency(self):
        self.admit('1');self.g.reconcile('1','.11')
        def attempt(i):
            return Guardianes(self.path).admit('after-'+str(i),'LIN-1-1','demo','demo','.01')
        with ThreadPoolExecutor(8) as ex:r=list(ex.map(attempt,range(8)))
        self.assertTrue(all(x['motivo']=='COTA_INVALIDADA' for x in r))
    def test_projection_and_allowlist(self):
        self.assertEqual(public_case({'caso_id':'LIN-1-1','token':'SECRET','usuario':'private'}),{'caso_id':'LIN-1-1'})
        self.assertTrue(allow_tool('consultar_ventas'))
        with self.assertRaises(PermissionError):allow_tool('transferir_dinero')
    def test_recovery_loop(self):
        tries=[];trace=[]
        def query():
            tries.append(1)
            if len(tries)<3:raise TimeoutError()
            return {'caso_id':'LIN-1-1'}
        r=recuperar(query,self.g,'LIN-1-1','demo','test',trace,allowed_user='demo')
        self.assertEqual(r['estado'],'OK');self.assertEqual(len(trace),3)
    def test_recovery_auth(self):
        trace=[]
        with self.assertRaises(PermissionError):
            recuperar(lambda:{'caso_id':'LIN-1-1'},self.g,'LIN-1-1','intruso','t',trace,allowed_user='demo')
    def test_recovery_stops(self):
        trace=[]
        def fail():raise ConnectionError()
        self.assertEqual(recuperar(fail,self.g,'LIN-1-1','demo','test',trace,allowed_user='demo')['estado'],'ESCALAR')
        self.assertEqual(len(trace),3)
if __name__=='__main__':unittest.main()
