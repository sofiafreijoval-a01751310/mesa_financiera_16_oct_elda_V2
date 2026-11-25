# Workflow candidato v04 - revisión antes del registro

Estado: preparado y probado localmente; no importado, ejecutado ni publicado en n8n. No sustituye la prueba integral de los cinco agentes. El original de 28 nodos permanece intacto. La copia tiene 35 nodos y se entrega inactiva.

## Cambios implementados

1. `calcular_propuesta` rechaza strings, booleanos, no finitos, negativos, más de dos decimales, saldo mayor a asignación, ventas negativas/fraccionarias y segmentos duplicados o inválidos. Calcula en centavos; un centavo indivisible obliga a reducir el alcance manteniendo aportaciones iguales.
2. Las herramientas de consulta usan el distribuidor canónico de Inicializar caso; el modelo no elige otro distribuidor. Las lecturas admiten una fila adicional para detectar duplicados.
3. La salida final del orquestador debe conservar cuatro objetos completos, folio y estados. La comprobación de moneda, fecha, audiencia, modelo y campos faltantes ocurre en código antes de guardar.
4. Tres nodos Data Table vuelven a leer las fuentes directamente antes del registro. Verifican cardinalidad 1/1/4, fuente SINTETICA_ACADEMICA, versión 0.1, periodos, conciliación del saldo y asignación contra ventas. No confían en las cifras copiadas por el modelo.
5. El loop determinista contrasta la propuesta con esas lecturas, corrige exclusivamente valores derivados y aceptación, hasta tres revisiones/10 s. Una fuente inválida bloquea; una aprobación o modificación de presupuesto declarada por el modelo bloquea. La traza se conserva en `resultado.control_determinista`.
6. El mensaje financiero final se reconstruye con cifras verificadas; no reproduce el resumen financiero libre del modelo.
7. La decisión de aprobar exige control determinista v04. Un caso histórico sin ese control requiere nueva evaluación. Para alcance reducido: `/aprobar FOLIO VERSION ACEPTAR_AJUSTE`. Un comando normal no implica aceptación del ajuste. Rechazar no exige aceptación.
8. La prueba manual guarda un caso pero no intenta enviar un resultado a Telegram sin destinatario autorizado. El acceso MCP queda deshabilitado en la copia.

## Uso de los archivos

- `Lincoln_Apoyos_v04_PARA_IMPORTAR.json`: copia privada para la misma instancia. Conserva las referencias de sus credenciales y tablas; no contiene sus valores secretos. No subir a un repositorio público.
- `exports/Lincoln_Apoyos_v04_PUBLICO.json`: copia de revisión sin credenciales, con tablas a configurar e identidad DEMO. No importar sobre el bot actual.
- `src/preparar_workflow_v04.py ARCHIVO_ORIGINAL.json`: reproduce las modificaciones. Sin argumento usa el respaldo público v03 y produce una copia que requiere configurar tablas y credenciales.

Crear un workflow nuevo e importar desde archivo; mantenerlo inactivo. Antes de ejecutar, confirmar que las tablas elegidas tienen los nombres de columnas del contrato existente y que las credenciales enlazan a la cuenta correcta. La copia se creó con los tipos/versiones de nodos observados en el export aportado; la importación real aún no se verificó.

## Límites que siguen abiertos

- El campo limite_costo_usd=0.25 no es un tope facturable. maxIterations, timeout y maxRetries acotan ejecución, pero no implementan reserva y conciliación por llamada. Hace falta conectar el control de costo al proveedor o a un intermediario con registro transaccional antes de cada llamada. No ejecutar modelos suponiendo que ese campo protege el saldo.
- No se añadió una falsa deduplicación basada en leer y después insertar: dos workers podrían admitir el mismo evento. La admisión del evento y su reserva deben ser atómicas en un almacén compartido antes del modelo.
- La comprobación de decisión y el update condicionado se preservan; la atomicidad remota y la respuesta ante carreras requieren pruebas en el backend vigente. Este cambio no mueve presupuestos.
- La extracción de datos de la solicitud aún depende del agente 1. El código comprueba su contrato; no certifica que cada campo se extrajo fielmente del texto original.
- La adaptación JavaScript reutiliza el criterio del revisor de negocio, pero no equivale a ejecutar el script Python personal dentro de n8n. La prueba aislada anterior sigue siendo evidencia separada.
- No modifica el canal de voz. Debe revalidarse contra el nuevo registro y el formato ampliado.

## Validación reproducible

`node tests/test_workflow_v04.cjs`: 37 pruebas locales sobre el JavaScript y grafo exportados, incluyendo V1→V2, fuentes inválidas, rechazo de aprobación automática, folios, comandos y aceptación de alcance. No hay llamadas API ni mensajes en estas pruebas. Los fixtures de mercado se transforman de la base sintética local al esquema esperado en n8n; no sustituyen una inspección de las tablas vivas.

Documentación técnica consultada: https://github.com/n8n-io/n8n-docs/blob/main/docs/integrations/builtin/core-nodes/n8n-nodes-base.datatable/rows.md y https://github.com/n8n-io/skills/blob/main/skills/n8n-data-tables-official/references/OPERATIONS.md.
