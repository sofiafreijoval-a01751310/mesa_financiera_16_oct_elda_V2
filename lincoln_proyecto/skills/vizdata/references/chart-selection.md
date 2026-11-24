# Selección de gráficas por pregunta y estructura de datos

## Índice

1. Protocolo de selección
2. Matriz principal
3. Reglas por familia
4. Codificación y escalas
5. Casos que requieren cautela

## 1. Protocolo de selección

Responder en orden:

1. ¿Qué debe detectar la audiencia: valor, diferencia, tendencia, forma, relación, parte, flujo, lugar o secuencia?
2. ¿Qué campos intervienen y qué tipo tiene cada uno?
3. ¿Cuántas categorías, series y observaciones existen?
4. ¿La tarea exige precisión, patrón general o exploración?
5. ¿Hay negativos, faltantes, outliers, incertidumbre o denominadores diferentes?
6. ¿La pieza es estática o interactiva y cuánto espacio real tiene?

## 2. Matriz principal

| Pregunta analítica | Datos mínimos | Primera opción | Alternativas | Evitar o condicionar |
|---|---|---|---|---|
| Valor exacto o lookup | 1+ medidas, claves | tabla, texto KPI | tabla con barras en celda | gráfica si la precisión individual es la tarea |
| Comparar magnitudes | categoría + medida | barras ordenadas, dot plot | lollipop, small multiples | pastel; barras con eje truncado |
| Comparar dos estados | categoría + 2 medidas | dot plot conectado, slopegraph | barras agrupadas | demasiadas series o categorías sin separar |
| Actual vs meta | medida + objetivo | bullet chart, barra con referencia | variance bar | gauge si solo repite un número |
| Desviación respecto a cero/meta | categoría + desviación | barras divergentes | dot plot divergente | paleta secuencial sin punto neutral |
| Evolución temporal continua | tiempo + medida | línea | área solo si la magnitud acumulada importa | barras para series densas; eje temporal desordenado |
| Totales por periodos discretos | periodo + medida | barras/columnas | línea si la continuidad es válida | conectar periodos sin relación continua |
| Cambio de ranking | tiempo + categoría + rango | bump chart | slopegraph para 2 periodos | más series de las que se pueden seguir |
| Calendario o eventos | inicio/fin o instancias | Gantt, timeline, instance chart | calendario heatmap | línea para eventos discretos |
| Distribución de una medida | muchas observaciones numéricas | histograma | densidad, ECDF, dot/strip plot | barras de categorías; bins arbitrarios sin revisión |
| Comparar distribuciones | grupo + medida | boxplot/violín + puntos | histogramas o densidades small multiple | promedios sin dispersión ni n |
| Relación entre 2 medidas | x numérico + y numérico | scatterplot | hexbin/densidad 2D si hay sobreposición | línea si x no es secuencial |
| Relación con tercera medida | x + y + tamaño cuantitativos | bubble plot con escala de área | facetas o color si es más legible | radio proporcional al valor; burbujas saturadas |
| Matriz de dos dimensiones | 2 categorías + medida | heatmap | matrix chart, tabla | arcoíris; demasiados valores sin agrupación |
| Parte de un total | partes no negativas del mismo total | barras apiladas, 100% apiladas | waffle; pastel con 2–5 partes | pastel con muchas partes; totales incompatibles |
| Composición jerárquica | jerarquía + medida aditiva | treemap | sunburst, icicle | si la comparación exacta domina |
| Jerarquía estructural | nodos padre-hijo | dendrograma/árbol | icicle | treemap si no hay medida para área |
| Flujo entre etapas/nodos | origen + destino + magnitud | Sankey/alluvial | flow map, chord solo para relaciones densas | Sankey sin conservación o con cruces excesivos |
| Red o conexiones | nodos + enlaces | network diagram | matriz de adyacencia | “hairball” sin filtros ni agrupación |
| Conteo por ubicación | geometría/punto + conteo | símbolos proporcionales o dot map | hexbin map | coropleta de conteos brutos |
| Tasa por región | región + tasa normalizada | coropleta | grid map | comparar áreas muy dispares sin nota |
| Superficie continua | coordenadas + medida continua | isarithmic/contour map | raster heatmap | coropleta por límites administrativos arbitrarios |
| Cómo se forma un total | componentes ordenados +/- | waterfall | barras divergentes | si el orden no construye un total |
| Perfil multivariable | entidad + varias medidas comparables | dot plots o small multiples | radar solo con orden y escalas defendibles | superponer muchos radares |

## 3. Reglas por familia

### Comparación categórica

- Ordenar por valor, lógica, tiempo o jerarquía; no dejar orden alfabético por defecto.
- Usar horizontal cuando las etiquetas sean largas.
- Mantener una base común y cero en barras.
- Preferir small multiples frente a apilados cuando la comparación entre subgrupos sea prioritaria.

### Tendencia temporal

- Mostrar intervalos regulares y distinguir huecos de ceros.
- No suavizar de manera que invente valores o puntos de giro.
- Limitar el número de líneas destacadas; atenuar o facetar el resto.
- Anotar eventos que expliquen cambios relevantes sin afirmar causalidad automática.

### Distribución

- Reportar n y, cuando aplique, mediana, intervalos o percentiles.
- Probar varios anchos de bin; el histograma puede cambiar de forma con el binning.
- Mostrar puntos reales cuando el tamaño de muestra lo permita.
- No comparar boxplots con escalas distintas.

### Relación

- Revisar outliers, subgrupos y rango antes de calcular o dibujar tendencia.
- Etiquetar unidades y, si se usa logaritmo, declararlo claramente.
- Indicar fuerza/incertidumbre del ajuste cuando sea relevante.
- No usar tamaño y color para variables adicionales si bloquean la lectura principal.

### Parte-todo

- Verificar que las partes sean mutuamente excluyentes, exhaustivas y del mismo total.
- No incluir negativos en pastel, donut, waffle o 100% apilado.
- En apilados, solo el primer segmento tiene una línea base común; facetar si todos deben compararse.

### Geografía

- Elegir mapa solo cuando la ubicación sea parte de la pregunta.
- Normalizar conteos para coropletas y declarar denominador.
- Usar proyección y límites adecuados al territorio; incluir “sin datos”.
- No confundir densidad visual con importancia estadística.

## 4. Codificación y escalas

Priorizar para comparación cuantitativa:

1. posición sobre escala común;
2. longitud con base común;
3. posición sobre escalas no alineadas;
4. área correctamente escalada;
5. ángulo;
6. volumen, que debe evitarse para precisión.

Usar tono de color para categorías; luminosidad o saturación ordenada para valores. Usar escala divergente solo cuando exista un centro significativo. Mantener el dominio consistente entre paneles comparables.

## 5. Casos que requieren cautela

- `Pastel/donut`: máximo aproximado de cinco partes, diferencias amplias y total inequívoco.
- `Radar/polar`: usar solo si la forma radial o el orden cíclico tiene significado y las escalas son comparables.
- `Dual axis`: preferir dos paneles alineados o normalizar; si se conserva, marcar escalas y evitar sugerir correlación.
- `Área/streamgraph`: apropiado para composición y patrón global, no para precisión individual.
- `Word cloud`: usar como recurso editorial, nunca como evidencia de frecuencia precisa.
- `3D`: rechazar si la profundidad distorsiona posición, longitud, área u oclusión.
- `Animación`: aportar cambio o causalidad temporal; ofrecer pausa y alternativa estática.

