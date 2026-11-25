# Arquitectura Lincoln y estado de integración

Mapa del proceso objetivo solicitado por la guía. El export v04 y la ejecución53 acreditan el recorrido manual de cuatro agentes, lectura de fuentes y revisión determinista. Las rutas de canal, aprobación, corrección, exportación pública y voz deben revalidarse de extremo a extremo. Las flechas de este diagrama describen conexiones y responsabilidades; no certifican pruebas pendientes.

```mermaid
flowchart TD
  T["Telegram: usuario autorizado"] --> V["Validar, enrutar y asignar folio"]
  V --> O["Orquestador"]
  O --> A1["Agente 1: solicitud"]
  A1 --> A2["Agente 2: fuentes"]
  F[("Ventas, presupuesto y PMA sintéticos")] --> A2
  A2 --> A3["Agente 3: propuesta"]
  A3 --> A4["Agente 4: revisión"]
  A4 -. "Corrección acotada" .-> A3
  A4 --> R["Validación y lectura directa de fuentes"]
  F --> R
  R --> D{"Resultado válido"}
  D -->|"No"| E["Aclaración o caso detenido"]
  D -->|"Sí"| H["Decisión humana: folio y versión"]
  H --> C[("Registro privado de casos")]
  C --> N["Notificación Telegram"]
  C --> X["Exportación sanitizada manual"]
  X --> G["Actions: validar y publicar"]
  G --> P["GitHub Pages"]
  P --> L["ElevenLabs con consentimiento"]
  L --> W["Herramienta autenticada de voz"]
  W --> C
  C --> W
  W --> L
```

- **Comprobado en53:** extracción, fuentes, cálculo, revisión, validación determinista y registro pendiente.
- **Fuera de ese recorrido manual:** ingreso/aprobación/notificación real de Telegram y voz desde Pages.
- **Pendiente antes del modelo:** deduplicación compartida y reserva/control monetario por llamada.
- Las operaciones empresariales siguen simuladas; ninguna revisión autoriza pagos.
