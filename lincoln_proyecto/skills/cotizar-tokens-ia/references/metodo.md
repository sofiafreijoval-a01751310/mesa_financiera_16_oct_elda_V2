# Método de cálculo y contrato de datos

Fórmula sin descuentos: C = (Tin × Pin + Tout × Pout) / 1,000,000 + cargo fijo.
Total de N llamadas = C × N. Una interacción de q llamadas idénticas cuesta C × q.
Diferencia absoluta A−B = C_A − C_B. Diferencia % = 100 × (C_A−C_B)/C_B; si B=0, N/D.
Participación económica entrada = 100 × C_entrada / C_total; análogo para salida.
Conversión = costo USD × tasa (unidades de moneda por USD).
Recargo r = costo × (1+r). Margen bruto sobre precio: precio = costo/(1−m); no confundir.
Caché requiere tarifa y cantidad explícitas: ((Tin−Tcache)Pin + Tcache Pcache + Tout Pout)/1M + fijo.

El script de referencia opera sin caché y sin batch. Usar Decimal, no redondear cálculos intermedios.

## JSON de entrada

Incluir currency, fx, fx_source, fx_date, baseline, scenarios y models.
Cada escenario: name, input_tokens, output_tokens.
Cada modelo: name, input_usd_m, output_usd_m, fixed_usd_call, source, verified_at.
Entregar precios como cadenas decimales. No llenar faltantes con cero: cero solo cuando el usuario o la fuente lo confirma. USD→USD permite fx=1, fuente identidad.

Los escenarios de renta de autos aportados por Sofía usan 10/40 tokens de pregunta y 200/3100 de respuesta. Se trata de una simulación con tokens conocidos. Medir el mismo texto con cada proveedor para comparar consumo efectivo.

## Fuentes

Tokenizer de referencia: https://platform.openai.com/tokenizer
Port BPE incluido: https://github.com/niieani/gpt-tokenizer (2.9.0, MIT).
Tarifas comparativas: https://gptforwork.com/tools/openai-chatgpt-api-pricing-calculator
Banxico SIE: https://www.banxico.org.mx/SieAPIRest/
No fijar precios ni tipos de cambio en el skill: verificarlos en cada ejecución.
