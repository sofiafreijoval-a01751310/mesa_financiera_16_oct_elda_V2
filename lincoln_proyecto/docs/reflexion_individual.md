# Reflexión individual

Este proyecto me ayuda a evaluar si conviene apoyar las acciones que un distribuidor propone realizar en su localidad para generar prospectos y vender más. Lo relaciono directamente con mi trabajo en Ford, porque permite revisar solicitudes con criterios consistentes, consultar el presupuesto disponible y preparar una propuesta que una persona pueda decidir. El ejercicio no demuestra que un evento cause más ventas; esa efectividad tendría que medirse después.

Cada agente aportó una función distinta. El primero revisó que la solicitud tuviera la información necesaria; el segundo consultó ventas, mercado y presupuesto; el tercero calculó la propuesta y ajustó el alcance cuando el saldo era insuficiente; y el cuarto revisó cifras y reglas. El orquestador coordinó sus entregas. Separar estas funciones me ayudó a entender que una respuesta útil depende de datos, cálculos y revisión, además de la redacción del modelo.

La aprobación humana fue un control importante. Si el saldo obligaba a reducir el alcance, el sistema pedía aceptar expresamente ese ajuste. En las pruebas bloqueó una aprobación sin esa aceptación, rechazó una solicitud vencida e impidió decidir por segunda vez un caso ya aprobado. Así, la propuesta del sistema no sustituye la decisión de la persona responsable ni ejecuta un pago.

La parte más costosa para mí fue consolidar los componentes y conseguir que funcionaran juntos. El mayor esfuerzo estuvo en conectar n8n, Telegram, los agentes, el sitio y la voz, conservar el mismo folio y corregir los errores de integración. Me refiero al tiempo y al esfuerzo de desarrollo: todavía no tengo una conciliación monetaria completa que permita afirmar cuál componente consumió más dinero.

Con diez veces más solicitudes, necesitaría controlar mejor los costos, los tiempos de respuesta y el trabajo simultáneo. Sería indispensable completar la deduplicación antes del modelo y el límite automático de gasto por llamada. También organizaría los casos pendientes para que la revisión humana no se convierta en un cuello de botella. No asumiría que los costos crecerán de forma idéntica sin medir reintentos, tamaño de las solicitudes y duración de las consultas de voz.

Antes de utilizar datos reales en Ford, validaría los permisos para usar la información y conectar servicios externos, los presupuestos actualizados y las reglas oficiales de apoyo. Compararía los cálculos con casos revisados por el equipo y comprobaría la protección de datos y credenciales. Mantendría la aprobación humana y comenzaría con una prueba controlada, sin pagos ni cambios automáticos al presupuesto. Esta versión usa datos sintéticos y todavía requiere completar controles técnicos antes de trasladarse a una operación real.

---
Redacción asistida por IA a partir de la experiencia expresada por Sofía y las respuestas que confirmó en el chat.
