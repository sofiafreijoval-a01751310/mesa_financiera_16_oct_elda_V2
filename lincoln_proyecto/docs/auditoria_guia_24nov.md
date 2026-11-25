# Auditoría de entregables Lincoln — 24 de noviembre de 2026

## Dictamen

El proyecto todavía no cubre absolutamente todo. La ejecución53 acredita un caso completo con cuatro agentes y revisión por entrada manual; no acredita aprobación/notificación por Telegram, tres casos completos medidos, voz desde Pages ni protección monetaria y de duplicados antes de las llamadas.

Guía revisada: **Proyecto_final_individual_AI_Tools_Guia_del_estudiante(1).pdf**, 16 páginas, consigna30/oct/2026. SHA256: `7f2467bfc4e0bf85ad3ec05bcf421dfb53a13503c15b02903caa51ce184a8c0d`.
Estado del código auditado: commit `b999c7a4b8ffd2c9572de5158b1e0f08432ce535`. Esta auditoría compara archivos y evidencia disponible; no presenta como repetidas hoy las pruebas históricas de voz o Telegram.

## Skills: qué ya se hizo y qué falta

- **cotizar-tokens-ia** sí se utilizó: cinco tokenizaciones y cinco cotizaciones, con referencias y hashes en evidencias/cotizar_tokens_ia_ejecucion.json.
- **vizdata** sí se utilizó: instrucciones y referencias leídas, brief, selección de gráfica, auditoría y salida visual; ver evidencias/vizdata_ejecucion.json.
- **revisar-apoyo-lincoln1.0.1** ya fue creado, instalado y ejecutado en casos locales. Su calidad/loop se mostró también en una prueba n8n aislada. No falta crearlo por primera vez.
- La guía(p7) exige dos skills específicos, uno de negocio y otro de calidad/seguridad, cargados y utilizados en el proceso. El uso de dos recursos generales como apoyo al desarrollo no acredita por sí solo ese requisito operativo.
- Acción recomendada: completar un skill de negocio **preparar-apoyo-lincoln**, conservar el revisor específico y conectar ambos al flujo real mediante carga trazable de instrucciones. Añadir caso válido/rechazado, versión, recursos y autoevaluación. Esta recomendación no afirma que ese cuarto skill ya exista.

## Hallazgos que cambian el plan

1. Telegram acepta solicitudes por texto y comandos de decisión, pero el validador actual rechaza /estado como comando desconocido. Falta consulta de folio en ese canal.
2. Las salidas de agentes no incorporan de forma uniforme duración y referencia a consumo, requeridas en p3.
3. La muestra exigida es tres casos completos distintos y uno de error/rechazo, no tres fixtures locales. Solo53 está acreditado como completo manual.
4. La plantilla de consumo real está vacía y no tiene todos los campos exigidos. USD0.16 es un agregado Gateway, no costos individuales por llamada.
5. El export de voz y la configuración reproducible de ElevenLabs no están incluidos; el propio manual reconoce esa ausencia.
6. La matriz actual P01-P14 conserva estados parciales, pero le faltan columnas obligatorias de fecha, versión, caso, entrada, esperado y obtenido.
7. El informe tiene ocho páginas de cuerpo y una de referencias: cubre extensión, pero aún debe completar reflexión individual y resultados finales.
8. La introducción menciona tarea programada. No se encontró una propia de Lincoln en el workflow revisado. La guía no fija frecuencia; no inventar obligación de cron cada cinco minutos.

## Orden de trabajo

1. Completar skill de negocio y carga de ambos skills específicos; enlazar sus instrucciones al orquestador/agentes y registrar hashes/versiones.
2. Conectar loops de calidad y seguridad/costo, deduplicación persistente, consulta /estado y contrato completo. Justificar límites mayores de tres iteraciones.
3. Verificar la versión operativa con un solo Telegram Trigger; probar caso, aprobación, rechazo y vencimiento con el mismo folio.
4. Completar muestra de tres casos más error, con trazas sanitizadas de los cinco roles y registro por llamada.
5. Exportar/recrear voz y probar desde Pages consulta de folio y segunda interacción; revisar 390/1366px, teclado y fallas de micrófono/servicio.
6. Conciliar costos y comparar optimización antes/después; actualizar matriz, manual, reflexión e índice.
7. Reemitir ZIP del commit final y preparar video/defensa. El paquete actual continúa siendo REVISION.

La intervención personal de Sofía será necesaria para validar su reflexión, usar micrófono cuando corresponda y grabar video/defender el proyecto. No se requiere compartir claves en el chat para realizar esta auditoría.

## Revisión completa por requisito

La columna estado distingue documentación, prueba local, evidencia histórica y operación comprobada. La matriz P01-P14 sigue siendo la de pruebas del sistema; la tabla siguiente audita entregables y no la sustituye.

