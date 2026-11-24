---
name: vizdata
description: Diseñar, revisar y mejorar visualizaciones de datos, dashboards, infografías, sitios web, apps y one-pagers con estructura profesional y selección de gráficas compatible con la pregunta analítica, los tipos de variables y la forma de los datos. Usar al explorar datasets, definir una arquitectura de información, elegir o auditar gráficas, crear especificaciones visuales, diseñar interfaces analíticas, contar historias con datos o comprobar claridad, honestidad, accesibilidad y adaptación responsive.
---

# VizData

Convertir datos en una experiencia visual útil, verificable y profesional. Elegir la gráfica por la tarea analítica y la estructura de los datos; tratar estilo, herramienta y formato como decisiones posteriores.

## Flujo obligatorio

1. Formular el encargo.
2. Auditar la estructura y calidad de los datos.
3. Definir el mensaje o las preguntas que la pieza debe responder.
4. Elegir la familia analítica y después la gráfica.
5. Diseñar la jerarquía y el recorrido de lectura para el formato final.
6. Aplicar anotación, color, tipografía, interacción y accesibilidad.
7. Auditar integridad estadística, adecuación gráfica y legibilidad.
8. Probar el resultado con datos reales, tamaños finales y estados límite.

No saltar directamente a la gráfica. Si faltan datos esenciales, declarar supuestos y proponer la estructura sin inventar valores.

## 1. Formular el encargo

Definir antes de diseñar:

- audiencia, decisión y acción esperada;
- pregunta principal y hasta tres preguntas secundarias;
- modo `exploratorio`, `explicativo` o `híbrido`;
- formato: dashboard, infografía, web, app o one-pager;
- contexto de uso, tamaño, dispositivo, frecuencia de actualización y tiempo de lectura;
- nivel de detalle, sensibilidad, fuente, periodo, zona horaria y unidad;
- restricciones de marca, herramienta, accesibilidad y privacidad.

Usar `assets/viz-brief-template.json` como estructura inicial cuando el encargo sea complejo.

## 2. Auditar los datos

Identificar cada campo como identificador, categórico nominal, ordinal, cuantitativo, temporal, geográfico, jerárquico, relacional o textual. Registrar:

- unidad, granularidad y denominador;
- cardinalidad de categorías y número de series;
- valores faltantes, duplicados, ceros, negativos y outliers;
- rango, distribución, sesgo y periodicidad;
- si las partes forman un total válido y comparable;
- si una medida geográfica es conteo o tasa normalizada;
- si fechas, monedas, porcentajes y agregaciones son coherentes;
- si el tamaño de muestra y la incertidumbre deben mostrarse.

No presentar correlación como causalidad. No comparar totales con denominadores incompatibles. No ocultar cambios de definición o periodos incompletos.

## 3. Establecer la intención editorial

Escribir una frase de trabajo:

`La audiencia necesita [entender/decidir] ___; la evidencia principal es ___; debería poder actuar haciendo ___.`

Para una pieza explicativa, convertir el título principal en una conclusión comprobable. Para una pieza exploratoria, usar un título descriptivo y ofrecer controles que respondan preguntas reales. Separar claramente hechos, estimaciones, metas y opiniones.

## 4. Elegir la gráfica

Leer siempre `references/chart-selection.md` antes de seleccionar o aprobar gráficas. Aplicar este orden:

1. Determinar la tarea: búsqueda exacta, comparación, tendencia, distribución, relación, composición, desviación, rango, flujo, jerarquía, geografía o agenda.
2. Confirmar que los campos y sus escalas permiten esa tarea.
3. Elegir la codificación más perceptualmente precisa disponible: posición en escala común, longitud, posición no alineada, área, ángulo y finalmente volumen.
4. Probar una opción familiar antes de una exótica; usar una forma compleja solo si revela algo que la simple no puede.
5. Documentar una alternativa y explicar por qué fue descartada.

Reglas estrictas:

