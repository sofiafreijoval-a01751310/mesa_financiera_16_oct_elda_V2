"""Controles locales persistentes; integrar ANTES del modelo en producción."""
import json
import re
import sqlite3
from contextlib import closing
from decimal import Decimal
from pathlib import Path

class Guardianes:
    def __init__(self,path):
        self.path=str(path)
        with closing(self.connect()) as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS requests (
                event_id TEXT PRIMARY KEY, case_id TEXT NOT NULL, user_id TEXT NOT NULL,
                reserved_microusd INTEGER NOT NULL CHECK(reserved_microusd>=0),
                actual_microusd INTEGER CHECK(actual_microusd>=0),state TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS limits(case_id TEXT PRIMARY KEY,cap_microusd INTEGER NOT NULL);''')
    def connect(self):
        db=sqlite3.connect(self.path,timeout=5,isolation_level=None)
        db.execute('PRAGMA busy_timeout=5000')
        return db
    @staticmethod
    def micros(value):
        n=Decimal(str(value))
        if isinstance(value,bool) or not n.is_finite() or n<0 or n*1000000!=(n*1000000).to_integral_value():
            raise ValueError('USD inválido; máximo seis decimales')
        return int(n*1000000)
    def admit(self,event_id,case_id,user_id,allowed_user,bound_usd,cap_usd='0.25'):
        if not user_id or user_id!=allowed_user: raise PermissionError('Usuario no autorizado')
        if not re.fullmatch(r'LIN-\d+-\d+',str(case_id)): raise ValueError('Folio inválido')
        if not isinstance(event_id,str) or not event_id or len(event_id)>200: raise ValueError('Evento inválido')
        bound,cap=self.micros(bound_usd),self.micros(cap_usd)
        if bound<=0 or cap<=0: raise ValueError('Cota y límite deben ser positivos')
        with closing(self.connect()) as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                if db.execute('SELECT 1 FROM requests WHERE event_id=?',(event_id,)).fetchone():
                    db.rollback();return {'admitido':False,'motivo':'DUPLICADO'}
                row=db.execute('SELECT cap_microusd FROM limits WHERE case_id=?',(case_id,)).fetchone()
                if row and row[0]!=cap: raise ValueError('Límite del caso es inmutable')
                db.execute('INSERT OR IGNORE INTO limits VALUES (?,?)',(case_id,cap))
                spent=db.execute('SELECT COALESCE(SUM(COALESCE(actual_microusd,reserved_microusd)),0) FROM requests WHERE case_id=?',(case_id,)).fetchone()[0]
                if spent+bound>cap:
                    db.rollback();return {'admitido':False,'motivo':'LIMITE_COSTO'}
                db.execute('INSERT INTO requests VALUES (?,?,?,?,NULL,?)',(event_id,case_id,user_id,bound,'RESERVADO'))
                db.commit();return {'admitido':True,'motivo':'RESERVA_PREVIA'}
            except Exception:
                db.rollback();raise
    def reconcile(self,event_id,actual_usd):
        actual=self.micros(actual_usd)
        with closing(self.connect()) as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT reserved_microusd,actual_microusd FROM requests WHERE event_id=?',(event_id,)).fetchone()
            if not row: db.rollback();raise ValueError('Reserva inexistente')
            if row[1] is not None:
                db.rollback();raise ValueError('Consumo ya conciliado')
            # Guardar incluso un exceso observado para no ocultar el gasto real.
            state='COTA_EXCEDIDA' if actual>row[0] else 'CONCILIADO'
            db.execute('UPDATE requests SET actual_microusd=?,state=? WHERE event_id=?',(actual,state,event_id));db.commit()
            return state

def allow_tool(name):
    allowed={'consultar_ventas','consultar_presupuesto','consultar_mercado','calcular_propuesta','consultar_caso_lincoln'}
    if name not in allowed: raise PermissionError('Herramienta fuera de lista permitida')
    return True

def public_case(case):
    # Proyección por lista permitida: nunca devolver el objeto privado completo.
    keys=('caso_id','estado','version_propuesta','distribuidor','apoyo_mxn','modo')
    return {key:case[key] for key in keys if key in case}
