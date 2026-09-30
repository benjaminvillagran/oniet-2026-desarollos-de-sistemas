"""Conversión de valores "crudos" (tal como vienen en los archivos) a datos limpios.

Las funciones a_* lanzan ValueError con un mensaje en español cuando el valor no sirve.
La validación usa ese mensaje para decirle al usuario qué está mal y en qué fila.
"""

from __future__ import annotations

import math
import re
import unicodedata
from datetime import date, datetime

# Formatos de fecha aceptados (se prueban en este orden). Día antes que mes: formato argentino.
FORMATOS_FECHA = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%Y/%m/%d", "%d.%m.%Y")


def es_vacio(valor) -> bool:
    return valor is None or (isinstance(valor, str) and valor.strip() == "")


def normalizar_texto(valor) -> str:
    """Quita espacios sobrantes:  '  Juan   Pérez ' -> 'Juan Pérez'."""
    if valor is None:
        return ""
    return " ".join(str(valor).split())


def quitar_acentos(texto: str) -> str:
    descompuesto = unicodedata.normalize("NFKD", texto)
    return "".join(letra for letra in descompuesto if not unicodedata.combining(letra))


def normalizar_clave(texto) -> str:
    """Convierte un encabezado de columna en nombre de campo.

    'Precio Unitario ($)' -> 'precio_unitario'      'Categoría' -> 'categoria'
    'CompaniaSeguro' -> 'compania_seguro'           'precioUSD' -> 'precio_usd'
    """
    limpio = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", normalizar_texto(texto))  # separa camelCase
    limpio = quitar_acentos(limpio).lower()
    return re.sub(r"[^a-z0-9]+", "_", limpio).strip("_")


def a_decimal(valor) -> float:
    """Convierte a número decimal aceptando formatos argentinos e internacionales.

    1234.5 | '1234,5' | '1.234,50' | '1,234.50' | '$ 1.234,50' | '1.234.567'
    Si hay un único punto y ninguna coma ('1.5'), el punto se toma como decimal.
    """
    if isinstance(valor, bool):
        raise ValueError(f"'{valor}' no es un número válido")
    if isinstance(valor, (int, float)):
        numero = float(valor)
    else:
        texto = normalizar_texto(valor).replace("$", "").replace(" ", "")
        if texto == "":
            raise ValueError("está vacío")
        if "," in texto and "." in texto:
            if texto.rfind(",") > texto.rfind("."):  # 1.234,56
                texto = texto.replace(".", "").replace(",", ".")
            else:  # 1,234.56
                texto = texto.replace(",", "")
        elif "," in texto:
            # una sola coma es el decimal (1234,56); varias son separador de miles (1,234,567)
            texto = texto.replace(",", ".") if texto.count(",") == 1 else texto.replace(",", "")
        elif texto.count(".") > 1:  # 1.234.567
            texto = texto.replace(".", "")
        try:
            numero = float(texto)
        except ValueError:
            raise ValueError(f"'{valor}' no es un número válido") from None
    if not math.isfinite(numero):
        raise ValueError(f"'{valor}' no es un número válido")
    return numero


def a_entero(valor) -> int:
    numero = a_decimal(valor)
    if not numero.is_integer():
        raise ValueError(f"'{valor}' debe ser un número entero")
    return int(numero)


def a_fecha(valor) -> date:
    """Convierte a fecha. Acepta DD/MM/AAAA, AAAA-MM-DD, DD-MM-AAAA y fechas de Excel."""
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    texto = normalizar_texto(valor)
    if texto == "":
        raise ValueError("está vacía")
    solo_fecha = texto.split(" ")[0].split("T")[0]  # descarta la hora si viene incluida
    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(solo_fecha, formato).date()
        except ValueError:
            continue
    raise ValueError(f"'{texto}' no es una fecha válida (usá DD/MM/AAAA o AAAA-MM-DD)")


def a_fecha_iso_o_vacio(valor) -> str:
    """Para filtros opcionales: devuelve 'AAAA-MM-DD' o '' si el valor no es una fecha válida."""
    if es_vacio(valor):
        return ""
    try:
        return a_fecha(valor).isoformat()
    except ValueError:
        return ""
