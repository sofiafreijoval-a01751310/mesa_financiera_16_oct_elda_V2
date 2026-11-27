# Adaptador de admisión y modelos v07 — inactivo

Este export conserva Telegram, los cuatro especialistas, la revisión versionada y la decisión humana. Antes de cualquier modelo, intenta admitir el evento en el proxy. Solo una respuesta HTTP200 con `ok:true`, `admitido:true` y el mismo folio permite continuar. Un fallo, folio ajeno o repetición devuelve un aviso seguro y no crea otro registro del caso.

Los cinco modelos se configuran exclusivamente con `gpt-4o-mini-2024-07-18`, salida máxima4096 y cero reintentos automáticos. Sus credenciales anteriores se eliminan deliberadamente del candidato: falta seleccionar en los cinco nodos una credencial cliente de proxy con Base URL `https://sofiafreijo.app.n8n.cloud/webhook/lincoln-llm-guard/v1`, API key igual al secreto exclusivo del proxy y encabezado personalizado `X-Lincoln-Case` con expresión `{{ $('Inicializar caso').first().json.caso_id }}`. La API key real OpenAI permanece en el workflow servidor.

La admisión HTTP usa Header Auth con el mismo secreto del proxy. El servidor debe exigir encabezado `Authorization` cuyo valor sea `Bearer ` seguido del secreto. Esta credencial nueva debe configurarse privadamente por la usuaria; el código no genera ni guarda secretos. No reutilizar la clave del webhook de voz.

Si el orquestador o el contrato de respuesta fallan, el caso se detiene con un mensaje genérico; no se propagan errores del proveedor que pudieran incluir detalles internos. Esto no convierte una reserva incierta en consumo cero ni libera su presupuesto.

## Estado y activación pendiente

El adaptador no está importado ni publicado y el bot sigue en Gateway. La selección de credenciales, la disponibilidad/calidad del modelo, la compatibilidad SDK/SSE y la concurrencia CAS requieren pruebas en n8n antes de sustituir la ruta publicada. El export público no contiene credenciales ni datos fijados. Cada llamada al proxy agrega una ejecución n8n.

El26/nov se observó la credencial OpenAI seleccionada en el nodo servidor y se verificaron los cuatro enlaces a la tabla privada. Esta observación no acredita todavía una llamada de API satisfactoria ni un límite monetario activo.

Validación local: `node tests/test_admission_v07.cjs` comprueba admisión, bloqueo de respuestas ambiguas, ausencia de camino hacia modelos o registro en la rama denegada y sanitización de errores. No certifica las credenciales ni sustituye las pruebas vivas.
