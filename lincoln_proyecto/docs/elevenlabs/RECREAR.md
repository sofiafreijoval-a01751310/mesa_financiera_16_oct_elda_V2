# Agente de consulta Lincoln: configuración reproducible

Configuración observada y publicada el 26/nov/2026, agente `agent_3501m6mxrb3df2hr4f4491ew8j6s`, rama Main. Versión final observada `agtvrsn_3101m8d5fse5fr69cpwex6gbfaem`. El respaldo público es una selección normalizada de campos del JSON copiado desde la interfaz; omite información de cuenta, IDs de secretos y valores predeterminados ajenos al ejercicio. No es una exportación íntegra del workspace ni una copia de credenciales.

## Recreación

1. Crear un agente personalizado. Utilizar `exports/ElevenLabs_Lincoln_CONFIG_PUBLICA.json` como configuración de referencia; copiar el texto de `prompt_sistema.txt` al mensaje del sistema. No sobrescribir el agente operativo para probar la recreación.
2. Establecer idioma Español, zona America/Mexico_City y el primer mensaje del JSON. Voz observada Eric, ID `cjVigY5qzO86Huf0OWal`, modelo `eleven_v4_turbo`. LLM observado `deepseek-v41-flash`. Su disponibilidad depende de la plataforma; no se ha verificado una importación en otra cuenta.
3. Crear o reutilizar la herramienta webhook `consultar_caso_lincoln`: POST al Production URL del workflow de voz de n8n, path `lincoln-voice-cases-v1`. Crear en ElevenLabs la referencia al secreto compartido existente y enviar encabezado `X-Lincoln-Key`, sin punto final. El mismo valor debe estar configurado en Header Auth de n8n. Nunca guardarlo en GitHub, Pages, el prompt o el ZIP público.
4. Cuerpo JSON con `caso_id` y `version`, ambos strings requeridos. Adjuntar la herramienta al agente; crearla en el workspace no la adjunta automáticamente. No activar herramientas simuladas para demostrar integración. Timeout de herramienta observado10s y redirecciones desactivadas.
5. Configurar voz activada (`text_only:false`) y eventos de audio. Texto/transcripción del widget habilitados como alternativa accesible. Una entrada por dictado en un chat de texto no demuestra reproducción de voz. Iniciar una llamada de voz para probar micrófono y altavoz.
6. Límites publicados:120s por conversación,30s de silencio,5llamadas/día,1concurrente; ráfagas, colas y turno especulativo desactivados. Son límites de uso, no una garantía de gasto máximo en USD. Falta comprobar en vivo que cada corte se haga cumplir.
7. Publicar, probar un folio único existente y otro inexistente. Ver `evidencias/elevenlabs_26nov.json`. Para acceso al caso, usar folio completo con guiones y versión separada. APROBADO_SIMULADO es una decisión humana del ejercicio; no autoriza pagos reales.

## Estado y límites de la evidencia

La herramienta real devolvió `ok:true` para LIN-34-1 y `ok:false` para LIN-999999-1. Una conversación de texto con simulación de herramientas desactivada llamó dos veces al webhook y explicó ambos resultados. Rechazó después revelar el encabezado y aprobar un pago; no generó una tercera llamada de herramienta. Se ajustó después la redacción de APROBADO_SIMULADO y la brevedad; falta la prueba audible de esa versión final.

El panel estimó200créditos, desglosados en110LLM (USD0.011 estimados) y90plataforma. No equivale a factura ni al costo de una conversación de voz. No se midieron tokens ni minutos de voz de esta prueba de texto.

Base de conocimiento observada vacía: la fuente de casos es el webhook, no documentos inventados. Autenticación del agente desactivada y lista de hosts vacía; el widget sigue público. No es una configuración apropiada para datos reales. Se conserva esta limitación explícita; el encabezado protege n8n frente a solicitudes sin secreto, pero el acceso público al agente no autentica al usuario que pregunta. Solo se usan datos sintéticos y la respuesta de n8n aplica una proyección de campos permitidos.
