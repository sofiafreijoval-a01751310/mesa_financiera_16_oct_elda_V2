# Lincoln | Apoyos a Distribuidores - complemento reproducible

Sofía Freijo Valdovinos · AI Tools · Prof. Elda Morales.
Datos sintéticos académicos; corte23nov2026. Este subproyecto conserva separada la actividad Mesa Financiera de Batuta, Iris, Euler y Vera.

## Ejecutar sin llaves

Desde `lincoln_proyecto`, Python3.12 y Node22 (sin paquetes externos para las pruebas):

```bash
python3 tests/validar_base.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
node exports/verificar_workflow_v03.cjs
python3 src/run_demo.py
python3 skills/vizdata/scripts/audit_viz_spec.py docs/vizdata_brief.json --strict
python3 src/validar_paquete.py
```

Resultado esperado:base consistente;21pruebas Python;25JS;3casos convergen en2revisiones y1escala;loop recuperación3intentos. Las pruebas no llaman APIs ni mandan Telegram. `run_demo.py` regenera un ledger SQLite de DEMO; nunca apuntarlo a una base operativa.

## Contenido

- `skills/`:dos previos documentados y revisor nuevo reproducible.
- `src/`:guardianes, loops y prueba de paquete.
- `exports/`:respaldo n8n v03 sin credenciales, inactivo y con usuario DEMO.
- `datos/`:base y PMA ficticios v0.1.
- `evidencias/`:dictámenes/trazas/reports de ejecución local.
- `costos/`:conteos medidos de texto estático, supuestos, tarifas y estimaciones.
- `docs/`:costos, ciberseguridad, loops, VizData y pendientes de cierre.

No importar el export sobre un flujo activo sin configurar credenciales/tablas/identidad:es copia pública para revisión. Los guardianes nuevos NO están desplegados en n8n. Los controles financieros requieren una cota máxima por llamada calculada en servidor y una reserva transaccional antes del modelo. El gasto real no está disponible.

El tokenizador binario original permanece en la instalación personal de cotizar-tokens-ia. Su salida medida se conserva con hashes. El script cotizar.py copiado reproduce los cálculos por las entradas JSON, sin necesitar el tokenizador.

Ver `docs/cierre_y_evidencias.md` para pendientes de rúbrica y límites. Ningún dictamen numérico aprueba apoyos ni mueve presupuesto.

## Regenerar el informe y figura (opcional)

Instalar `python3 -m pip install -r requirements-report.txt`. Ejecutar `python3 src/generar_grafica.py` y `python3 src/generar_informe.py`. Requieren fuentes DejaVuSans de la distribución Linux; las pruebas de negocio no dependen de estas librerías. El informe se escribe fuera de la carpeta de código, en output/pdf.

## Prueba aislada en n8n

El export `exports/Lincoln_Prueba_Aislada_Skills_Loops.json` tiene4nodos manuales y no necesita credenciales. Fue importado y ejecutado con PASS (ejecución50). La salida muestra carga de las tres instrucciones, V1/V2 y recuperación acotada. Continúa separado del bot operativo. Validación local del mismo JS:`node tests/verificar_n8n_loops.cjs`.

## Panel y publicación

[Panel Lincoln](https://sofiafreijoval-a01751310.github.io/mesa_financiera_16_oct_elda_V2/) · datos ficticios, exportación manual con fecha, sin datos de chats. GitHub confirmó el despliegue inicial. El control de datos bloqueó una publicación deliberadamente inconsistente; ver `evidencias/pages_despliegue.json` y `docs/Panel_GitHub_Pages.md`.

Pruebas web: `python3 tests/validar_web.py` y `node tests/test_web.cjs` (12 pruebas). La voz embebida y la revisión visual móvil siguen pendientes; no equivalen a las comprobaciones de código. El ZIP y PDF de revisión publicados anteriormente corresponden a un commit anterior y deben regenerarse antes de entregar.
