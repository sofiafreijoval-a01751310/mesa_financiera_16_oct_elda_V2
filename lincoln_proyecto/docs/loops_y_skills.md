# Dos skills previos, uno nuevo y dos loops

| Skill | Procedencia | Ejecución/uso comprobado |
|---|---|---|
| cotizar-tokens-ia | Personal existente | Tokenizador y cotizador original; resultados y hashes en evidencias/cotizar_tokens_ia_ejecucion.json |
| vizdata | Archivos originales adjuntos por Sofía | Brief, auditoría de fuente/denominador, selección barras vs donut, auditor --strict, gráfica y tabla equivalente |
| revisar-apoyo-lincoln | Nuevo, versión funcional1.0.1 | Creado, validado e instalado; ejecutado en tres casos válidos y un caso de fuente insuficiente |

La invocación no se demuestra mencionando un nombre en un prompt. Se conservan instrucciones leídas, hashes, entradas y salidas. Los archivos del skill nuevo están disponibles también como copia reproducible en skills/revisar-apoyo-lincoln; la instalación personal es independiente. VizData aplica al diseño y la auditoría, no requiere ejecutar un modelo. El tokenizador usa o200k_base para texto plano, con el límite declarado en el reporte de costos.

## Loop 1: proponer, revisar, corregir

Recurso: skills/revisar-apoyo-lincoln/scripts/revisar.py . Máximo tres revisiones y diez segundos. V1 parte con propuesta vacía y falla revisión; la corrección usa solo inversión/saldo originales; V2 vuelve a revisar y converge. Nunca cambia fuente, inversión ni distribuidor. El apoyo es min(50% inversión, saldo), inversión ajustada dos veces apoyo y aportación igual a apoyo. Si reduce alcance, marca aceptación requerida. No aprueba ni paga. Registrar caso, versión local, iteración, dictamen y hashes de instrucciones/script/contrato. La versión local del loop no sustituye version_propuesta de n8n hasta integrar explícitamente el contrato.

Casos de demostración, no casos vivos:
- LIN-101-1 Monterrey: apoyo200000, aportación200000, evento400000, saldo450000.
- LIN-102-1 Chiapas: apoyo62500, aportación62500, evento125000, saldo0; requiere aceptar alcance.
- LIN-103-1 Guadalajara: apoyo250000, aportación250000, evento500000, saldo200000.
- LIN-104-1: falta versión de fuente; se detiene en una revisión y escala sin inventarla.

## Loop 2: recuperar consulta ante error transitorio

Recurso: src/loop_servicio.py . Máximo tres intentos/diez segundos; reserva costo ANTES de cada intento; reintenta únicamente TimeoutError/ConnectionError. Detiene ante esquema/folio inválido, duplicado o límite de costo. La demostración provoca dos timeouts locales y éxito al tercero, sin servicio remoto. Un adaptador HTTP debe imponer timeout de transporte usando el tiempo restante: el reloj Python no cancela una función bloqueada. No afirmar un deadline de red duro sin esa conexión.

Pruebas y trazas están en evidencias/. Costo API de loops locales USD0; costo operativo de infraestructura no medido. La implementación se entrega separada del respaldo v03: no está activada automáticamente en n8n Cloud. Para conectar: entradas de Telegram -> autenticar -> dedup persistente -> inicializar -> reserva por llamada -> orquestador; revisor después de propuesta -> aceptación de alcance -> aprobación humana; consulta de voz -> Header Auth -> esquema -> lectura -> proyección segura.

## Prueba nativa separada en n8n

Se importó y ejecutó Lincoln | Prueba aislada de skills y loops v1 (4nodos, manual, sin credenciales ni publicación). Ejecución50:PASS. Leyó las tres instrucciones embebidas, procesó LIN-50-1..4 con V1/V2, escaló fuente sin versión y recuperó el transporte de prueba al tercer intento con USD0 de API. Export reproducible en exports/Lincoln_Prueba_Aislada_Skills_Loops.json y observación sanitizada en evidencias/n8n_prueba_aislada_observada.json. La carga nativa no vuelve a ejecutar el tokenizador ni el auditor VizData:su uso real se conserva en los artefactos previos. El revisor está adaptado a JS para esta demostración. No afirmar que la prueba manual ya protege el bot operativo, factura consumos reales o deduplica entre workers.


## Actualización 25/nov: preparación e integración candidata
Se creó preparar-apoyo-lincoln v1.0.0. Ver docs/Entrega_y_cierre_25nov.md y src/preparar_workflow_v05.py. Los dos SKILL.md se leen de archivos al construir el export. v05 completó agentes 1–4 y revisión determinista en LIN-56-1 el 26/nov; quedó PENDIENTE_APROBACION. El cierre del loop monetario sigue pendiente en Cloud. La tarea diaria 09h México quedó publicada y probada manualmente: LIN-53-1 vencido y repetición con cero actualizaciones. Falta observar el primer disparo horario. Ver evidencias/v05_integracion_26nov.json.
