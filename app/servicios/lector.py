"""PASO 1 - LECTURA de archivos de datos: CSV, TXT, JSON y Excel (.xlsx).

Sin importar el formato, siempre devuelve lo mismo: una lista de FilaLeida.
Así el resto del sistema no necesita saber de qué tipo de archivo vinieron los datos.
Esta parte es genérica: normalmente NO hace falta cambiarla al adaptar la plantilla.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.utils.conversiones import es_vacio, normalizar_clave

FORMATOS_SOPORTADOS = ("csv", "txt", "json", "xlsx")
SEPARADORES_POSIBLES = ";,\t|"


class ErrorLectura(Exception):
    """El archivo completo no se puede procesar (vacío, formato inválido, faltan columnas...)."""


@dataclass
class FilaLeida:
    numero: int  # número de fila/elemento en el archivo original (para los mensajes de error)
    datos: dict[str, Any]  # nombre_de_columna_normalizado -> valor tal como vino


def extension_de(nombre_archivo: str) -> str:
    return Path(nombre_archivo).suffix.lower().lstrip(".")


def leer_archivo(nombre_archivo: str, contenido: bytes) -> list[FilaLeida]:
    extension = extension_de(nombre_archivo)
    if extension not in FORMATOS_SOPORTADOS:
        formatos = ", ".join(f".{f}" for f in FORMATOS_SOPORTADOS)
        raise ErrorLectura(f"El formato '.{extension}' no está soportado. Usá {formatos}.")
    if not contenido or not contenido.strip():
        raise ErrorLectura("El archivo está vacío.")

    if extension in ("csv", "txt"):
        filas = leer_csv(decodificar(contenido))
    elif extension == "json":
        filas = leer_json(decodificar(contenido))
    else:
        filas = leer_xlsx(contenido)

    if not filas:
        raise ErrorLectura("El archivo no tiene filas con datos (solo encabezados).")
    return filas


def decodificar(contenido: bytes) -> str:
    """Pasa de bytes a texto. Excel en Windows suele guardar los CSV en cp1252, no en UTF-8."""
    for codificacion in ("utf-8-sig", "cp1252"):
        try:
            return contenido.decode(codificacion)
        except UnicodeDecodeError:
            continue
    return contenido.decode("latin-1")  # latin-1 nunca falla


def detectar_separador(texto: str) -> str:
    """Elige el separador más frecuente en la primera línea con contenido (';' ',' tab o '|')."""
    primera_linea = next((linea for linea in texto.splitlines() if linea.strip()), "")
    conteos = {separador: primera_linea.count(separador) for separador in SEPARADORES_POSIBLES}
    separador = max(conteos, key=conteos.get)
    return separador if conteos[separador] > 0 else ","


def leer_csv(texto: str) -> list[FilaLeida]:
    lector = csv.reader(io.StringIO(texto), delimiter=detectar_separador(texto))
    encabezados: list[str] | None = None
    filas: list[FilaLeida] = []
    for valores in lector:
        if all(es_vacio(valor) for valor in valores):
            continue  # se ignoran las filas vacías
        if encabezados is None:
            encabezados = _preparar_encabezados(valores)
            continue
        filas.append(FilaLeida(numero=lector.line_num, datos=_combinar(encabezados, valores)))
    return filas


def leer_json(texto: str) -> list[FilaLeida]:
    """Acepta una lista de objetos  [{...}, {...}]  o un objeto con una lista  {"ventas": [...]}."""
    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as error:
        raise ErrorLectura(f"El JSON no es válido (línea {error.lineno}): {error.msg}.") from None

    if isinstance(datos, dict):
        listas = [valor for valor in datos.values() if isinstance(valor, list)]
        if len(listas) != 1:
            raise ErrorLectura("El JSON debe ser una lista de objetos o un objeto con una lista.")
        datos = listas[0]
    if not isinstance(datos, list):
        raise ErrorLectura("El JSON debe ser una lista de objetos.")

    filas = []
    for posicion, elemento in enumerate(datos, start=1):
        if not isinstance(elemento, dict):
            raise ErrorLectura(f"El elemento {posicion} del JSON no es un objeto {{...}}.")
        datos_fila = {normalizar_clave(clave): valor for clave, valor in elemento.items()}
        filas.append(FilaLeida(numero=posicion, datos=datos_fila))
    return filas


def leer_xlsx(contenido: bytes) -> list[FilaLeida]:
    """Lee la primera hoja del Excel. La primera fila con datos se toma como encabezado."""
    try:
        from openpyxl import load_workbook
    except ImportError:
        raise ErrorLectura(
            "Para leer Excel hay que instalar openpyxl: pip install openpyxl"
        ) from None
    try:
        libro = load_workbook(io.BytesIO(contenido), read_only=True, data_only=True)
    except Exception:  # openpyxl lanza errores distintos según qué esté dañado
        raise ErrorLectura("No se pudo abrir el Excel. ¿Es un archivo .xlsx válido?") from None

    encabezados: list[str] | None = None
    filas: list[FilaLeida] = []
    try:
        for numero, valores in enumerate(libro.active.iter_rows(values_only=True), start=1):
            if all(es_vacio(valor) for valor in valores):
                continue
            if encabezados is None:
                encabezados = _preparar_encabezados(valores)
                continue
            filas.append(FilaLeida(numero=numero, datos=_combinar(encabezados, list(valores))))
    finally:
        libro.close()
    return filas


def _preparar_encabezados(valores) -> list[str]:
    encabezados = [normalizar_clave(valor) for valor in valores]
    repetidos = sorted({e for e in encabezados if e and encabezados.count(e) > 1})
    if repetidos:
        raise ErrorLectura(f"Hay columnas repetidas en el encabezado: {', '.join(repetidos)}.")
    return encabezados


def _combinar(encabezados: list[str], valores: list) -> dict[str, Any]:
    """Une encabezados y valores. Si a la fila le faltan valores, quedan como ''."""
    return {
        clave: (valores[posicion] if posicion < len(valores) else "")
        for posicion, clave in enumerate(encabezados)
        if clave  # se ignoran columnas sin nombre
    }
