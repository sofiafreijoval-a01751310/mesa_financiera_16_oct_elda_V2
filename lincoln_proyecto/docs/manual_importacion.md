# Manual de revisión e importación

## Repetir las pruebas

Ver README. Las pruebas locales no necesitan llaves. Para detener, finalizar el proceso; no hay bot ni polling continuo en este módulo. Si Python no encuentra el skill, ejecutar desde la carpeta correcta y conservar skills/revisar-apoyo-lincoln/scripts/revisar.py. El auditor VizData requiere todos sus archivos adjuntos en la estructura entregada.

## Configuración del respaldo n8n

Guardar copia de la versión vigente antes de importar. Crear un workflow de prueba nuevo; importar exports/Lincoln_Workflow_Telegram_Aprobacion_v03.json. Mantener inactivo hasta configurar:

1. Credencial Telegram con token nuevo si se revocó el expuesto; nunca guardarlo en código.
2. Credencial de modelos:seleccionar proveedor/modelos disponibles y verificar límites; el respaldo usa gpt-4.1 y gpt-5-mini, cuya disponibilidad puede cambiar.
3. Data Tables de ventas, presupuesto, mercado y casos; el export público usa CONFIGURAR_TABLA para no publicar identificadores operativos. Crear muestras desde datos/ y verificar esquema antes de ejecutar.
4. Identidad autorizada en Validar entrada Telegram; reemplazar el usuario DEMO1000000001 solo en la copia operativa privada. Restringir chat privado y no bots.
5. Conectar admisión persistente y registro por llamada ANTES del modelo. Python local no puede invocarse directamente en n8n Cloud sin adaptador o servicio confiable. No poner URLs arbitrarias ni secretos en mensajes.
6. Conectar el revisor y aceptación de alcance al flujo antes de aprobación. Mantener modo SIMULADO. Comprobar folio, versión, dueño, caducidad y decisión única.
7. Solo una instancia Telegram Trigger por bot. Evitar cambiar el webhook del bot operativo durante pruebas paralelas.

Antes de probar un evento nuevo, utilizar fecha futura relativa al día de prueba, inversión, asistentes, audiencia, formato y objetivo completos. La solicitud antigua de20nov2026 es histórica y no debe tratarse como evento futuro después de esa fecha.

## ElevenLabs y consulta de voz

Lo comprobado en la conversación anterior:agente Lincoln | Apoyos a Distribuidores, herramienta consultar_caso_lincoln y workflow separado Lincoln | Consulta de casos por voz. La consulta LIN-34-1 versión1 funcionó después de aclarar el folio. El export de ese workflow y la configuración exacta de herramienta no están en este respaldo; no se inventó un export.

Para recrear con la configuración vigente:exportar el workflow de voz desde n8n y la herramienta desde ElevenLabs sin secretos; verificar métodoPOST, ruta lincoln-voice-cases-v1, body conforme al validador real, Header Auth y respuestaJSON. La URL de producción se obtiene del nodo Webhook; no usar webhook-test para un agente publicado. Copiar el mismo nombre de encabezado exacto y la misma credencial en ambos lados. No añadir un punto al nombre por accidente.

Dar folio completo y versión. Si hay error de transporte, mostrar error de consulta; no afirmar que el folio no existe ni inventar su estado. El acceso público debe limitarse a muestra ficticia mínima y dominios autorizados. Solicitar consentimiento antes de iniciar micrófono y ofrecer texto cuando se deniega. El widget todavía requiere verificación desde la web final.

## Troubleshooting y validación final

Sin respuesta Telegram:verificar activación, credencial y único webhook. No hay datos:verificar tabla/folio/versión y flujo de carga, nunca inventar saldo. Error de auth voz:comprobar encabezado y secreto en ambos servicios sin publicarlo. Error de cliente ElevenLabs no demuestra fallo de n8n; revisar ejecución y respuesta por separado.

Para autorizar cambios de producción, usar resultados de tests/pruebas.csv y conservar evidencia sanitizada. No confundir validación de código en Actions con publicación de Pages ni con una prueba de voz actual.
