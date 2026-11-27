# Lincoln | Apoyos a Distribuidores

Sofía Freijo Valdovinos · AI Tools · Dra.Elda C.Morales. Corte27/nov/2026. Proyecto académico con datos sintéticos; no es una aprobación comercial de Lincoln/Ford. La actividad anterior Mesa Financiera permanece separada.

**Leer primero [índice de entrega](docs/ENTREGA_FINAL.md)** y [manual vigente](docs/manual_importacion.md). El ZIP identifica su commit exacto en MANIFIESTO.json. El video individual y ciertas pruebas de la matriz siguen pendientes; no se declara cumplimiento total.

## Objetivo y resultado

Evaluar si conviene apoyar una acción local de un distribuidor, con fuentes, cálculo50/50 y revisión antes de una decisión humana simulada. Telegram recibe y decide; n8n coordina un orquestador y cuatro especialistas; ElevenLabs consulta el mismo registro; Pages muestra una proyección sanitizada estática. No se efectúan pagos ni cambios de presupuesto.

## Estado probado

-140:entrada nueva Telegram, cuatro agentes, revisión V1→V2, registro22 PENDIENTE_APROBACION y respuesta confirmada por Sofía en75.68s. No aprobado automáticamente.
-123:recorrido manual equivalente,11llamadas OpenAI conciliadas;30414tokens entrada+4132salida, USD0.007041300 a tarifa estándar, sin infraestructura ni voz y sin afirmar factura.
-136:lote HTTP de3peticiones; corte por cota antes del proveedor y una admisión frente a un duplicado. Sus11reservas sintéticas no son cargos. No certifica toda carga concurrente.
-76:decisión humana77 y voz Pages confirmada,46s/630créditos.78 bloqueó segunda decisión. No atribuir esa decisión al caso140.
-Cron diario09h México publicado; transición e idempotencia manuales probadas. Actions tiene validación, bloqueo deliberado y recuperación documentados.

## Ejecutar sin llaves

Python3.12 y Node22. Desde lincoln_proyecto:

```bash
python3 src/run_checks.py
python3 src/run_demo.py
```

El primer comando ejecuta14comprobaciones locales. No llama modelos ni envía Telegram. El segundo recrea una base SQLite de DEMO; no apuntarlo a una base operativa. Resultado esperado:3casos convergentes en2revisiones,1escalado y recuperación acotada. La validación local no certifica canales externos.

Para regenerar informes:instalar requirements-report.txt, fuentes DejaVuSans y ejecutar `python3 src/generar_informe.py`, `python3 src/generar_guia_entrega.py`. `python3 src/consolidar_costos.py` reconstruye el registro sin inventar campos desconocidos. `src/empaquetar_entrega.py` usa exclusivamente fuentes del commit, no cambios locales sin commit.

## Importación actual

Usar exports/Lincoln_Proxy_OpenAI_CANDIDATO_PUBLICO.json, Lincoln_Apoyos_v07_CANDIDATO_PUBLICO.json, Lincoln_Consulta_Voz_PUBLICO.json y Lincoln_Vencimientos_Programados_PUBLICO.json. Los nombres CANDIDATO son antecedentes; las versiones nativas están publicadas. Todos los exports públicos son inactivos, sin credenciales ni datos fijados. v03-v06 conservan historia, no son la ruta inicial de esta entrega.

El manual detalla tablas, fila inicial del ledger, credenciales por función, identidad autorizada, publicación, parada y fallas. Crear un workflow vacío por export. Solo un receptor Telegram por bot. La API key real OpenAI va únicamente en el servidor; la contraseña del proxy es otra credencial. No publicar valores ni identidades.

## Navegar la entrega

| Carpeta | Contenido |
|---|---|
|skills/|cotizar-tokens-ia y VizData reutilizados; preparar-apoyo-lincoln y revisar-apoyo-lincoln específicos, con SKILL.md y recursos|
|src/|validaciones, loops, constructores y reproducción|
|exports/|workflows y configuración sanitizada ElevenLabs|
|datos/|muestras y PMA sintéticos v0.1; no datos oficiales|
|costos/|costos.csv, uso por petición, subtotales, voz y proyecciones históricas separadas|
|tests/|matriz P01-P14 con estados honestos y pruebas locales|
|evidencias/|trazas, observaciones nativas y antecedentes con fecha|
|docs/|informe fuente, arquitectura, manual, ciberseguridad, reflexión, guion e índice|
|web/|HTML, interfaz y proyección pública estática|

El tokenizador original conserva su instalación personal y aviso MIT; los conteos entregados tienen motor/hash. El cotizador copiado reproduce cálculos, no se presenta como un binario del tokenizador.

## Enlaces y acceso

[Pages](https://sofiafreijoval-a01751310.github.io/mesa_financiera_16_oct_elda_V2/) · [Actions](https://github.com/sofiafreijoval-a01751310/mesa_financiera_16_oct_elda_V2/actions) · bot @lincoln_apoyo_distribuidores_bot. El bot está restringido; solicitar autorización a Sofía por el canal privado del curso, sin compartir token. Pages usa exportación manual sanitizada seguida de commit y Actions, no tiempo real. Fechas, datos vacíos y fuentes se muestran en la interfaz.

## Límites que no deben omitirse

Video5–8min y defensa≤12min pendientes de Sofía. P01 aún requiere cierre humano del mismo caso nuevo;140 fue revisado y entregado, no decidido. Rechazo explícito, micrófono denegado y ciertos escenarios negativos nativos siguen en tests/pruebas.csv. El ledger no atribuye todavía agente/etapa por request; costos.csv lo declara. La factura total y el gasto de desarrollo son desconocidos. La voz pública maneja solo muestra sintética; no usarla para información privada.

El proxy exige revalidación de tarifa/modelo a partir de2026-12-04T00:00:00Z y entonces bloquea. Mantener servicios y cuotas disponibles durante la evaluación. No reiniciar ledger para borrar reservas ni publicar dos versiones del bot simultáneamente.

Declaración de IA y procedencia:docs/uso_ia_y_fuentes.md. Detalle histórico:docs/cierre_y_evidencias.md. Las fuentes originales conservan fecha y alcance; el índice actual prevalece para seleccionar archivos.
