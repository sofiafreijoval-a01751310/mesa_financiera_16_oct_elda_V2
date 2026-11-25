# Uso de créditos Gateway de n8n

Decisión de Sofía: conservar Gateway credits. Revisión documental: 24 de noviembre de 2026.

## Qué se conserva

Los modelos continúan utilizando la conexión Gateway existente. No se requiere una clave nueva de OpenAI. Los créditos del asistente de construcción de n8n son distintos de los créditos Gateway que pagan las llamadas de los modelos del workflow.

n8n descuenta las solicitudes de un saldo prepago de la instancia y publica tarifas propias por servicio. Por tanto, los escenarios calculados con precios públicos de OpenAI en `costos.md` son referencias de planeación; no acreditan el cargo Gateway ni su saldo actual.

## Alcance de los controles actuales

- La exportación v04 mantiene los límites de tokens, iteraciones y tiempo configurados. Estos acotan trabajo, pero no constituyen una reserva monetaria por llamada.
- `limite_costo_usd: 0.25` es una regla declarada del caso. Todavía no está conectada a un corte monetario comprobado en el servicio Gateway.
- El guardián SQLite y sus pruebas de reservas y duplicados son locales. No prueban exclusión mutua ni gasto máximo en la instancia n8n.
- El agotamiento del saldo Gateway detiene los nodos que lo utilizan. Es un control del saldo de la instancia, no un límite individual por caso.
- No se habilitarán recargas automáticas ni compras como parte de esta revisión.

## Medición de una prueba controlada

1. Confirmar el saldo actual en la credencial Gateway y consultar las tarifas de los modelos seleccionados.
2. Mantener la copia de ensayo sin publicar y comprobar que no haya otras ejecuciones consumiendo Gateway durante la medición.
3. Ejecutar una sola solicitud sintética y conservar el identificador de ejecución, hora, modelo y llamadas observadas. No enviar aprobaciones de prueba a destinatarios reales.
4. Consultar el consumo por workflow/modelo en Cloud console y registrar el cargo informado por n8n, incluidas llamadas fallidas facturadas. Si el panel no permite atribuir un cargo a una solicitud, marcarlo como consumo agregado, no como costo exacto del caso.
5. Completar `costos/consumo_real_plantilla.csv` únicamente con datos verificables. Una diferencia entre saldos redondeados es una aproximación; no es un recibo por solicitud.
6. Revisar el resultado antes de ejecutar otro caso. No presentar la prueba como validación de un tope automático de USD 0.25.

## Alternativa descartada

No se incorporará el nodo LangChain Code como envoltorio de llamadas. La documentación oficial lo declara no disponible en n8n Cloud y desaconseja su uso por problemas de seguridad. No se sustituye esta limitación por código que aparente controlar un gasto que no puede interceptar.

## Pendientes de la instancia

Saldo actual, tarifas Gateway aplicables, consumo real y prueba de ejecución de la copia v04: pendientes de verificar. Este documento no afirma haber modificado ni ejecutado el workflow vivo.

## Fuentes oficiales consultadas

- Gateway, distinción de créditos, saldo y seguimiento por workflow/modelo: https://github.com/n8n-io/n8n-docs/blob/main/docs/build/understand-workflows/use-gateway-credits.md
- Tarifas Gateway: https://app.n8n.cloud/service-pricing
- Disponibilidad y advertencia de LangChain Code: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.code/
