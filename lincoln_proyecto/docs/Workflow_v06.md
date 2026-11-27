# Revisión versionada v06

Cambio publicado el26/nov/2026 en el workflow operativo existente (título histórico Skills v05), versión Lincoln v06 revisión versionada. No importar una copia adicional para aplicar este cambio.

## Qué cambia

El revisor conserva caso_id y agrega en cada vuelta version_propuesta, valores evaluados, errores y resultado. Una V1 válida sigue en versión1; una corrección se vuelve a revisar como V2 del mismo folio. El registro exige que la traza sea consecutiva, corresponda al caso y termine válida. Solo entonces persiste la versión final del revisor. Las futuras decisiones humanas deben indicar esa versión.

Se conserva el contrato de control_determinista versión0.4 para compatibilidad con las comprobaciones de aprobación. Los montos se siguen calculando con las mismas fuentes y centavos. No se modificaron criterios comerciales ni controles de aprobación.

El resumen Telegram añade ACEPTAR_AJUSTE al comando cuando el alcance se redujo, para evitar que la persona copie una aprobación incompleta.

## Costo del loop

El nodo determinista no llama al modelo: cada vuelta y el total registran0llamadas y costo API USD0 para ese nodo. No representa el costo del orquestador, especialistas, infraestructura ni del caso completo. Límite de3revisiones y10segundos. Corte monetario de Gateway y deduplicación antes del modelo siguen pendientes.

## Evidencia y límite

44pruebas locales del export v06 pasan, incluidas V1 errónea→V2 correcta, conservación de folio, registro de versión2 y rechazo de traza manipulada. La publicación se observó en el editor n8n. Falta comprobar el cambio con una entrada integral nueva; la publicación por sí sola no acredita un caso vivo V1→V2.

Exports públicos y privados se generan inactivos mediante src/preparar_workflow_v06.py. No contiene credenciales nuevas ni altera registros anteriores.
