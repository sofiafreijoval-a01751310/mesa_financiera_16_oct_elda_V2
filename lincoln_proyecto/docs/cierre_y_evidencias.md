# Estado de entrega y pendientes comprobables

Fecha de actualización: 24 nov 2026. Proyecto académico con datos sintéticos. Este módulo agrega código local, evidencia de ejecución y documentación. No afirmar cierre100% mientras falten pruebas vivas y publicación.

## Evidencia disponible

- Base consistente:19distribuidores,2000unidades,MXN5millones,76registros mercado.
- Respaldo n8n28nodos sanitizado e inactivo, con25pruebas JavaScript del código exportado.
- Nuevos controles y loops:29pruebas Python, incluyendo concurrencia, dedup durable y presupuesto.
- Skill nuevo validado e instalado; forward-test independiente sobre dos casos más fuente insuficiente.
- Tres propuestas locales correctas y un error de fuente, trazas JSON/JSONL.
- Prueba aislada nativa n8n (ejecución50) con PASS, tres cargas de skills, V1/V2 y recuperación acotada. Adicionalmente, la ejecución53 completó cuatro agentes, lecturas directas y revisión determinista en la copia v04, sin publicarla.
- Skills previos de costos y VizData realmente utilizados.
- Escenarios de costos base/alto, por etapa y a100/1000/10000; consumo histórico completo desconocido; el panel Gateway mostró USD0.16 agregados del workflow el24/nov/2026.
- Panel estático sanitizado y despliegue Pages confirmado por GitHub Actions.
- Fallo deliberado de datos bloqueó la publicación; corrección restaurada. Ver evidencias/pages_despliegue.json.
- La usuaria confirmó que el token Telegram compartido anteriormente ya fue invalidado.

## No confundir evidencia histórica y actual

Las capturas anteriores muestran Telegram con decisiones simuladas y ElevenLabs con consulta exitosa. El respaldo README_Respaldo_v03 documenta esas pruebas históricas. La consulta actual verificó la copia v04 por entrada manual y el panel Gateway (saldo USD1.46); no volvió a medir los canales Telegram/voz ni el cargo exacto por request. Los nuevos LIN-101..104 son fixtures locales y no acreditan tres casos integrales vivos de cinco agentes.

## Para cerrar la rúbrica

1. El camino de revisión ya está conectado y probado en la copia v04, ejecución53. Faltan deduplicación compartida, reserva monetaria por llamada y pruebas simultáneas. Ver docs/control_concurrencia_n8n.md. Completar cuatro casos por los canales requeridos.
2. La copia v04 sanitizada está disponible y el respaldo privado se actualizó. Obtener artefactos ElevenLabs sin secretos. Revalidar consulta por voz y segunda interacción de negocio desde Pages.
3. Pages y sus tres KPI ya están implementados y desplegados. Falta la revisión interactiva a 390/1366 px, teclado, voz desde Pages y dominio permitido del widget. Consentimiento y alternativa Telegram están implementados; aún no se acreditan como prueba viva.
4. Se observó un agregado Gateway de USD0.16 y saldo USD1.46; falta desglose por etapa/solicitud, voz y desarrollo completo. No repartir el agregado entre casos como si fueran cargos individuales.
5. Despliegue inicial confirmado y fallo deliberado bloqueado: ver evidencias/pages_despliegue.json, que también registra la recuperación. Conservar las URLs de Actions; no sustituirlas por resultados locales.
6. Grabar video5-8min y realizar demo12min según guía. Solo Sofía puede aportar su voz/presentación personal y entregar en Canvas.

La matriz P01-P14 debe completarse desde el texto oficial, sin inventar nombres o resultados para pruebas pendientes. El informe técnico adjunto documenta alcance y riesgos actuales; actualizar versión final con enlaces y evidencias de esos pasos.

Última prueba viva: LIN-53-1, fecha de evento ficticio20/dic/2026, apoyo200000 + aportación200000, saldo proyectado450000, PENDIENTE_APROBACION y sin modificación de presupuesto. Detalle en evidencias/n8n_gateway_24nov.json.
