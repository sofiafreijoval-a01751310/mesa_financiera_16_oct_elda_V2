# Diccionario de datos y contratos

Todos los datos de negocio de muestra son sintéticos v0.1. Moneda MXN antes de IVA; periodo ventas2025 y bolsa2026.

| Campo | Tipo/unidad | Regla |
|---|---|---|
| distribuidor_id | identificador D01..D19 | Único en base; une ventas y PMA. |
| nombre | categórico nominal | Nombre aportado por la estudiante;19categorías. |
| ventas_2025 | entero unidades/año | No negativo;total nacional2000. |
| ventas_por_nameplate | objeto Corsair/Nautilus/Aviator/Navigator | Enteros no negativos; suma igual ventas_2025. |
| participacion_pct | porcentaje0..100 | ventas_2025 /2000×100. |
| asignacion_mxn | moneda | ventas_2025 /2000×5000000. |
| aprobado_mxn/reservado_mxn | moneda | No negativo; descontar según política transaccional de estado. |
| disponible_mxn | moneda | asignacion-aprobado-reservado; nunca negativo. |
| nameplate_referencia | categoría | Uno de los cuatro modelos. |
| unidades_segmento_2024/2025 | entero de mercado ficticio | No inferir fuente real;2024positivo para calcular crecimiento. |
| crecimiento_pct | porcentaje | (unidades2025/unidades2024-1)×100; no garantiza oportunidad comercial. |
| caso_id | LIN-entero-entero | Consistente entre datos, propuesta y revisión. |
| modo | enumeración | SIMULADO por defecto y en demostrador. |
| inversion_mxn | decimal positivo | Hasta2decimales, finito, antes de IVA. |
| fuente/version | cadenas | Obligatorias; autenticidad depende del conector autorizado. |
| apoyo_mxn | decimal | min(inversion/2,saldo), centavo impar hacia abajo. |
| aportacion_mxn | decimal | Igual a apoyo para conservar50/50 del alcance ajustado. |
| inversion_ajustada_mxn | decimal | Dos veces apoyo; exigir aceptación si reduce inversión. |
| estado | enumeración | Propuesta PENDIENTE_APROBACION; no implica decisión humana. |
| version_propuesta | entero de negocio | Verificar antes de decisión; diferente del número de revisión local del loop. |
| event_id/update_id | identificador de evento | Único persistente para dedup previa al modelo. No publicar usuario real. |
| reserved/actual_microusd | entero microUSD | Reserva conservadora antes de llamada y conciliación del cargo real. |

El contrato ejecutable del nuevo revisor está en skills/revisar-apoyo-lincoln/references/contrato.json. Para los agentes vivos, conservar además los contratos originales del export n8n; no confundir el adaptador local simplificado con el formato completo de todas sus herramientas.