- Usar tabla o texto para valores exactos, no una gráfica decorativa.
- Iniciar barras en cero; si una excepción es imprescindible, marcar la ruptura y justificarla.
- Reservar líneas para secuencias ordenadas o continuas, especialmente tiempo.
- Usar dispersión para relación entre dos variables cuantitativas; añadir tamaño solo con una tercera variable cuantitativa legible.
- Usar histogramas, densidad, boxplots o violines para distribución, no barras de promedios aisladas.
- Usar pastel/donut solo para pocas partes no negativas de un único total; preferir barras cuando la comparación importe.
- Usar coropletas para tasas normalizadas, no para conteos brutos afectados por población o área.
- Evitar 3D, doble eje sin justificación, áreas decorativas, gauges redundantes, word clouds como análisis y arcoíris no ordenado.
- Mostrar incertidumbre cuando afecte la conclusión.

Para especificaciones estructuradas, ejecutar:

```bash
python scripts/audit_viz_spec.py especificacion.json
```

Corregir todos los hallazgos `error`; resolver o justificar los `warning`.

## 5. Estructurar el producto

Leer `references/layouts-by-format.md` y aplicar solo la sección del formato solicitado.

Principios comunes:

- Establecer una pregunta o mensaje dominante por vista.
- Ordenar de contexto y señal principal hacia evidencia y detalle.
- Crear jerarquía con posición, tamaño y espacio antes que con color.
- Mantener alineaciones y una retícula coherente.
- Agrupar elementos que deben compararse; separar los que no.
- Diseñar primero el tamaño real y después sus adaptaciones.
- Mantener fuentes, unidades, filtros activos, fecha de corte y definiciones visibles.
- Incluir estados vacío, carga, error, sin permiso y datos desactualizados en web/apps.

No convertir un dashboard en una presentación fija ni una infografía en un panel de monitoreo. Adecuar densidad, navegación e interacción al uso.

## 6. Narrar, anotar y dirigir atención

Leer `references/story-accessibility-qa.md` para piezas explicativas o de alta visibilidad.

- Usar títulos que indiquen el hallazgo cuando exista una conclusión.
- Etiquetar directamente cuando reduzca saltos entre marca y leyenda.
- Resaltar solo la evidencia que sostiene el mensaje; atenuar el contexto.
- Eliminar bordes, fondos, iconos, gridlines y decimales que no aporten lectura.
- Añadir notas para eventos, definiciones, anomalías y cambios metodológicos.
- Conservar una fuente humana legible y trazable.
- No usar color como único canal semántico.

## 7. Diseñar interacción

En web, app o dashboard interactivo:

- usar overview primero, luego filtro, detalle bajo demanda y retorno claro;
- conservar filtros, selección, orden y rango temporal en estado visible;
- ofrecer valores con teclado y lector de pantalla, no solo con hover;
- evitar controles que no cambian una decisión o pregunta;
- prevenir comparaciones inválidas tras filtrar;
- priorizar rendimiento perceptible y respuesta inmediata;
- permitir compartir o exportar el estado analítico cuando sea relevante.

## 8. Entregar y auditar

Entregar, según el encargo:

- objetivo, audiencia y decisión;
- inventario de datos y supuestos;
- mapa de preguntas a gráficas con justificación;
- arquitectura de información o wireframe;
- especificación de escalas, orden, color, etiquetas e interacción;
- resultado final;
- lista de comprobaciones y limitaciones.

La aprobación final exige:

- gráfica compatible con tarea, tipos y cardinalidad;
- escalas honestas, agregaciones coherentes y denominadores visibles;
- lectura principal comprensible en pocos segundos;
- detalle suficiente sin sobrecarga;
- contraste, teclado, texto alternativo y paleta accesible;
- visualización legible en tamaño final y pantallas estrechas;
- fuentes, fecha de corte, unidades y notas metodológicas presentes;
- ausencia de solapamientos, recortes, etiquetas ambiguas y estados rotos.

Leer `references/source-synthesis.md` solo cuando sea necesario explicar el fundamento metodológico o adaptar el sistema a una organización.

