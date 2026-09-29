"""Formato de valores para mostrar en pantalla (estilo argentino).

Se registran como filtros de Jinja:  {{ venta.total | moneda }}  ->  $ 1.234,50
"""

from __future__ import annotations

from datetime import date

from flask import Flask

MESES = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")


def _separadores_argentinos(texto: str) -> str:
    """'1,234.56' -> '1.234,56'"""
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formato_numero(valor, decimales: int = 0) -> str:
    if valor is None or valor == "":
        return "-"
    return _separadores_argentinos(f"{float(valor):,.{decimales}f}")


def formato_moneda(valor) -> str:
    if valor is None or valor == "":
        return "-"
    return f"$ {formato_numero(valor, 2)}"


def formato_porcentaje(valor) -> str:
    if valor is None or valor == "":
        return "-"
    return f"{formato_numero(valor, 1)} %"


def formato_fecha(valor) -> str:
    """'2026-03-15' -> '15/03/2026'"""
    if not valor:
        return "-"
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    texto = str(valor)
    partes = texto[:10].split("-")
    if len(partes) == 3:
        return f"{partes[2]}/{partes[1]}/{partes[0]}{texto[10:]}"
    return texto


def formato_mes(valor) -> str:
    """'2026-03' -> 'Mar 2026'"""
    try:
        anio, mes = str(valor).split("-")[:2]
        return f"{MESES[int(mes) - 1]} {anio}"
    except (ValueError, IndexError):
        return str(valor)


def registrar_filtros(app: Flask) -> None:
    app.add_template_filter(formato_numero, "numero")
    app.add_template_filter(formato_moneda, "moneda")
    app.add_template_filter(formato_porcentaje, "porcentaje")
    app.add_template_filter(formato_fecha, "fecha")
    app.add_template_filter(formato_mes, "mes")
