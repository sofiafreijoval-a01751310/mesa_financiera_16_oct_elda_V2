# Panel de demostración Lincoln

Aplicación estática en `web/`, con exportación sanitizada de n8n. Datos ficticios v0.1. No es un portal oficial de Lincoln.

## Fuente y alcance

`datos/panel_proyeccion_autorizada.json` conserva solo folio, distribuidor, estado, versión, monto, fechas y clasificación de prueba. La proyección se revisó sobre la tabla de casos de n8n; no publica chats, usuarios, solicitudes completas ni credenciales. `python3 src/exportar_panel.py` produce el JSON público. La fecha de exportación es explícita. La actualización es manual y una exportación de más de 24 horas presenta advertencia.

## Indicadores

- Apoyo aprobado simulado / presupuesto nacional de 5 millones MXN. No equivale a gasto pagado.
- Tiempo promedio creación-decisión en minutos, con n visible. Incluye espera humana.
- Aprobados / (aprobados + rechazados), con n visible.

La prueba técnica de vencimiento puede visualizarse, pero nunca participa en KPI. Las asignaciones por distribuidor y el simulador usan saldos iniciales v0.1; no representan saldo operativo actualizado. Las barras comienzan en cero, se ordenan por monto y no alteran su escala con filtros de casos.

## Interacción y accesibilidad

Filtros por distribuidor, estado y folio; restablecer; estado vacío; descarga de la proyección; vista de 8 o 19 distribuidores; simulación 50/50 sin reservas ni aprobaciones. Etiquetas y mensajes accesibles, controles nativos, foco visible. El componente de voz externo se carga solo tras consentimiento y requiere que la persona inicie la conversación. Ofrece alternativa de Telegram. La prueba de voz desde Pages, el teclado y la revisión visual a 390/1366 px siguen pendientes de comprobación interactiva.

## Despliegue y control

El workflow raíz `.github/workflows/lincoln-validacion.yml` valida base, guardianes, exportaciones, visualización, proyección pública y web antes de publicar. `publicar` depende de `validar` y solo opera en main; un fallo impide desplegar la nueva versión. Publica únicamente `lincoln_proyecto/web`, sin scripts de trabajo ni exportaciones privadas. Pages está configurado con origen GitHub Actions. La ejecución 45326466063 confirmó validación y publicación correctas. La URL de despliegue reportada por GitHub es https://sofiafreijoval-a01751310.github.io/mesa_financiera_16_oct_elda_V2/. La revisión visual independiente del sitio todavía está pendiente.

Pruebas: `python3 tests/validar_web.py` y `node tests/test_web.cjs` (12 casos). La ejecución 45514201989 detectó un presupuesto nacional de 5,000,001 en lugar de 5,000,000: validar falló y publicar quedó skipped. Se restauró exactamente el árbol validado en el commit c9298550ef49bc2a468cb3e5dfd99af20bd26905. Ver evidencias/pages_despliegue.json para la recuperación y sus enlaces.
