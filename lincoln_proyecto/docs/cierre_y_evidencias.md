# Estado de entrega y evidencia vigente

Actualización26/nov/2026. Datos sintéticos; versión de revisión, no cierre total.

## Evidencia integral disponible

| Componente | Verificación |
|---|---|
| Cuatro agentes | Monterrey56 y Mérida69 por entrada manual; Chiapas72/76 reprocesando un evento real de Telegram, con fuentes y revisión determinista |
| Telegram | /start61; consulta64/73; bloqueo de aprobación sin aceptar ajuste74; vencimiento75; aprobación humana77 de LIN-76-1; repetición78 sin nueva escritura |
| Voz desde Pages | v5 consultó LIN-76-1 y sus cifras; herramienta exitosa2.3s; llamada46s; audio confirmado por Sofía |
| Skills | Instrucciones reales en agentes3/4; previos de costos y VizData utilizados; scripts y trazas reproducibles |
| Loops | Calidad y recuperación ejecutables locales; prueba nativa aislada50. Esto no acredita integración completa de ambos loops en el bot |
| Tarea programada | Vencimientos diarios09h México publicados; vencimiento condicional y repetición probados manualmente; primer disparo horario aún no observado |
| Pages | Datos sintéticos con fecha y aviso de antigüedad; diseño390/1366, filtros, simulador, consentimiento y teclado parcial verificados |
| Costos | Gateway agregado y saldos observados, sin repartirlos entre casos. Voz:630créditos=511plataforma+119LLM; panel LLM USD0.00892, sin factura conciliada |

## Pendientes de la rúbrica

1. Reserva y corte monetario antes de cada llamada Gateway, incluyendo invocaciones internas; deduplicación durable antes del modelo y prueba concurrente.
2. Corrección operativa V1→V2 del mismo caso y comparación de costo incremental; los fixtures locales no la sustituyen.
3. Entrada completa nueva por webhook tras la corrección (las positivas72/76 son reprocesamientos), pruebas restantes de permisos, fallas y denegación del micrófono.
4. Conciliación de costos por request y factura; no confundir créditos del panel con un precio monetario total.
5. Reflexión propia integrada; quedan video5–8min, demostración≤12min y entrega individual en Canvas.

Rutas de detalle: tests/pruebas.csv; evidencias/v05_integracion_26nov.json; evidencias/elevenlabs_26nov.json; evidencias/pages_qa_26nov.json; docs/control_concurrencia_n8n.md; docs/Entrega_y_cierre_25nov.md. Las versiones históricas siguen fechadas; esta página es el índice vigente.

El token Telegram compartido antes fue invalidado según Sofía. No incluir capturas completas del navegador, secretos ni IDs privados en el video, repositorio o ZIP.

## Actualización27/nov: integración OpenAI publicada

123 completó agentes1–4, transferencia desde observaciones reales y revisión determinista V1→V2; registro21 PENDIENTE_APROBACION.11llamadas conciliadas,30414tokens entrada+4132salida, USD0.007041300 a tarifa estándar (sin voz/infraestructura/factura).136 pasó lote nativo de3peticiones: corte LIMITE_COSTO previo al proveedor, una admisión y un duplicado bloqueado. Las11reservas sintéticas de ese fixture no son cargos y están excluidas del CSV de consumo.

La ruta v07 está publicada; Gateway anterior despublicado para evitar dos webhooks del bot. Pendiente nueva entrada de Sofía desde Telegram, matriz negativa restante, carga amplia, factura total y video personal. Evidencias: v07_integracion_27nov.json, guard_negativo_27nov.json y costos/consumo_proxy_27nov.csv. La documentación histórica mantiene su fecha y alcance.
