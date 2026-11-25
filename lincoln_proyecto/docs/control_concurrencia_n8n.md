# Concurrencia y gasto: contrato de integración pendiente

Estado: diseño revisado; NO desplegado en n8n. No equivale a la protección SQLite local.

## Fuente revisada

Código oficial de n8n 2.47.6, versión observada en la instancia:
https://github.com/n8n-io/n8n/blob/n8n%402.47.6/packages/modules/data-table/backend/src/data-table-rows.repository.ts

updateRows aplica el filtro al propio UPDATE. PostgreSQL puede devolver filas afectadas mediante RETURNING. Otros motores pueden consultar identificadores antes y leer filas después; una fila devuelta no prueba por sí sola que esta ejecución ganó la exclusión. También debe comprobarse el propietario.

## Exclusión antes del modelo

1. Inicializar una única fila con identificador estable, estado LIBRE y propietario vacío. No usar get+insert como adquisición concurrente.
2. Adquirir con UPDATE condicionado por identificador y estado LIBRE, asignando OCUPADO y ejecución. Comprobar una sola fila cuyo propietario sea esta ejecución antes de llamar al modelo.
3. Dentro de la exclusión, consultar canal y update_id. Si ya fue registrado, omitir todas las llamadas. De lo contrario, persistir admisión antes del modelo.
4. Mantener exclusión durante procesamiento y registro. Liberar solo con UPDATE condicionado al propietario.
5. Ante caída o cancelación, conservar evento y bloquear reutilización automática. No liberar por TTL sin confirmar que terminó el trabajador anterior.
6. Aplicar el control a todas las rutas que comparten registro, incluidas decisiones y ensayos manuales.

Prueba viva requerida: dos ejecuciones simultáneas del mismo evento, una sola admisión y secuencia de llamadas; liberación por propietario y recuperación de caída. Dos llamadas secuenciales no acreditan concurrencia.

## Corte de USD0.25 con Gateway

El panel observado permite saldo, consumo por workflow/modelo y recarga automática. No se verificó una reserva por llamada ni un límite de USD0.25 por caso en la conexión actual. Una estimación de tokens o saldo agregado no sustituye ese control.

Se requieren cotas monetarias válidas del servidor, interceptar cada llamada del orquestador y especialistas, reservar antes y conciliar después. Las llamadas internas de herramientas también cuentan. El ledger SQLite implementa su control local, pero no intercepta Gateway de n8n.

Si una factura supera su cota, el guardián local bloquea llamadas posteriores aunque el total siga debajo de USD0.25. Se conserva el importe observado. Las pruebas cubren reapertura y ocho intentos concurrentes tras invalidación.

La ejecución nativa53 acredita cálculos, fuentes y revisión; no estos controles pendientes. USD0.16 es consumo Gateway agregado del workflow, no una factura exacta del caso53.
