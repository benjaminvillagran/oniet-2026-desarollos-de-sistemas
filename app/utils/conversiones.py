"""Conversión de valores "crudos" (tal como vienen en los archivos) a datos limpios.

Las funciones a_* lanzan ValueError con un mensaje en español cuando el valor no sirve.
La validación usa ese mensaje para decirle al usuario qué está mal y en qué fila.
"""

from __future__ import annotations

import math
import re
import unicodedata
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal

# Formatos de fecha aceptados (se prueban en este orden). Día antes que mes: formato argentino.
FORMATOS_FECHA = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%Y/%m/%d", "%d.%m.%Y")

# Números más grandes que esto no son datos reales (y no entran en la base de datos)
MAXIMO_NUMERO = 1e15

_MILES_CON_PUNTO = re.compile(r"-?\d{1,3}(\.\d{3})+(,\d+)?")  # 1.500 | 1.234.567 | 1.234,50
# Formato de EE. UU. solo si no hay duda: con punto decimal o con 2 o más grupos de miles
_MILES_CON_COMA = re.compile(r"-?\d{1,3}((,\d{3})+\.\d+|(,\d{3}){2,})")  # 1,234.50 | 1,234,567
_DECIMAL_CON_COMA = re.compile(r"-?\d*,\d+")  # 1234,5 | ,5


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
    """Convierte a número decimal. Prioriza el formato argentino (punto de miles, coma decimal).

    '1.500' -> 1500   '1.234,50' -> 1234.5   '$ 1.500' -> 1500   '1234,5' -> 1234.5
    '1234.5' -> 1234.5   '1.5' -> 1.5   '0.500' -> 0.5   '1,234.50' -> 1234.5 (formato de EE. UU.)
    Un punto seguido de exactamente 3 dígitos es separador de miles ('2.675' -> 2675).
    Formatos mezclados o raros ('1.2.3,4') se rechazan en vez de adivinar.
    """
    if isinstance(valor, bool):
        raise ValueError(f"'{valor}' no es un número válido")
    if isinstance(valor, (int, float)):
        numero = float(valor)
    else:
        texto = normalizar_texto(valor).replace("$", "").replace(" ", "")
        if texto == "":
            raise ValueError("está vacío")
        if _MILES_CON_PUNTO.fullmatch(texto) and not texto.lstrip("-").startswith("0"):
            texto = texto.replace(".", "").replace(",", ".")  # 1.234,50 -> 1234.50
        elif _MILES_CON_COMA.fullmatch(texto):
            texto = texto.replace(",", "")  # 1,234.50 -> 1234.50
        elif _DECIMAL_CON_COMA.fullmatch(texto):
            texto = texto.replace(",", ".")  # 1234,5 -> 1234.5
        try:
            numero = float(texto)
        except ValueError:
            raise ValueError(f"'{valor}' no es un número válido") from None
    if not math.isfinite(numero):
        raise ValueError(f"'{valor}' no es un número válido")
    if abs(numero) > MAXIMO_NUMERO:
        raise ValueError(f"'{valor}' es demasiado grande")
    return numero


def a_entero(valor) -> int:
    numero = a_decimal(valor)
    if not numero.is_integer():
        raise ValueError(f"'{valor}' debe ser un número entero")
    return int(numero)


def redondear_dinero(valor: float) -> float:
    """Redondea a centavos como en un comercio (1,005 -> 1,01), no como float (-> 1,00)."""
    return float(Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def a_fecha(valor) -> date:
    """Convierte a fecha. Acepta DD/MM/AAAA, AAAA-MM-DD, DD-MM-AAAA y celdas de Excel con formato
    fecha. Un número de serie de Excel (ej.: 45000) no se acepta: guardar la columna como fecha."""
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
