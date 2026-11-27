# Manual de importación y operación - versión de entrega27/nov/2026

## Qué corre en cada servicio

n8n Cloud recibe Telegram, ejecuta el orquestador y cuatro especialistas, conserva casos y aplica decisiones simuladas. Un workflow servidor separado protege la API OpenAI con admisión, reserva y conciliación. ElevenLabs consulta el registro de casos por una herramienta autenticada de solo lectura. GitHub Pages sirve HTML y datos sanitizados estáticos; Actions valida y publica. Pages no ejecuta n8n ni un servidor Python.

Python3.12 y Node22 son los runtimes de CI. `python3 src/run_checks.py`, desde lincoln_proyecto, ejecuta14comprobaciones sin APIs. `python3 src/run_demo.py` recrea solo una base local de demostración. Estas pruebas no activan el bot.

## Archivos actuales y orden de importación

1. `exports/Lincoln_Proxy_OpenAI_CANDIDATO_PUBLICO.json`: proxy servidor de26nodos.
2. `exports/Lincoln_Apoyos_v07_CANDIDATO_PUBLICO.json`: bot y cinco roles,42nodos. El nombre del archivo conserva CANDIDATO como antecedente; su versión nativa ya está publicada.
3. `exports/Lincoln_Consulta_Voz_PUBLICO.json`: consulta de voz de4nodos, exportada de la versión nativa publicada y sanitizada.
4. `exports/Lincoln_Vencimientos_Programados_PUBLICO.json`: vencimiento diario09h America/Mexico_City.

Crear un workflow vacío por archivo; importar sobre un grafo existente duplica nodos. Todos los exports públicos permanecen inactivos y sin credenciales. v03-v06 se conservan como antecedentes: no son el punto de entrada actual.

## Tablas privadas

Crear ventas, presupuesto, mercado y casos con los nombres de columnas de `docs/diccionario_datos.md` y datos sintéticos de `datos/`. Vincular cada marcador CONFIGURAR_TABLA con su tabla real. Mantener propuesta_json, folio, versión, estado, usuario autorizado, decisión y caducidad en el registro privado; no exportar la tabla completa a Pages.

Para el proxy crear una tabla exclusiva `lincoln_guard_ledger`, columna texto `state_json`. Inicializar una única fila con id1 y el texto:

```json
{"schema":1,"seq":0,"cases":[],"requests":[]}
```

Vincular los cuatro nodos Leer reserva, Reservar CAS, Leer conciliación y Conciliar CAS. El código exige esa única fila e identidad exacta; si no coincide se detiene. No sustituir la actualización condicional por get+insert ni reiniciar un ledger operativo para borrar gasto o duplicados. Archivar y migrar con revisión si se alcanza su capacidad.

## Tres credenciales diferentes para OpenAI

| Uso | Dónde | Qué contiene |
|---|---|---|
| OpenAI real | OpenAI controlado del proxy | API key privada del proveedor; destino fijo https://api.openai.com/v1/chat/completions |
| Autenticación del proxy | Los dos Webhook y Admitir caso en control | Header Auth: Nombre Authorization; Valor Bearer seguido de un secreto aleatorio exclusivo |
| Cliente del proxy | Los cinco OpenAI Chat Model del bot | La misma contraseña aleatoria, sin Bearer; no es la API key real |

En la credencial cliente, Base URL: `https://TU_INSTANCIA/webhook/lincoln-llm-guard/v1`. Activar encabezado personalizado `X-Lincoln-Case` con expresión `{{ $("Inicializar caso").first().json.caso_id }}`. Mantener modelo gpt-4o-mini-2024-07-18, Responses API desactivada,4096tokens de salida,90000ms y0reintentos en los cinco nodos.

Los secrets se introducen únicamente en credenciales privadas por su propietaria. No pegarlos en Telegram, HTML, JSON exportado, informe ni GitHub. Reemplazar el dominio de instancia en las URLs de admisión del bot si se importa en otra cuenta.

## Identidad y publicación del bot

Seleccionar el token privado del bot en Telegram Trigger y nodos de envío. Sustituir únicamente el usuario DEMO por la identidad autorizada en Validar entrada Telegram; mantener chat privado y rechazo de bots. No ampliar a todos los usuarios para hacer una demostración.

