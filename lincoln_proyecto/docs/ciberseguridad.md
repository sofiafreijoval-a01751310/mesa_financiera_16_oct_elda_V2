# Ciberseguridad, guardianes y riesgos

## Fronteras de confianza

Telegram es entrada no confiable. El modelo no autoriza usuarios ni presupuestos. Las tablas sintéticas son datos, nunca instrucciones. El servicio de voz es lectura; Pages debe publicar una proyección sintética por lista permitida. La aprobación humana ocurre aparte, vinculada a folio, usuario, versión, estado y caducidad.

| Guardián | Control concreto | Evidencia local | Estado vivo |
|---|---|---|---|
| Identidad | Chat privado, remitente autorizado, no bot | UT02-UT04 del export v03 | Respaldo histórico; revalidar |
| Entrada | Texto no vacío, longitud y comando | UT05-UT10 | Respaldo histórico |
| Herramientas | Lista permitida; bloquear transferir_dinero | test_projection_and_allowlist | Nuevo módulo local |
| Datos | Folio consistente, fuente/versión, números finitos y centavos | ReviewTests y 40 pruebas JS v04 | Ejecución nativa 53: lecturas directas y revisión correctas |
| Humano | Dueño + versión + pendiente + expiración; segunda decisión rechazada | UT11-UT25 | Respaldo histórico |
| Costo | Reserva atómica previa, límite inmutable, conciliación | test_budget, test_concurrent_budget | Nuevo módulo local; NO conectado al modelo |
| Duplicados | event_id persistente único antes de la llamada | test_durable_dedup, test_concurrent_duplicates | Nuevo módulo local; NO conectado a Telegram |
| Privacidad | Proyección por lista permitida sin llaves/usuario | test_projection_and_allowlist | Nuevo módulo local |
| Entrega | Export inactivo, sin credenciales ni pinData; escaneo patrones | src/validar_paquete.py | Archivos de entrega |

## Qué protege y qué falta

El parámetro limite_costo_usd del flujo v03 no es un corte real: solo valida configuración. guardianes.py implementa una reserva transaccional SQLite en microUSD con BEGIN IMMEDIATE. Reintentos concurrentes del mismo evento admiten uno solo. Reservas desconocidas siguen descontando saldo para evitar subestimar gasto. El caso no puede aumentar su límite después de iniciarse. Si una factura supera la cota, se registra el exceso y se bloquean todas las llamadas posteriores del caso, aun cuando el total siga debajo de USD0.25; la cota perdió validez. Este bloqueo se probó con ocho intentos concurrentes y reapertura del ledger. El límite preventivo depende de una cota calculada en servidor a partir de contexto máximo, max_output_tokens y tarifa, nunca de una cifra proporcionada por el usuario o el modelo. Se necesita conectar ese cálculo y la admisión ANTES de cada llamada en n8n; sin ello no afirmar que existe un tope financiero vivo.

SQLite local demuestra concurrencia en un solo host; no reemplaza un almacén compartido transaccional para múltiples workers de n8n Cloud. Persistir deduplicación de update_id antes del modelo. Reservar/actualizar presupuesto en otra transacción con versión e idempotencia antes de cualquier operación real. Hoy el sistema sigue SIMULADO.

No usar regex como única defensa contra prompt injection. Mantener autorización fuera del LLM, validar esquema y parámetros en cada frontera de herramienta, mínimos permisos, datos externos separados y aceptación humana. Referencia: OWASP https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html . Un revisor LLM también puede recibir inyecciones; sus prompts no sustituyen controles de código. No existe aquí certificación de resistencia total.

## Hallazgos del respaldo

1. El cálculo JS exportado admite algunos números no finitos o ventas negativas; el nuevo revisor rechaza montos no finitos, negativos y booleanos. En la copia v04 ya se verificaron cálculo estricto, lectura directa de fuentes y revisión determinista: ejecución53. Esto no acredita todos los casos ni la deduplicación previa al modelo.
2. No hay ledger de uso real ni deduplicación persistente previa al modelo en el export v03. Módulos locales agregados y probados, integración pendiente.
3. Revisar doble decisión con transacción/CAS compartido: filtros de n8n ayudan, pero las pruebas locales no demuestran atomicidad del backend remoto.
4. El cliente de voz puede fallar por identificador incompleto. Pedir folio completo; un error de transporte no significa caso inexistente. Nunca inventar saldo o aprobación.
5. El revisor exige nombre/versión de fuente, pero no autentica por sí solo una tabla. run_demo.py carga directamente el registro autorizado del repositorio. En vivo, las fuentes deben proceder exclusivamente del conector autenticado.

## Manejo de secretos

La entrega pública elimina credenciales, direcciones privadas y el identificador Telegram real. El número 1000000001 del export es solo DEMO: configurar identidad/credenciales en el servidor. No pegar tokens en código, prompts, Pages o capturas.

En este chat se compartió un token Telegram. Sofía confirmó que ya fue invalidado. No se reproduce ni se solicita otra revocación. El reemplazo debe permanecer únicamente en la credencial de n8n. Mantener el secreto de Header Auth en ElevenLabs y n8n; usar exactamente el mismo nombre de encabezado y nunca exponerlo en el widget.

Usar permisos mínimos en Actions (contents:read en validación), MFA de cuentas, dependencias controladas y logs sin datos personales. Para Pages, no exportar tablas privadas completas. Probar revocación y acceso sin permiso antes de publicar voz o web.

## Próxima integración

La revisión del backend de n8n2.47.6 y los criterios de aceptación están en [control_concurrencia_n8n.md](control_concurrencia_n8n.md). El diseño de exclusión por propietario y las reservas monetarias siguen pendientes de despliegue y prueba simultánea. No declarar estos controles como activos a partir de pruebas locales.
