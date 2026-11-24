# Lincoln | Apoyos a Distribuidores - complemento reproducible

Sofía Freijo Valdovinos · AI Tools · Prof. Elda Morales.
Datos sintéticos académicos; corte23nov2026. Este subproyecto conserva separada la actividad Mesa Financiera de Batuta, Iris, Euler y Vera.

## Ejecutar sin llaves

Desde `lincoln_proyecto`, Python3.12 y Node22 (sin paquetes externos para las pruebas):

```bash
python3 tests/validar_base.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
node exports/verificar_workflow_v03.cjs
python3 src/run_demo.py
python3 skills/vizdata/scripts/audit_viz_spec.py docs/vizdata_brief.json --strict
python3 src/validar_paquete.py
```

Resultado esperado:base consistente;21pruebas Python;25JS;3casos convergen en2revisiones y1escala;loop recuperación3intentos. Las pruebas no llaman APIs ni mandan Telegram. `run_demo.py` regenera un ledger SQLite de DEMO; nunca apuntarlo a una base operativa.

## Contenido

- `skills/`:dos previos documentados y revisor nuevo reproducible.
- `src/`:guardianes, loops y prueba de paquete.
- `exports/`:respaldo n8n v03 sin credenciales, inactivo y con usuario DEMO.
- `datos/`:base y PMA ficticios v0.1.
- `evidencias/`:dictámenes/trazas/reports de ejecución local.
- `costos/`:conteos medidos de texto estático, supuestos, tarifas y estimaciones.
- `docs/`:costos, ciberseguridad, loops, VizData y pendientes de cierre.

No importar el export sobre un flujo activo sin configurar credenciales/tablas/identidad:es copia pública para revisión. Los guardianes nuevos NO están desplegados en n8n. Los controles financieros requieren una cota máxima por llamada calculada en servidor y una reserva transaccional antes del modelo. El gasto real no está disponible.

El tokenizador binario original permanece en la instalación personal de cotizar-tokens-ia. Su salida medida se conserva con hashes. El script cotizar.py copiado reproduce los cálculos por las entradas JSON, sin necesitar el tokenizador.

Ver `docs/cierre_y_evidencias.md` para pendientes de rúbrica y límites. Ningún dictamen numérico aprueba apoyos ni mueve presupuesto.
