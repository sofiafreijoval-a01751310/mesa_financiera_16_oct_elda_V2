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

Resultado esperado: base consistente; pruebas Python y JavaScript satisfactorias;3casos convergen en2revisiones y1escala; recuperación3intentos. El comando python3 src/run_checks.py ejecuta las13comprobaciones vigentes. Las pruebas no llaman APIs ni mandan Telegram. `run_demo.py` regenera un ledger SQLite de DEMO; nunca apuntarlo a una base operativa.

## Contenido

- `skills/`:dos previos documentados y revisor nuevo reproducible.
- `src/`:guardianes, loops y prueba de paquete.
- `exports/`:respaldo n8n v03 sin credenciales, inactivo y con usuario DEMO.
- `datos/`:base y PMA ficticios v0.1.
- `evidencias/`:dictámenes/trazas/reports de ejecución local.
- `costos/`:conteos medidos de texto estático, supuestos, tarifas y estimaciones.
- `docs/`:costos, ciberseguridad, loops, VizData y pendientes de cierre.

No importar el export sobre un flujo activo sin configurar credenciales/tablas/identidad:es copia pública para revisión. El proxy protegido está publicado para pruebas; el adaptador v07 pasó en123 y se publicó tras la prueba negativa136. Los controles financieros requieren una cota máxima por llamada calculada en servidor y una reserva transaccional antes del modelo. El uso por request de123 está conciliado a tarifa estándar; siguen pendientes la factura histórica total, infraestructura y voz.

El tokenizador binario original permanece en la instalación personal de cotizar-tokens-ia. Su salida medida se conserva con hashes. El script cotizar.py copiado reproduce los cálculos por las entradas JSON, sin necesitar el tokenizador.

Ver `docs/cierre_y_evidencias.md` para pendientes de rúbrica y límites. Ningún dictamen numérico aprueba apoyos ni mueve presupuesto.

## Regenerar el informe y figura (opcional)

Instalar `python3 -m pip install -r requirements-report.txt`. Ejecutar `python3 src/generar_grafica.py` y `python3 src/generar_informe.py`. Requieren fuentes DejaVuSans de la distribución Linux; las pruebas de negocio no dependen de estas librerías. El informe se escribe fuera de la carpeta de código, en output/pdf.

## Prueba aislada en n8n

El export `exports/Lincoln_Prueba_Aislada_Skills_Loops.json` tiene4nodos manuales y no necesita credenciales. Fue importado y ejecutado con PASS (ejecución50). La salida muestra carga de las tres instrucciones, V1/V2 y recuperación acotada. Continúa separado del bot operativo. Validación local del mismo JS:`node tests/verificar_n8n_loops.cjs`.

## Panel y publicación

[Panel Lincoln](https://sofiafreijoval-a01751310.github.io/mesa_financiera_16_oct_elda_V2/) · datos ficticios, exportación manual con fecha, sin datos de chats. GitHub confirmó el despliegue inicial. El control de datos bloqueó una publicación deliberadamente inconsistente; ver `evidencias/pages_despliegue.json` y `docs/Panel_GitHub_Pages.md`.

Pruebas web: `python3 tests/validar_web.py` y `node tests/test_web.cjs` (12 pruebas). La voz embebida v5 ya se verificó desde Pages: LIN-76-1,46s, audio confirmado por Sofía. Diseño390/1366 y teclado parcial verificados; falta denegación del micrófono. El ZIP de revisión incluye un manifiesto con el commit exacto; el PDF refleja el despliegue, su bloqueo y su recuperación. Continúan pendientes las pruebas integrales del bot.


## Estado verificado26/nov

- Telegram: consulta de solo lectura, aceptación explícita de alcance, vencimiento, aprobación humana77 y repetición bloqueada78.
- Voz Pages: consultó el mismo LIN-76-1 aprobado simulado; el historial mostró46s y630créditos. No se hicieron pagos ni reservas de presupuesto.
- Skills: dos previos utilizados y dos nuevos instalados; instrucciones reales de preparación y revisión incorporadas en agentes3/4.
- Pendientes principales: corte monetario por llamada y deduplicación antes del modelo en Cloud; corrección V1→V2 operativa; matriz integral restante y video individual.

Consultar docs/Entrega_y_cierre_25nov.md, tests/pruebas.csv y evidencias/v05_integracion_26nov.json para el estado detallado. Los archivos históricos conservan sus fechas. Guion reproducible de grabación: docs/guion_video_y_demo.md.

La revisión versionada v06 se publicó sobre el workflow vigente; conserva fuentes y aprobación humana. El export v06 es inactivo al importar.44pruebas locales; ensayo integral nuevo pendiente. Ver docs/Workflow_v06.md.

Alternativa con API propia: docs/Proxy_OpenAI_CANDIDATO.md. Proxy protegido publicado; evaluación manual123 correcta con11 llamadas conciliadas y revisión V1→V2. La prueba136 verificó corte por cota y duplicados en un lote de3peticiones. Versión nativa v07 publicada; falta nueva entrada Telegram y pruebas de carga amplias. Ver evidencias/v07_integracion_27nov.json.
