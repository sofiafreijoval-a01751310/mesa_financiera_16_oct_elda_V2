# Entrega Lincoln: cierre del 26 de noviembre de 2026

Guía del estudiante, versión 30/oct/2026, sección de entregables. No entregar esta lista como sustituto del informe.

| Entregable | Qué contiene | Estado |
|---|---|---|
| Informe técnico y de negocio | 8–12 páginas de cuerpo; arquitectura, decisiones, controles, resultados, reflexión y referencias; anexos aparte | PDF de revisión de10páginas (9de cuerpo y1de referencias); actualizar con integración y pruebas finales |
| Repositorio GitHub | Código, instrucciones de reproducción, dependencias, datos sintéticos y versiones | Repositorio existente; cambios nuevos sujetos a Actions |
| ZIP del mismo commit | Copia del repositorio, informe, manifiesto; SKILL.md, scripts, referencias y ejemplos de todos los skills utilizados | Se genera en Actions; sustituir cualquier ZIP antiguo |
| Enlaces operativos | GitHub Pages, Actions correcto y bloqueo deliberado, bot y acceso sin secretos | Enlaces disponibles; faltan pruebas finales de canales |
| Exports de n8n | Roles, contratos, prompts, skills, loops y configuración sin credenciales | v05 publicado el 26/nov; caso LIN-56-1 correcto; tarea diaria publicada y transición/idempotencia comprobadas. Exports inactivos al importar por seguridad |
| Configuración/export de ElevenLabs | Voz, idioma, saludo, herramientas, conocimiento, dominios y recreación; pruebas | Configuración sanitizada y recreación agregadas; webhook positivo/negativo y chat con herramientas reales probados; llamada audible v5 desde Pages verificada (LIN-76-1,46s) |
| Costos y pruebas | CSV/XLSX, tarifas, proyecciones, matriz de casos, evidencias, diccionario y muestra | Existen archivos; completar medidas por llamada y casos exigidos |
| Video y defensa individual | Video de 5–8 minutos; demo de hasta 12 minutos; declaración de IA y licencias | Requiere grabación de Sofía |

No se exige una presentación como archivo independiente. Puede utilizarse como apoyo visual de la defensa; no reemplaza video ni informe.

## Dos skills específicos

`preparar-apoyo-lincoln` v1.0.0: negocio, validación de fuentes y propuesta 50/50. Creado, instalado y probado con dos casos válidos y uno rechazado. Incluye contrato, recursos y CLI sin APIs.

`revisar-apoyo-lincoln` v1.0.1: revisión de calidad y seguridad. Su uso local e integración aislada ya tienen evidencia. El constructor `src/preparar_workflow_v05.py` lee ambos SKILL.md y embebe las instrucciones y sus SHA256 en agentes 3 y 4. Un nodo registra la carga en el caso. Ejecución nativa 56 completó agentes 1–4 y revisión determinista; LIN-56-1 quedó PENDIENTE_APROBACION. El revisor devolvió su hash; el proponente omitió esa metadata. El registro nuevo conserva configuración de los dos archivos sin atribuir al modelo una verificación no observada. Ejecución 55 detectó error de esquema por skills_cargados; se agregó metadata opcional y se conservó additionalProperties:false. Ver evidencias/v05_integracion_26nov.json.

`cotizar-tokens-ia` y `vizdata` conservan sus evidencias auxiliares de uso. No se presentan como reemplazos de los dos skills específicos. Revisar también el recurso pendiente del tokenizador señalado en la auditoría.

## Dos loops: existencia frente a acreditación

1. Calidad: evaluar cálculo, diagnosticar diferencias, corregir y volver a validar; máximo tres vueltas y diez segundos en revisión determinista. Pruebas locales V1 errónea → V2 corregida. Una ejecución integral v04, folio LIN-53-1, superó la revisión en primera vuelta. Falta demostrar V1→V2 dentro del flujo operativo vigente y registrar costo adicional.
2. Seguridad y costo: autorizar, admitir presupuesto, reservar, ejecutar, registrar/reconciliar consumo y continuar o detener. Implementación SQLite y pruebas locales disponibles, incluida concurrencia. Falta integrar y acreditar el bloqueo monetario y la deduplicación persistente antes del modelo en n8n. `limite_costo_usd:0.25` por sí solo no corta gasto de Gateway.

No afirmar que ambos loops cumplen integralmente mientras el segundo siga local.

## Tarea programada publicada y probada

