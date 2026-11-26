# Entrega Lincoln: cierre del 25 de noviembre de 2026

Guía del estudiante, versión 30/oct/2026, sección de entregables. No entregar esta lista como sustituto del informe.

| Entregable | Qué contiene | Estado |
|---|---|---|
| Informe técnico y de negocio | 8–12 páginas de cuerpo; arquitectura, decisiones, controles, resultados, reflexión y referencias; anexos aparte | PDF de revisión de 9 páginas; actualizar con integración y pruebas finales |
| Repositorio GitHub | Código, instrucciones de reproducción, dependencias, datos sintéticos y versiones | Repositorio existente; cambios nuevos sujetos a Actions |
| ZIP del mismo commit | Copia del repositorio, informe, manifiesto; SKILL.md, scripts, referencias y ejemplos de todos los skills utilizados | Se genera en Actions; sustituir cualquier ZIP antiguo |
| Enlaces operativos | GitHub Pages, Actions correcto y bloqueo deliberado, bot y acceso sin secretos | Enlaces disponibles; faltan pruebas finales de canales |
| Exports de n8n | Roles, contratos, prompts, skills, loops y configuración sin credenciales | v04 ejecutado; v05 y tarea programada candidatos inactivos |
| Configuración/export de ElevenLabs | Voz, idioma, saludo, herramientas, conocimiento, dominios y recreación; pruebas | Consulta histórica por voz exitosa; cerrar export y evidencia vigente |
| Costos y pruebas | CSV/XLSX, tarifas, proyecciones, matriz de casos, evidencias, diccionario y muestra | Existen archivos; completar medidas por llamada y casos exigidos |
| Video y defensa individual | Video de 5–8 minutos; demo de hasta 12 minutos; declaración de IA y licencias | Requiere grabación de Sofía |

No se exige una presentación como archivo independiente. Puede utilizarse como apoyo visual de la defensa; no reemplaza video ni informe.

## Dos skills específicos

`preparar-apoyo-lincoln` v1.0.0: negocio, validación de fuentes y propuesta 50/50. Creado, instalado y probado con dos casos válidos y uno rechazado. Incluye contrato, recursos y CLI sin APIs.

`revisar-apoyo-lincoln` v1.0.1: revisión de calidad y seguridad. Su uso local e integración aislada ya tienen evidencia. El constructor `src/preparar_workflow_v05.py` lee ambos SKILL.md y embebe las instrucciones y sus SHA256 en agentes 3 y 4. Un nodo registra la carga en el caso. Esto demuestra carga desde archivos al construir el export; aún no demuestra ejecución de v05 en n8n.

`cotizar-tokens-ia` y `vizdata` conservan sus evidencias auxiliares de uso. No se presentan como reemplazos de los dos skills específicos. Revisar también el recurso pendiente del tokenizador señalado en la auditoría.

## Dos loops: existencia frente a acreditación

1. Calidad: evaluar cálculo, diagnosticar diferencias, corregir y volver a validar; máximo tres vueltas y diez segundos en revisión determinista. Pruebas locales V1 errónea → V2 corregida. Una ejecución integral v04, folio LIN-53-1, superó la revisión en primera vuelta. Falta demostrar V1→V2 dentro del flujo operativo vigente y registrar costo adicional.
2. Seguridad y costo: autorizar, admitir presupuesto, reservar, ejecutar, registrar/reconciliar consumo y continuar o detener. Implementación SQLite y pruebas locales disponibles, incluida concurrencia. Falta integrar y acreditar el bloqueo monetario y la deduplicación persistente antes del modelo en n8n. `limite_costo_usd:0.25` por sí solo no corta gasto de Gateway.

No afirmar que ambos loops cumplen integralmente mientras el segundo siga local.

## Tarea programada propuesta y construida

`exports/Lincoln_Vencimientos_Programados_PUBLICO.json`: Schedule Trigger cada cinco minutos, zona America/Mexico_City, lectura de pendientes y transición a VENCIDO solo de propuestas simuladas cuya fecha venció. Comparación condicional al actualizar: ID, folio, versión, estado pendiente, decisión vacía, vencimiento y propuesta original idénticos. No usa modelos ni Telegram; no aprueba, reserva, libera ni modifica presupuesto financiero. No interviene en casos reales.

El selector evita fechas inválidas, propuestas corruptas y aprobaciones existentes. Repetir una transición no genera otra. La actualización compara la instantánea, para no sobrescribir una decisión concurrente. Hay que comprobar en el servicio la transición y la ausencia de filas actualizadas cuando cambie la instantánea. El registro de ejecuciones de n8n conserva la evidencia; el JSON de la propuesta añade fecha e ID de vencimiento.

**Estado: export candidato, inactivo; no programado en la cuenta todavía.** La guía menciona una tarea programada sin fijar frecuencia. Cinco minutos limita a aproximadamente cinco minutos la demora de marcado, sujeto al funcionamiento del servicio. Consume ejecuciones de n8n, aunque no tokens; durante la demostración puede probarse manualmente antes de activar el horario. No dejarlo activo indefinidamente durante una prueba gratuita.

## Orden de cierre

1. Importar v05 como candidato sin publicar otro Telegram Trigger; configurar referencias de tablas y credenciales existentes.
2. Importar tarea programada, asociar tabla de casos, probar sin modelos y activar su horario solo tras verificar filtros.
3. Integrar guardián/deduplicación y consulta `/estado`; ejecutar la matriz de pruebas con evidencia real de al menos tres casos completos y un error/rechazo.
4. Exportar configuración actual de ElevenLabs y completar prueba de voz enlazada al caso, accesibilidad y pantalla móvil.
5. Completar costos medidos y estimados separados, informe, reflexión personal y manifiesto del mismo commit.
6. Sofía graba video y realiza defensa; descargar ZIP final únicamente después de Actions correcto y comprobar que coincide con el commit del informe.

## Intervención concreta necesaria para continuar en las cuentas

En esta sesión no hay herramienta de navegador conectada a n8n o ElevenLabs. Para editar sus configuraciones hace falta restablecer el navegador compartido. Los enlaces por sí solos no conceden control de una sesión autenticada. Los candidatos y pruebas locales pueden completarse sin ese acceso y sin gastar créditos Gateway.
