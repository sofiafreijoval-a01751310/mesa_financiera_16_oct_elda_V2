# Índice de entrega - Sofía Freijo Valdovinos

Proyecto individual AI Tools: Lincoln | Apoyos a Distribuidores. Datos sintéticos; uso potencial en el trabajo de Ford sujeto a autorización y validación. Corte27/nov/2026. Esta es una versión documental para entrega con limitaciones declaradas; no una certificación de100% de la rúbrica.

## Archivos y enlaces que se entregan

1. **Informe_Lincoln.pdf**:10páginas,9de cuerpo y1de referencias; problema, arquitectura, datos, skills/loops, seguridad, costos, resultados y reflexión individual.
2. **Freijo_Valdovinos_Sofia_AI_Tools_ProyectoFinal.zip**:fuentes del mismo commit que identifica MANIFIESTO.json, informe, esta guía, exports sanitizados, skills, datos, pruebas y costos. El video aún no está incluido.
3. **Guia_Entrega_y_Grabacion.pdf**:índice práctico y guion; es un apoyo, no sustituye el informe ni el video.
4. **Costos y evidencias**:costos/costos.csv, resumen_por_caso.csv, costos_por_etapa.csv, consumo_proxy_27nov.csv, voz_observada_26nov.csv; tests/pruebas.csv y evidencias/. Incluyen datos desconocidos explícitos y estimaciones separadas.
5. **GitHub**:https://github.com/sofiafreijoval-a01751310/mesa_financiera_16_oct_elda_V2 . Rama main; el commit de entrega está en el manifiesto. Leer primero lincoln_proyecto/README.md.
6. **Pages**:https://sofiafreijoval-a01751310.github.io/mesa_financiera_16_oct_elda_V2/ . Datos estáticos con fecha; no tiempo real.
7. **Actions**:https://github.com/sofiafreijoval-a01751310/mesa_financiera_16_oct_elda_V2/actions . La ejecución de este paquete se registra en el manifiesto. Bloqueo deliberado y recuperación documentados con identificadores completos en evidencias/pages_despliegue.json; no usar solo una captura de Settings.
8. **Telegram**:@lincoln_apoyo_distribuidores_bot. Acceso restringido:la docente solicita autorización a Sofía por el canal privado del curso. No compartir token ni publicar identidades.
9. **Video personal5–8minutos y demo hasta12minutos**:pendientes de grabación/defensa de Sofía. Agregar su enlace o archivo al envío según la indicación del curso. No inventar un enlace ni confundir el guion con el video.

La guía no exige una presentación como archivo independiente. No hace falta crear otro skill: cotizar-tokens-ia y VizData se reutilizaron; preparar-apoyo-lincoln y revisar-apoyo-lincoln están creados, versionados y usados. El ZIP incluye sus SKILL.md y recursos disponibles.

## Exports actuales

- Bot:exports/Lincoln_Apoyos_v07_CANDIDATO_PUBLICO.json.
- Proxy:exports/Lincoln_Proxy_OpenAI_CANDIDATO_PUBLICO.json.
- Voz:exports/Lincoln_Consulta_Voz_PUBLICO.json.
- Cron:exports/Lincoln_Vencimientos_Programados_PUBLICO.json.
- ElevenLabs:exports/ElevenLabs_Lincoln_CONFIG_PUBLICA.json y docs/elevenlabs/RECREAR.md.

Los nombres CANDIDATO son antecedentes de archivo; las versiones nativas v07/proxy/voz están publicadas. Los exports se conservan inactivos al importar, sin credenciales. Manual vigente:docs/manual_importacion.md. Los v03-v06 son históricos, no importarlos por error como ruta actual.

## Lo acreditado

-140 fue una entrada nueva Telegram:75.68s,cuatro especialistas, registro22, V1 incompleta y V2 válida; respuesta confirmada por Sofía. Quedó PENDIENTE_APROBACION, no aprobado.
-123 pasó manualmente con11llamadas conciliadas:30414tokens entrada,4132salida, USD0.007041300 a tarifa estándar; excluye voz/plataformas y no es factura.
-136 bloqueó una llamada por cota antes del proveedor y admitió solo una de dos solicitudes idénticas en un lote HTTP de3items. No certifica toda carga concurrente. Sus reservas de fixture son sintéticas, no consumo.
-76 fue aprobado de forma simulada mediante decisión humana77 y consultado por voz desde Pages.630créditos y46s; Sofía confirmó audio.78 bloqueó segunda decisión. No atribuir esa aprobación a140.
-Tarea09h México publicada; transición e idempotencia manuales probadas. Actions publica solo tras validación; bloqueo y recuperación históricos documentados.

## Pendientes antes de afirmar cumplimiento integral

- P01/P04:cierre humano del mismo caso recibido de nuevo; rechazo explícito en otro caso vigente. Nunca aprobar un folio vencido ni reutilizar su versión anterior.
- P05:validar respuesta real a solicitud incompleta; P06:prueba explícita de inyección por n8n; P07:acceso no autorizado en endpoint vivo; P08:timeout/caída/cuota nativos. Hay pruebas locales y algunas fallas de integración observadas, con alcance declarado.
- P13:micrófono denegado y recuperación; carga amplia de CAS; primer disparo horario observado si corresponde.
- P14:etapa/agente por request no vienen en el ledger; el CSV los deja no atribuidos. Faltan factura total, gasto de desarrollo y experimento pareado de optimización. Hay tres casos de negocio históricos con traza, pero no usage completo de todos.
- Video personal y demostración. Revisar la matriz:tener un archivo no convierte una prueba pendiente en PASS.

El proxy bloquea nuevas llamadas desde2026-12-04T00:00:00Z hasta revalidar política/modelo/tarifa y publicar la configuración revisada. Mantener n8n/ElevenLabs disponibles y con cuota durante la evaluación.

## Envío

Entregar PDF, ZIP, enlaces y video por el canal indicado en clase. El ZIP y GitHub deben corresponder al mismo commit. No enviar exports privados, claves, chats ajenos ni capturas con perfil/correo. No es necesario entregar por separado cada archivo del ZIP salvo indicación de la docente. Declaración de IA y procedencia:docs/uso_ia_y_fuentes.md. La reflexión personal fue revisada por Sofía.