Publicar primero el proxy autenticado. Ejecutar una prueba manual sintética y comprobar reserva, usage y estado de negocio. Para activar Telegram: despublicar el receptor anterior antes de publicar v07. Solo puede existir un webhook/receptor por bot. Una publicación correcta muestra Published y confirma escucha de eventos.

Operación comprobada:123 manual pasó cuatro especialistas y V1→V2;136 bloqueó una llamada por cota y un duplicado en el mismo lote;140 recibió una solicitud nueva de Sofía y entregó su respuesta en75.68s. El retraso no significa necesariamente falta de recepción. No reenviar hasta revisar Executions y el estado del caso.

## Repetir un caso

Enviar una vez al bot: “Lincoln Monterrey solicita apoyo para una exhibición de Navigator el20 de diciembre de2026. Inversión total400000MXN antes de IVA.80asistentes de35a60años, NSE A/A+/B+. Objetivo: generar prospectos y pruebas de manejo”. Cambiar la fecha por una futura si se evalúa después de ese evento.

Resultado esperado: folio nuevo, cuatro especialistas, revisión válida,200000MXN de Lincoln y200000del distribuidor, saldo proyectado450000, PENDIENTE_APROBACION. La versión puede aumentar si el control corrige el contrato; usar la versión realmente devuelta.

Consultar `/estado FOLIO VERSION`. Aprobar solo después de revisar con `/aprobar FOLIO VERSION` o rechazar con `/rechazar FOLIO VERSION`. Si hubo alcance reducido, añadir ACEPTAR_AJUSTE. Caduca a los30minutos; nunca reabrir una propuesta vencida ni usar comandos históricos como si fueran vigentes. Decisiones simuladas, sin pagos ni cambios de presupuesto.

## Voz, cron y panel

En el webhook de voz conservar POST, ruta lincoln-voice-cases-v1 y Header Auth separado, nombre X-Lincoln-Key. Copiar el mismo secreto privado a la herramienta ElevenLabs. Su cuerpo admite exclusivamente caso_id y version; la consulta no aprueba ni escribe. Recrear el agente con `exports/ElevenLabs_Lincoln_CONFIG_PUBLICA.json`, `docs/elevenlabs/RECREAR.md` y prompt_sistema.txt. La configuración es documentación sanitizada, no una importación universal garantizada.

Vincular el cron a la tabla de casos, zona America/Mexico_City y09h diarias. Se probaron transición e idempotencia manuales; no se atribuye un disparo horario aún no observado.

Para actualizar Pages, usar la proyección por lista permitida de `src/exportar_panel.py`, revisar que no contenga usuarios ni conversaciones, hacer commit y esperar Actions. Es una exportación manual reproducible; el panel no es tiempo real. Mantener consentimiento y alternativa Telegram antes de cargar el widget.

## Límites, parada y fallas

Proxy: USD0.25/caso de tokens estándar,25llamadas,6minutos y100casos por ledger. La tarifa incorporada exige revalidación a partir de `2026-12-04T00:00:00Z`; después el servidor bloquea. Revalidar tarifa/modelo antes de una evaluación posterior, conservar pruebas y volver a publicar; no ampliar fechas o cotas para ocultar un fallo.

Detener el bot con Unpublish; no desactivar el proxy mientras haya evaluaciones en curso. Mantener servicios y cuotas disponibles durante la defensa. La versión anterior se conserva para reversión, pero no publicarla simultáneamente.

Sin respuesta: revisar ejecución antes de reenviar; distinguir fallo controlado de estado Succeeded. Un estado DETENIDO no es propuesta válida.403: revisar credencial cliente/servidor sin mostrarla. USAGE_INCIERTO: conservar reserva y detener nuevas llamadas del caso; no contabilizar cero. Folio no único: resolver ambigüedad sin borrar evidencia. La voz debe reconocer errores y derivar a Telegram.

Las pruebas negativas aisladas escriben fixtures identificados como reservas sintéticas. No son consumo real ni deben mezclarse con costos del proveedor. No ejecutar ese diagnóstico de nuevo solo para grabar.
