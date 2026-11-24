"""Regenera figura estática auditada por VizData (requiere matplotlib)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
rows=sorted(json.loads((ROOT/'datos/base_proyecto.json').read_text())['distribuidores'],key=lambda x:x['asignacion_mxn'])
fig,ax=plt.subplots(figsize=(10,7.8));fig.patch.set_facecolor('#fbfaf7');ax.set_facecolor('#fbfaf7')
colors=['#aab7bf']*len(rows);colors[-1]='#15455b';colors[0]='#956233'
ax.barh([d['nombre'].replace('Lincoln ','') for d in rows],[d['asignacion_mxn']/1000 for d in rows],color=colors,height=.62)
for i,d in enumerate(rows):ax.text(d['asignacion_mxn']/1000+7,i,f"{d['asignacion_mxn']:,.0f}",va='center',fontsize=9)
ax.set_xlim(0,760);ax.set_xlabel('Asignación de Lincoln (miles de MXN antes de IVA)',fontsize=10)
ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0)
ax.set_title('Monterrey recibe 13% de la bolsa ficticia',loc='left',fontsize=18,pad=26,fontweight='bold')
fig.text(.22,.905,'19 distribuidores · Ventas 2025: 2,000 unidades · Bolsa 2026: MXN 5 millones',fontsize=9,color='#555555')
fig.text(.02,.015,'Fuente: base_proyecto.json v0.1. Datos sintéticos académicos; no oficiales.\nAsignación = ventas del distribuidor / 2,000 × MXN 5,000,000. Corte del informe: 23 nov. 2026.',fontsize=8,color='#555555')
fig.subplots_adjust(left=.22,right=.97,top=.87,bottom=.1)
fig.savefig(ROOT/'docs/asignaciones.png',dpi=150)
