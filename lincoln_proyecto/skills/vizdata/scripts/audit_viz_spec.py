#!/usr/bin/env python3
"""Audit a VizData JSON specification and report incompatible chart choices."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


ALIASES = {
    "column": "bar",
    "column_chart": "bar",
    "bar_chart": "bar",
    "line_chart": "line",
    "pie_chart": "pie",
    "donut_chart": "donut",
    "scatterplot": "scatter",
    "scatter_plot": "scatter",
    "bubble_chart": "bubble",
    "box_plot": "boxplot",
    "choropleth_map": "choropleth",
    "proportional_symbol_map": "symbol_map",
    "sankey_diagram": "sankey",
    "word_cloud": "wordcloud",
    "dual_axis": "dual-axis",
}


def norm(value: Any) -> str:
    return str(value or "").strip().lower().replace(" ", "_").replace("-", "_")


def finding(chart_id: str, severity: str, code: str, message: str, fix: str) -> dict[str, str]:
    return {"chart": chart_id, "severity": severity, "code": code, "message": message, "fix": fix}


def has_field(fields: dict[str, Any], *names: str) -> bool:
    return any(bool(fields.get(name)) for name in names)


def audit_chart(chart: dict[str, Any]) -> list[dict[str, str]]:
    cid = str(chart.get("id") or "unnamed")
    raw_type = norm(chart.get("chart_type"))
    chart_type = ALIASES.get(raw_type, raw_type)
    purpose = norm(chart.get("purpose"))
    fields = chart.get("fields") if isinstance(chart.get("fields"), dict) else {}
    cardinality = chart.get("category_cardinality")
    series_count = chart.get("series_count")
    has_negative = bool(chart.get("has_negative"))
    part_to_whole = bool(chart.get("part_to_whole"))
    axis_start = chart.get("axis_start")
    results: list[dict[str, str]] = []

    if not chart_type or not purpose:
        results.append(finding(cid, "error", "missing-intent", "Falta chart_type o purpose.", "Declarar la gráfica y la pregunta analítica antes de diseñar."))
        return results

    if "3d" in chart_type:
        results.append(finding(cid, "error", "3d-distortion", "La codificación 3D puede distorsionar magnitud y ocluir marcas.", "Usar posición o longitud en 2D."))

    if chart_type == "bar":
        if purpose not in {"comparison", "deviation", "trend", "ranking", "actual_vs_target", "range"}:
            results.append(finding(cid, "warning", "bar-purpose", "La barra no es la primera opción para esta tarea.", "Revisar la matriz de selección por propósito."))
        if axis_start is not None and isinstance(axis_start, (int, float)) and not math.isclose(float(axis_start), 0.0):
            results.append(finding(cid, "error", "bar-zero", "Las barras no comienzan en cero.", "Establecer axis_start en 0 o cambiar a dot plot y justificar el dominio."))

    if chart_type == "line":
        if purpose not in {"trend", "time", "ranking"}:
            results.append(finding(cid, "warning", "line-purpose", "Una línea implica orden o continuidad.", "Usar línea solo con tiempo/secuencia; para categorías usar barras o puntos."))
        if not has_field(fields, "time", "ordered", "sequence"):
            results.append(finding(cid, "error", "line-order", "No se declaró un campo temporal u ordenado.", "Añadir el campo de tiempo/secuencia o elegir otra gráfica."))
        if isinstance(series_count, int) and series_count > 8:
            results.append(finding(cid, "warning", "line-overload", "Hay demasiadas series para seguimiento visual fiable.", "Destacar pocas series, filtrar o usar small multiples."))

    if chart_type in {"pie", "donut", "waffle"}:
        if purpose not in {"composition", "part_to_whole"} or not part_to_whole:
            results.append(finding(cid, "error", "whole-invalid", "La gráfica requiere partes de un único total válido.", "Verificar exclusividad y exhaustividad o usar barras."))
        if has_negative:
            results.append(finding(cid, "error", "whole-negative", "Una composición circular/unidad no admite valores negativos.", "Usar barras divergentes o waterfall según la tarea."))
        if isinstance(cardinality, int) and cardinality > 5:
            results.append(finding(cid, "warning", "whole-cardinality", "Demasiadas partes dificultan comparar ángulos o áreas.", "Usar barras ordenadas o agrupar categorías justificadamente."))

    if chart_type in {"stacked_bar", "stacked_area", "treemap", "sunburst"} and not part_to_whole:
        results.append(finding(cid, "error", "composition-required", "La gráfica codifica composición, pero part_to_whole es falso.", "Confirmar un total común o cambiar a comparación/facetas."))
    if chart_type in {"stacked_bar", "stacked_area", "treemap", "sunburst"} and has_negative:
        results.append(finding(cid, "warning", "composition-negative", "Los negativos rompen la lectura aditiva de composición.", "Separar signos o usar barras divergentes/waterfall."))

    if chart_type == "scatter":
        if purpose not in {"relationship", "correlation"}:
            results.append(finding(cid, "warning", "scatter-purpose", "La dispersión está optimizada para relaciones entre medidas.", "Revisar si la pregunta es realmente relacional."))
        if not (has_field(fields, "x") and has_field(fields, "y")):
            results.append(finding(cid, "error", "scatter-fields", "Faltan campos cuantitativos x e y.", "Declarar dos medidas cuantitativas."))

    if chart_type == "bubble":
        if not (has_field(fields, "x") and has_field(fields, "y") and has_field(fields, "size")):
            results.append(finding(cid, "error", "bubble-fields", "La burbuja requiere x, y y size cuantitativos.", "Declarar tres medidas o usar scatterplot."))
        results.append(finding(cid, "warning", "bubble-area", "El tamaño debe codificarse por área, no por radio.", "Verificar escala de área y limitar solapamientos."))

    if chart_type in {"histogram", "density", "boxplot", "violin", "ecdf"}:
        if purpose != "distribution":
            results.append(finding(cid, "warning", "distribution-purpose", "Esta gráfica muestra forma o dispersión de una distribución.", "Definir purpose como distribution o elegir otra gráfica."))
        if not has_field(fields, "measure", "value", "x"):
            results.append(finding(cid, "error", "distribution-field", "Falta una medida cuantitativa.", "Declarar el campo numérico y el tamaño de muestra."))

    if chart_type == "choropleth":
        if purpose not in {"geospatial", "spatial"}:
            results.append(finding(cid, "warning", "map-purpose", "El mapa solo aporta valor si el lugar es parte de la pregunta.", "Usar barras si solo se comparan regiones."))
        if not bool(chart.get("normalized_rate")):
            results.append(finding(cid, "error", "choropleth-rate", "No se confirmó una tasa normalizada.", "Normalizar por un denominador relevante o usar símbolos proporcionales."))

    if chart_type == "symbol_map" and not has_field(fields, "location", "geometry"):
        results.append(finding(cid, "error", "map-location", "Falta ubicación o geometría.", "Declarar coordenadas/geometría y la medida de tamaño."))

    if chart_type == "heatmap" and not (has_field(fields, "row") and has_field(fields, "column") and has_field(fields, "measure", "value")):
        results.append(finding(cid, "error", "heatmap-fields", "El heatmap requiere fila, columna y medida.", "Declarar dos dimensiones y una medida, o usar tabla."))

    if chart_type in {"sankey", "alluvial"}:
        if purpose != "flow":
            results.append(finding(cid, "warning", "flow-purpose", "Sankey/alluvial representa flujos entre etapas o nodos.", "Definir purpose como flow o elegir otra gráfica."))
        if not (has_field(fields, "source") and has_field(fields, "target") and has_field(fields, "measure", "value")):
            results.append(finding(cid, "error", "flow-fields", "Faltan source, target y magnitud.", "Declarar los nodos y la medida de flujo."))

    if chart_type in {"radar", "polar"}:
        results.append(finding(cid, "warning", "radial-caution", "La forma radial dificulta comparaciones y depende del orden.", "Preferir dot plots/small multiples; conservar solo con escalas y orden significativos."))
    if chart_type in {"dual_axis", "dual-axis"}:
        results.append(finding(cid, "warning", "dual-axis-caution", "Dos ejes pueden sugerir relaciones sensibles al dominio elegido.", "Usar paneles alineados, normalización o justificar ambos dominios."))
    if chart_type in {"gauge", "speedometer"}:
        results.append(finding(cid, "warning", "gauge-space", "El gauge usa mucho espacio para poca información.", "Usar KPI con meta, bullet chart o barra de progreso."))
    if chart_type == "wordcloud":
        results.append(finding(cid, "warning", "wordcloud-analysis", "Una word cloud no permite comparar frecuencias con precisión.", "Usar barras de términos, tabla o análisis textual; dejar la nube como recurso editorial."))

    if not chart.get("source") and not chart.get("notes"):
        results.append(finding(cid, "info", "provenance", "No hay fuente o nota a nivel de gráfica.", "Añadir fuente, fecha de corte, unidad y transformaciones cuando apliquen."))

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="VizData JSON specification")
    parser.add_argument("--strict", action="store_true", help="Return nonzero for warnings as well as errors")
    args = parser.parse_args()

    try:
        data = json.loads(args.spec.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2

    charts = data.get("charts") if isinstance(data, dict) else None
    if not isinstance(charts, list) or not charts:
        print(json.dumps({"valid": False, "error": "La especificación debe contener una lista charts no vacía."}, ensure_ascii=False, indent=2))
        return 2

    findings = [item for chart in charts if isinstance(chart, dict) for item in audit_chart(chart)]
    counts = {level: sum(f["severity"] == level for f in findings) for level in ("error", "warning", "info")}
    valid = counts["error"] == 0 and (not args.strict or counts["warning"] == 0)
    print(json.dumps({"valid": valid, "summary": counts, "findings": findings}, ensure_ascii=False, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())

