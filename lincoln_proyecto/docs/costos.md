# Costos y límites

Corte de tarifas: 23 de noviembre de 2026. Moneda USD; no se usó tipo de cambio a MXN.

| Modelo del respaldo v03 | Entrada USD / millón | Salida USD / millón |
|---|---:|---:|
| Orquestador: GPT-4.1 | 2.00 | 8.00 |
| Cuatro especialistas: GPT-5 mini | 0.25 | 2.00 |

Fuentes oficiales: https://developers.openai.com/api/docs/models/gpt-4.1 y https://developers.openai.com/api/docs/models/gpt-5-mini . La segunda ficha marca el modelo como deprecated; conservarlo aquí explica el respaldo, no garantiza disponibilidad futura. No se cambió el modelo del flujo activo.

Se ejecutó el skill original cotizar-tokens-ia: cinco tokenizaciones o200k_base y cinco cálculos Decimal. Se consultó también https://autosheet.com/tools/openai-chatgpt-api-pricing-calculator (antes gptforwork). Los conteos son del texto estático exportado, con expresiones n8n sin resolver: no son usage del proveedor. El archivo costos/tokenizacion.json indica alcance y hash. La sobrecarga, contexto dinámico y toda salida facturable (incluido razonamiento) son supuestos explícitos de planeación en costos_por_etapa.csv. No se asumió caché ni descuentos.

| Escenario | Llamadas supuestas/caso | USD/caso LLM | 100 casos | 1,000 casos | 10,000 casos |
|---|---:|---:|---:|---:|---:|
| Base | 14 | 0.09615425 | 9.615425 | 96.15425 | 961.5425 |
| Alto | 25 | 0.29446350 | 29.446350 | 294.46350 | 2944.6350 |

Fórmula por etapa = (tokens entrada × tarifa entrada + tokens salida × tarifa salida)/1,000,000. Sumar etapas por caso, luego multiplicar por volumen. El escenario alto es sensibilidad sin restricción: al exceder USD 0.25, una admisión correctamente conectada debe detener nuevas llamadas. No garantizar que cualquier caso termina bajo ese límite.

## Voz e infraestructura

ElevenAgents mensual público: Free USD0/15 minutos, Starter USD6/75 minutos, Creator USD22/275 minutos; fuente https://elevenlabs.io/pricing/agents . No se usaron promociones. Duración por consulta desconocida. Sensibilidad ilustrativa: a un minuto por consulta, 100/1,000/10,000 casos consumen 100/1,000/10,000 minutos; a dos minutos, 200/2,000/20,000. Esto no es una medición. El precio aplicable a excedentes y al LLM de voz debe confirmarse en el plan contratado; no sumar una tarifa inventada.

n8n anuncia Starter EUR20/mes con facturación anual y 2,500 ejecuciones: https://n8n.io/pricing/ . Es referencia comercial, no factura de esta cuenta. Cada entrada, consulta de voz y eventual callback pueden producir ejecuciones separadas. El volumen de casos no equivale automáticamente al de ejecuciones. Hosting, gateway, voz, IVA, FX y cuotas de desarrollo quedan separados.

## Gasto real

No se dispone de usage completo por request ni facturas. Gasto de producción y desarrollo: DESCONOCIDO, nunca cero. Los dos loops de demostración sí ejecutan exclusivamente Python local y no llaman API de modelos: gasto API de esas ejecuciones = USD0; esto no estima CPU/hosting ni el trabajo de desarrollo en ChatGPT.

Para conciliar, completar costos/consumo_real_plantilla.csv con request_id, etapa, modelo, entrada/caché/salida/razonamiento, USD facturado y duración de voz desde logs/exportaciones del proveedor. No volver a sumar reasoning si ya integra output_tokens. Registrar llamadas fallidas cuando el proveedor las facture.

## Conexión elegida: Gateway credits

Se conserva la conexión Gateway de n8n por indicación de Sofía. Sus tarifas y cargos se deben consultar en n8n; los precios públicos de OpenAI de este documento no se presentan como tarifas Gateway. El 24/nov/2026 se observó saldo USD1.46 y consumo Gateway agregado del workflow de USD0.16 en el periodo de siete días; el saldo inicial mostrado era USD1.62. Estos importes están redondeados y no son un cargo exacto por caso. Ver evidencia `evidencias/n8n_gateway_24nov.json`. El valor nominal USD 0.25 no es todavía un corte monetario comprobado en n8n. Ver [procedimiento de medición y alcance](creditos_gateway.md).
