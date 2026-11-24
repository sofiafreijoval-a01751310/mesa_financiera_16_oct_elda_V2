# Arquitectura visual por formato

## Índice

1. Sistema común
2. Dashboard
3. Infografía
4. Web
5. App
6. One-pager
7. Responsive

## 1. Sistema común

Construir una retícula, una escala tipográfica, reglas de espaciado y tokens semánticos de color. Reservar la zona de mayor prominencia para la señal más importante, no para el logo o la decoración. Organizar por proximidad y comparación.

## 2. Dashboard

### Jerarquía recomendada

1. Contexto: título, alcance, fecha de corte, filtros activos.
2. Estado: 3–7 KPIs esenciales con meta, periodo comparativo y tendencia.
3. Diagnóstico: visuales que explican por qué cambia el estado.
4. Detalle: tabla o drill-down para decidir acciones.
5. Fuente, definiciones y freshness.

Mantener una vista inicial sin scroll cuando el uso sea monitoreo operativo y el tamaño objetivo lo permita. No forzar esta regla en análisis profundo. Usar consistencia de escalas en pequeños múltiples. Diseñar alertas por excepción, no llenar todo de rojo/verde.

### Tipos

- Ejecutivo: síntesis, tendencias y excepciones; baja densidad.
- Operativo: estado actual, umbrales, responsables y actualización frecuente.
- Analítico: filtros, comparación, detalle y trazabilidad; mayor densidad controlada.
- Personal: priorizar decisiones y métricas del usuario, no un promedio organizacional.

## 3. Infografía

Definir un recorrido explícito: gancho, contexto, evidencia, explicación y cierre/acción. Usar una visual principal y módulos secundarios. Integrar texto e imagen sin convertir los datos en decoración. Mantener el orden de lectura en móvil y al imprimir. Las ilustraciones deben explicar, orientar o crear memoria, nunca cambiar la magnitud representada.

## 4. Web

Ubicar la promesa y la señal principal temprano. Usar secciones escaneables, ancho de lectura cómodo y navegación consistente. Cargar visualizaciones progresivamente sin desplazar el layout. Ofrecer una tabla accesible o resumen equivalente. Preservar URL/estado para filtros compartibles cuando el análisis sea colaborativo.

## 5. App

Estructurar alrededor de tareas: observar, investigar, decidir, actuar y confirmar. Reducir controles simultáneos; revelar complejidad bajo demanda. Diseñar feedback, permisos, estados vacíos, error, carga, offline y datos vencidos. Hacer objetivos táctiles suficientes y mantener interacción por teclado.

## 6. One-pager

Usar una sola tesis. Distribuir la página en:

1. título-conclusión y subtítulo contextual;
2. cifra o visual principal;
3. 2–4 evidencias de soporte;
4. implicaciones y recomendación;
5. metodología, fuente y contacto.

Evitar miniaturizar un dashboard. Si una gráfica requiere interacción o explicación extensa, simplificarla o mover el detalle a un anexo/enlace.

## 7. Responsive

- Cambiar estructura, no solo tamaño.
- Apilar módulos en orden de decisión.
- Convertir leyendas en etiquetas directas cuando sea posible.
- Reducir ticks, no eliminar unidades o contexto.
- Ofrecer scroll horizontal controlado solo para tablas o series donde preserve significado.
- Reemplazar hover por tap/focus y mantener contenido accesible sin gesto.
- Probar 320 px, 768 px, escritorio y tamaño de impresión cuando apliquen.

