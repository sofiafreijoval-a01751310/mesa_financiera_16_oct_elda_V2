# Aplicación de VizData

Audiencia: coordinación académica y de distribuidores. Decisión: comprobar asignación proporcional y revisar evidencia antes de activar integraciones. La audiencia necesita entender el reparto ficticio; la evidencia son ventas2025 y asignación2026; debe poder cotejar valores en la tabla y detectar límites.

Inventario: distribuidor_id identificador único; nombre nominal19 categorías; ventas_2025 conteo entero anual; asignacion_mxn cuantitativo MXN antes de IVA. Granularidad: un distribuidor. 19 registros sin duplicados; 2000 unidades y5millones reconciliados con validar_base.py. Los cuatro nameplates suman cada distribuidor. Mercado PMA es sintético, no oficial ni causal. No se infiere demanda real.

Pregunta principal: comparar magnitudes de asignación. Barras horizontales ordenadas, dominio desde0, una serie, etiquetas largas legibles y valores exactos al lado. Se descarta donut19 partes por lectura angular imprecisa y mapa porque la ubicación no es la pregunta. El color solo destaca extremos; nombres/posición/etiquetas transmiten el mismo contenido. No graficar ventas y asignación como correlación descubierta: son proporcionales por fórmula.

Artefactos: asignaciones.png + tabla asignaciones.csv y brief JSON. El auditor original se ejecutó con --strict sin errores ni warnings. Se revisó el render final del informe. Esto valida una pieza estática; no demuestra teclado, filtros o responsive de un dashboard web. Esa verificación se debe efectuar cuando se prepare Pages. No convertir una gráfica estática en evidencia ficticia de una web publicada.
