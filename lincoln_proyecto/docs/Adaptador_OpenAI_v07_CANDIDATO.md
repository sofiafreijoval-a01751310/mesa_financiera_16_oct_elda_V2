# Adaptador de admisión y modelos v07 — inactivo

Este export conserva Telegram, los cuatro especialistas, la revisión versionada y la decisión humana. Antes de cualquier modelo, intenta admitir el evento en el proxy. Solo una respuesta HTTP200 con `ok:true`, `admitido:true` y el mismo folio permite continuar. Un fallo, folio ajeno o repetición devuelve un aviso seguro y no crea otro registro del caso.

Los cinco modelos se configuran exclusivamente con `gpt-4o-mini-2024-07-18`, salida máxima4096 y cero reintentos automáticos. Sus credenciales anteriores se eliminan deliberadamente del candidato: falta seleccionar en los cinco nodos una credencial cliente de proxy con Base URL `https://sofiafreijo.app.n8n.cloud/webhook/lincoln-llm-guard/v1`, API key igual al secreto exclusivo del proxy y encabezado personalizado `X-Lincoln-Case` con expresión `{{ $('Inicializar caso').first().json.caso_id }}`. La API key real OpenAI permanece en el workflow servidor.

La admisión HTTP usa Header Auth con el mismo secreto del proxy. El servidor debe exigir encabezado `Authorization` cuyo valor sea `Bearer ` seguido del secreto. Esta credencial nueva debe configurarse privadamente por la usuaria; el código no genera ni guarda secretos. No reutilizar la clave del webhook de voz.

Si el orquestador o el contrato de respuesta fallan, el caso se detiene con un mensaje genérico; no se propagan errores del proveedor que pudieran incluir detalles internos. Esto no convierte una reserva incierta en consumo cero ni libera su presupuesto.

## Estado y activación pendiente

El adaptador está importado como candidato inactivo; el bot publicado sigue en Gateway. Los cinco modelos ya seleccionan Lincoln Proxy Cliente con Responses API desactivada. La selección de credenciales, la disponibilidad/calidad del modelo, la compatibilidad SDK/SSE y la concurrencia CAS requieren pruebas en n8n antes de sustituir la ruta publicada. El export público no contiene credenciales ni datos fijados. Cada llamada al proxy agrega una ejecución n8n.

El26/nov se observó la credencial OpenAI seleccionada en el nodo servidor y se verificaron los cuatro enlaces a la tabla privada. La prueba mínima81 sí acreditó reserva previa y conciliación de19 tokens de entrada y1 de salida. La autenticación cliente/servidor se corrigió después: el caso87 pasó el primer especialista, pero se detuvo por formato de historial;92 reprodujo el bloqueo. El proxy ya normaliza assistant con tool_calls y contenido ausente o array vacío, y bloques exclusivamente textuales. El caso97 pasó además las tres fuentes y alcanzó propuesta/revisión; el calculador rechazó metadatos de transporte nuevos. Se corrigió el esquema sin relajar importes. La evaluación manual123 sí pasó: cuatro especialistas, transferencia observada y revisión determinista V1→V2; registro21 pendiente de aprobación. Sus11 llamadas conciliadas suman USD0.007041300 a tarifa estándar, sin infraestructura ni voz. Fuente: evidencias/v07_integracion_27nov.json y costos/consumo_proxy_27nov.csv. Ninguna de estas observaciones certifica todavía concurrencia CAS ni un límite monetario activo en el bot Gateway.

Validación local: `node tests/test_admission_v07.cjs` comprueba admisión, bloqueo de respuestas ambiguas, ausencia de camino hacia modelos o registro en la rama denegada y sanitización de errores. No certifica las credenciales ni sustituye las pruebas vivas.


Los metadatos control_admitido, control_estado y respuesta_control se admiten exclusivamente como transporte. La etiqueta skills_cargados.carga no es evidencia de uso ni autorización; el cálculo la ignora. Los hashes e instrucciones configurados se registran separadamente.

La salida final usa Return Intermediate Steps: reconstruye exclusivamente observaciones de herramientas ejecutadas, con folio/rol/estado y orden verificados. El contrato original sigue validando audiencia y datos; una traza incompleta, ajena o adversa detiene el caso. No se guardan pensamientos del modelo ni se convierte una revisión técnica en aprobación humana.
