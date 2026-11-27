# Alternativa OpenAI: candidato para revisión y conexión

Sofía confirmó que dispone de API OpenAI con saldo. Este candidato aún no está activo: no se hicieron llamadas a su API ni se guardó su clave. El bot publicado conserva Gateway.

## Diseño preparado

- Un proxy compatible con Chat Completions reside en otro workflow de la misma instancia n8n. No necesita contratar otro alojamiento.
- El ingreso se protege con Header Auth. El cliente usa una credencial de proxy distinta de la clave OpenAI; la clave real queda únicamente en la credencial del nodo HTTP de servidor. No incluir ninguna de las dos en GitHub, Pages, ZIP o chat.
- Una tabla privada `lincoln_guard_ledger`, con una sola fila de ID1 y columna texto `state_json`, guarda admisiones, reservas, consumo y estados inciertos. Semilla: `{"schema":1,"seq":0,"cases":[],"requests":[]}`. No crear filas de ledger durante una petición concurrente.
- La admisión de un evento Telegram precede al orquestador. La combinación de actualización condicional del JSON anterior y verificación del propietario debe permitir una sola admisión del mismo evento. La misma puerta se usa para pruebas manuales.
- Cada llamada de los cinco roles pasa por reserva CAS antes de OpenAI. El destino es fijo; el cliente no puede aportar URL, tarifa ni límite. Un conflicto vuelve a leer y recalcular, máximo3veces. Un fallo sin consumo verificable mantiene la reserva y bloquea nuevas llamadas del caso.
- La conciliación usa `usage` del proveedor; no suma de nuevo el costo del loop ni el razonamiento incluido en la salida. El cargo calculado con tarifa estándar sigue separado de una factura.
- Máximo25llamadas y360segundos por caso; USD0.25 de costo de tokens de texto a tarifa estándar, sin impuestos, voz ni infraestructura. La política vence el4/dic/2026 UTC para exigir revisión de tarifas. No es un límite de gasto de toda la cuenta OpenAI.

## Cota conservadora sin adivinar tokens de entrada

El candidato admite exclusivamente `gpt-4o-mini-2024-07-18`, texto, una salida, tarifa default, hasta4096tokens de salida. Reserva el costo de toda la ventana de128000tokens de entrada más esa salida máxima: `128000×0.15/1e6 + 4096×0.60/1e6 = USD0.0216576` por llamada. Al conciliar uso válido libera la diferencia; el costo estándar conserva la tarifa completa de entrada sin suponer descuentos de caché.

La cota depende de las tarifas y límites del modelo revisados, no de caracteres ni estimaciones del prompt. Se rechazan otros modelos, precios premium, imágenes, servicios de búsqueda facturables y múltiples salidas. El snapshot está deprecado con retiro anunciado el14/ene/2027; no se cambia automáticamente a otro modelo y requiere prueba de disponibilidad en la cuenta. La calidad de los cuatro agentes con este modelo todavía no se ha medido.

Fuentes oficiales revisadas26/nov/2026:
- https://developers.openai.com/api/docs/models/gpt-4o-mini
- https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create
- https://github.com/n8n-io/n8n/blob/n8n%402.47.6/packages/%40n8n/nodes-langchain/nodes/llms/LMChatOpenAi/LmChatOpenAi.node.ts
- https://github.com/n8n-io/n8n/blob/n8n%402.47.6/packages/nodes-base/credentials/OpenAiApi.credentials.ts

## Configuración e intervención pendiente

1. Crear tabla y semilla, asociarla a las cuatro operaciones de lectura/actualización. El JSON público contiene únicamente un marcador de tabla.
2. En `OpenAI controlado`, Sofía guarda su API Key en una credencial OpenAI con URL oficial. Esa entrada debe realizarla ella en la interfaz; no pegar la clave en el chat.
3. Configurar un secreto exclusivo para el proxy en Header Auth y la credencial cliente OpenAI compatible. El cliente apunta al webhook del proxy y añade `X-Lincoln-Case` con el folio generado por el servidor. Esta protección nueva debe revisarse antes de publicar el endpoint.
4. Preparar el adaptador del flujo principal: admisión del evento, todos los modelos a través del proxy, sin reintentos automáticos y respuesta segura de bloqueo. Este adaptador sigue pendiente; no cambiar un solo modelo dejando otros fuera del guardián.
5. Probar CAS simultáneo, fallo/timeout y costo antes de una evaluación completa. Después comprobar calidad y conservación del folio en Telegram/voz. Solo entonces activar y actualizar la matriz.

## Evidencia actual

`tests/test_guard_proxy.cjs`:21pruebas locales del planificador. Prueban esquema, admisión, presupuesto, reservas sin conciliar, conciliación, límites, incertidumbre y respuesta compatible. No ejecutan peticiones reales ni certifican atomicidad de DataTable.

`exports/Lincoln_Proxy_OpenAI_CANDIDATO_PUBLICO.json`:26nodos, inactivo, sin credenciales y sin datos fijados. No debe presentarse como integración terminada. Cada invocación del proxy consume una ejecución adicional de n8n; medir la cuota y la latencia antes de escalar.