`exports/Lincoln_Vencimientos_Programados_PUBLICO.json`: Schedule Trigger diario a las 09:00 America/Mexico_City (`0 9 * * *`). Publicado el 26/nov/2026 como Lincoln | Vencimientos diarios 09h. Se eligió una ejecución diaria para cuidar la cuota de n8n; la guía no fija frecuencia. El export permanece inactivo al importarlo y exige asociar la tabla de casos.

Prueba nativa: LIN-53-1, fila 6, versión 1 pasó de PENDIENTE_APROBACION a VENCIDO, ID VENCIMIENTO:LIN-53-1:1. La repetición con la misma instantánea produjo cero filas actualizadas. La comparación condicional incluye ID, folio, versión, estado pendiente, decisión vacía, vencimiento y propuesta original idénticos. Solo casos simulados vencidos. No utiliza modelos ni Telegram ni modifica presupuestos. Configuración nativa: ejecución v1, zona México y acceso MCP deshabilitado. Se probó manualmente la lógica; el primer disparo horario queda pendiente de observación.

## Orden de cierre

1. v05 ya publicado con Telegram habilitado; /start verificado desde cuenta autorizada, ejecución61, 1.996s, sin modelos.
2. Tarea diaria ya publicada; conservar prueba de transición e idempotencia y verificar posteriormente el primer disparo horario.
3. Consulta `/estado FOLIO VERSION` publicada y probada localmente; prueba nativa62 bloqueó LIN-56-1 duplicado sin escrituras ni modelos. Consulta positiva LIN-34-1 respondió APROBADO_SIMULADO según respuesta compartida por Sofía. Integrar guardián/deduplicación; completar matriz: Monterrey56, Mérida69 y Chiapas72 pasaron revisión; Chiapas70 falló contrato y72 reprocesó el mismo mensaje con corrección. Faltan cierre monetario, V1→V2 del loop operativo ; decisión humana positiva ya confirmada en77 y repetición bloqueada en78.
4. Configuración y recreación de ElevenLabs agregadas, pruebas reales de texto/webhook y rechazo de inyección correctas. Diseño390/1366, filtros y teclado parcial verificados. Llamada audible final verificada; falta probar micrófono denegado.
5. Completar costos medidos y estimados separados, informe y manifiesto del mismo commit; reflexión personal ya integrada.
6. Sofía graba video y realiza defensa; descargar ZIP final únicamente después de Actions correcto y comprobar que coincide con el commit del informe.

## Intervención concreta

`/start` pasó. `/estado LIN-34-1 1` respondió correctamente según la respuesta aportada por Sofía; LIN-56-1 pertenece a prueba manual y tiene dos inserciones, bloqueadas correctamente. Chiapas72 ya tuvo respuesta real de Telegram; ejecución74 bloqueó aprobar sin ACEPTAR_AJUSTE (aplicar:false, sin escritura ni modelo). Ejecución77 aprobó LIN-76-1 con ACEPTAR_AJUSTE;78 bloqueó la repetición sin modelo ni segunda escritura. Acceso ElevenLabs recuperado, configuración publicada y pruebas de herramienta/texto correctas. Sofía confirmó audio audible; el historial nativo acredita consulta LIN-76-1,46s,630créditos y USD0.00892 del LLM (desgloses no aditivos). Reflexión individual integrada con su confirmación; la grabación corresponde a Sofía. No hace falta volver a compartir credenciales ni importar otra copia del workflow.


## Revisión versionada publicada

El26/nov se publicó Lincoln v06 revisión versionada en el workflow operativo existente: traza por versión, persistencia de la versión final revisada y comando de aceptación completo.44pruebas locales pasan. No se ejecutó una evaluación nueva después de publicar; ese ensayo sigue pendiente. Detalle: docs/Workflow_v06.md. La reflexión individual ya fue integrada y confirmada por Sofía.

## Actualización del27/nov: candidato OpenAI

La ejecución manual123 completó los cuatro especialistas vía proxy protegido, con transferencia reconstruida desde observaciones reales. El loop determinista pasó de V1 con indicadores faltantes a V2 correcta y guardó registro21 PENDIENTE_APROBACION:200000MXN Lincoln,200000distribuidor, saldo450000. Sin aprobación humana ni cambios de presupuesto. Sus11 llamadas quedaron CONCILIADO:30414tokens entrada,4132salida, USD0.007041300 a tarifa estándar. No incluye infraestructura/voz/factura. Ver evidencias/v07_integracion_27nov.json y costos/consumo_proxy_27nov.csv.

Esto acredita V1→V2 dentro del candidato manual real, no un evento nuevo de Telegram. El bot publicado sigue Gateway; faltan concurrencia CAS nativa, bloqueo monetario negativo nativo, migración controlada y nueva entrada Telegram. Las secciones anteriores conservan sus observaciones históricas.
