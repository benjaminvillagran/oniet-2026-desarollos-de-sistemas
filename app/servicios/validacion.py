"""PASO 2 - VALIDACIÓN de los datos de VENTAS (específico del problema).

Al adaptar la plantilla a la consigna, este es uno de los primeros archivos a cambiar:
  1. COLUMNAS: qué columnas trae el archivo (se usan para validar y para la ayuda en pantalla).
  2. ALIAS: otros nombres con los que puede venir una columna.
  3. validar_venta(): las reglas de cada campo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.servicios.lector import FilaLeida
from app.utils.conversiones import a_decimal, a_entero, a_fecha, es_vacio, normalizar_texto

COLUMNAS = [
    {"campo": "fecha", "descripcion": "Fecha de la venta", "ejemplo": "15/03/2026"},
    {"campo": "producto", "descripcion": "Nombre del producto", "ejemplo": "Alfajor triple"},
    {"campo": "categoria", "descripcion": "Rubro del producto", "ejemplo": "Kiosco"},
    {"campo": "cantidad", "descripcion": "Unidades vendidas (entero mayor a 0)", "ejemplo": "3"},
    {
        "campo": "precio_unitario",
        "descripcion": "Precio por unidad (0 o más)",
        "ejemplo": "1250,50",
    },
]

ALIAS = {
    "fecha_venta": "fecha",
    "articulo": "producto",
    "rubro": "categoria",
    "cant": "cantidad",
    "unidades": "cantidad",
    "precio": "precio_unitario",
    "precio_unit": "precio_unitario",
}

LARGO_MAXIMO_TEXTO = 100


@dataclass
class ErrorValidacion:
    fila: int
    campo: str
    mensaje: str


@dataclass
class ResultadoValidacion:
    validos: list[dict[str, Any]] = field(default_factory=list)
    errores: list[ErrorValidacion] = field(default_factory=list)

    @property
    def filas_con_error(self) -> int:
        return len({error.fila for error in self.errores})


def aplicar_alias(datos: dict[str, Any]) -> dict[str, Any]:
    return {ALIAS.get(clave, clave): valor for clave, valor in datos.items()}


def columnas_faltantes(filas: list[FilaLeida]) -> list[str]:
    """Columnas obligatorias que no aparecen en el archivo (se revisa la primera fila)."""
    if not filas:
        return []
    presentes = aplicar_alias(filas[0].datos).keys()
    return [columna["campo"] for columna in COLUMNAS if columna["campo"] not in presentes]


def validar_venta(datos: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, str]]:
    """Valida UNA venta.

    Devuelve (venta_limpia, {}) si está todo bien, o (None, {campo: mensaje}) si hay errores.
    """
    datos = aplicar_alias(datos)
    errores: dict[str, str] = {}
    venta: dict[str, Any] = {}

    for columna in COLUMNAS:
        if es_vacio(datos.get(columna["campo"])):
            errores[columna["campo"]] = "Es obligatorio."

    if "fecha" not in errores:
        try:
            venta["fecha"] = a_fecha(datos["fecha"]).isoformat()
        except ValueError as error:
            errores["fecha"] = str(error)

    for campo in ("producto", "categoria"):
        if campo not in errores:
            texto = normalizar_texto(datos[campo])
            if len(texto) > LARGO_MAXIMO_TEXTO:
                errores[campo] = f"No puede superar {LARGO_MAXIMO_TEXTO} caracteres."
            else:
                venta[campo] = texto[0].upper() + texto[1:]

    if "categoria" in venta:
        venta["categoria"] = venta["categoria"].capitalize()  # 'KIOSCO' y 'kiosco' -> 'Kiosco'

    if "cantidad" not in errores:
        try:
            cantidad = a_entero(datos["cantidad"])
            if cantidad <= 0:
                errores["cantidad"] = "Debe ser mayor a 0."
            else:
                venta["cantidad"] = cantidad
        except ValueError as error:
            errores["cantidad"] = str(error)

    if "precio_unitario" not in errores:
        try:
            precio = a_decimal(datos["precio_unitario"])
            if precio < 0:
                errores["precio_unitario"] = "No puede ser negativo."
            else:
                venta["precio_unitario"] = round(precio, 2)
        except ValueError as error:
            errores["precio_unitario"] = str(error)

    if errores:
        return None, errores
    return venta, {}


def validar_filas(filas: list[FilaLeida]) -> ResultadoValidacion:
    """Valida todas las filas: separa las válidas de las que tienen errores."""
    resultado = ResultadoValidacion()
    for fila in filas:
        venta, errores = validar_venta(fila.datos)
        if errores:
            resultado.errores.extend(
                ErrorValidacion(fila=fila.numero, campo=campo, mensaje=mensaje)
                for campo, mensaje in errores.items()
            )
        else:
            resultado.validos.append(venta)
    return resultado