| ID | Requisito / páginas | Estado | Acción pendiente |
|---|---|---|---|
| E01 | Caso empresarial y tres KPI (p.2) | DOCUMENTADO | Consolidar caso en una página con fórmulas, unidad, periodo y fuente; diferenciar meta de resultado medido |
| E02 | Mapa y cinco roles (p.2-3) | PARCIAL | Diagrama incluido en esta auditoría e instrucciones en export; entregar traza completa sanitizada, no solo resumen |
| E03 | Contrato completo (p.3) | INCOMPLETO | Agregar duración y referencia al registro de consumo a salidas; preservar mismo caso_id |
| E04 | Telegram inicio y consulta (p.4) | PARCIAL | Implementar /estado FOLIO o equivalente; verificar respuesta por Telegram de la versión vigente |
| E05 | Aprobación rechazo vencimiento (p.4,8,12) | LOCAL_E_HISTORICO | Repetir aprobar/rechazar/vencer por canal real, dueño y versión; comprobar registro y notificación |
| E06 | Producción y receptor único (p.4) | PENDIENTE_VERSION_V04 | Validar y publicar versión final sin dos receptores del mismo bot; documentar disponibilidad |
| E07 | Persistencia y duplicados (p.4,8) | PARCIAL | Deduplicación compartida antes del modelo y prueba simultánea; caso/evento idempotentes |
| E08 | Export n8n reproducible (p.4,13) | PARCIAL | Consolidar guía v04 y tablas/muestras; añadir export de consulta de voz |
| E09 | HTML VizData y export sanitizado (p.5-6) | IMPLEMENTADO_CON_QA_PENDIENTE | Verificar datos finales del registro y actualización export->commit->Actions->Pages |
| E10 | Accesibilidad y estados UI (p.5,12) | PENDIENTE_PRUEBA_INTERACTIVA | Probar 390/1366 px, teclado, foco, contraste y estados de carga/vacío/error/desactualizado |
| E11 | Voz operativa desde Pages (p.5) | HISTORICO_Y_CONFIGURACION_PARCIAL | Consultar folio y otra interacción de negocio desde Pages; comprobar herramienta y registro; micrófono denegado/servicio caído |
| E12 | Configuración ElevenLabs exportable (p.5,13) | INCOMPLETO | Entregar configuración/exports sin secretos: propósito, español, voz, saludo, conocimiento, derivación, dominios y herramienta |
| E13 | GitHub Actions Pages y bloqueo (p.6) | VERIFICADO | Conservar enlaces y relacionarlos con commit final; no confundir con QA de voz |
| E14 | Dos skills anteriores y uno nuevo pedidos por Sofía (p.Petición de Sofía;7) | USO_PREVIO_Y_LOCAL_ACREDITADO | Mantener evidencia y actualizar referencias; el número de carpetas no acredita integración operativa |
| E15 | Dos skills específicos negocio y calidad (p.7) | INCOMPLETO_EN_OPERACION | Completar skill de preparación de apoyo Lincoln y cargar ambos en el proceso; ejemplos válido/rechazado, versión, recursos y traza |
| E16 | Dos loops operativos y reutilización (p.7) | PARCIAL | Integrar calidad y seguridad/costo al camino operativo; demostrar V1 fallida->V2 válida con mismo folio/costo adicional y segundo caso |
| E17 | Autoevaluación skills y loops (p.7) | LOCAL_DOCUMENTADA | Actualizar tras integración/skill específico nuevo; cada uno>=16 y ningún aspecto<3; justificar límites>3iteraciones |
| E18 | Guardrails en endpoint real (p.8,12) | PARCIAL | Ataque de inyección/extracción, usuario no autorizado, herramienta prohibida, caída/cuota en flujo real; evidencia sin fuga |
| E19 | Presupuesto previo y corte (p.8,12) | PENDIENTE_GATEWAY | Reservar margen y detener nuevas llamadas al agotar presupuesto; el campo0.25 no acredita corte; la guía no fija ese monto |
| E20 | Costos por llamada/etapa/caso (p.9-10) | INCOMPLETO | Llenar costos.csv/xlsx con fecha/caso/llamada/agente/proveedor/modelo/tokens/voz/unidad/tarifa/costo/moneda/estado/reintento/origen; estimar solo cuando se declare |
| E21 | Muestra mínima y conciliación (p.10) | INCOMPLETO | Tres casos completos distintos y uno error/rechazo; voz al mismo registro; reconciliar cargos, fallas, caché y razonamiento sin duplicarlos |
| E22 | Escenarios y optimización (p.10) | ESTIMACIONES_DISPONIBLES | Actualizar mezcla de rutas/voz/cuotas con mediciones; comparar antes/después costo y calidad; separar desarrollo e infraestructura |
| E23 | Matriz P01-P14 (p.12) | PARCIAL | Agregar fecha, versión, caso_id, entrada, esperado, obtenido, aprobado/fallido y evidencia; completar las14 pruebas integradas |
| E24 | Paquete informe y manual (p.11,13) | REVISION_REPRODUCIBLE | Reemitir final tras cerrar brechas, nombre Apellido_Nombre_AI_Tools_ProyectoFinal.zip; índice/enlaces, licencias, dependencias y manual actualizado |
| E25 | Reflexión individual (p.15) | NO_IDENTIFICADA_COMO_SECCION_COMPLETA | Agregar reflexión propia que responda las seis preguntas de la guía sin inventar experiencia personal |
| E26 | Video y defensa (p.13,15) | SIN_EVIDENCIA_DISPONIBLE | Sofía:video5-8min y defensa<=12min; demostrar folio, agentes, aprobación, voz, inyección, loop y costos |
| E27 | Tarea programada mencionada (p.1) | NO_ACREDITADA_EN_LINCOLN | Definir y demostrar tarea programada útil del proyecto; la guía no especifica frecuencia, no atribuirle un cron obligatorio de5min |

Detalle con evidencia y prioridad: [auditoria_entregables.csv](../tests/auditoria_entregables.csv).
