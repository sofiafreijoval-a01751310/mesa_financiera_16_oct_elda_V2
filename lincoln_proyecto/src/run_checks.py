"""Ejecuta y registra comprobaciones reales; termina con error si alguna falla."""
import json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
commands=[['python3','tests/validar_base.py'],['python3','-m','unittest','discover','-s','tests','-p','test_*.py','-v'],['node','exports/verificar_workflow_v03.cjs'],['python3','src/run_demo.py'],['python3','skills/vizdata/scripts/audit_viz_spec.py','docs/vizdata_brief.json','--strict'],['node','tests/verificar_n8n_loops.cjs'],['python3','tests/validar_web.py'],['node','tests/test_web.cjs'],['python3','src/validar_paquete.py']]
results=[]
for cmd in commands:
 r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=30)
 results.append({'command':cmd,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
report={'fecha_utc':datetime.now(timezone.utc).isoformat(),'scope':'LOCAL sin APIs; no prueba integral en n8n','ok':all(r['returncode']==0 for r in results),'comprobaciones':results}
(ROOT/'evidencias/comprobaciones.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'ok':report['ok'],'comandos':len(results),'evidencia':'evidencias/comprobaciones.json'}))
raise SystemExit(0 if report['ok'] else 1)
