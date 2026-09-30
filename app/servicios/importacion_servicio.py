"""Importación de un archivo: el recorrido completo LEER -> VALIDAR -> PROCESAR -> GUARDAR."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.db import transaccion
from app.repositorios import importaciones_repositorio, ventas_repositorio
from app.servicios import lector, procesamiento, validacion
from app.servicios.lector import ErrorLectura
from app.servicios.validacion import ErrorValidacion


@dataclass
class ResumenImportacion:
    nombre_archivo: str
    filas_leidas: int
    filas_guardadas: int
    errores: list[ErrorValidacion] = field(default_factory=list)
    importacion_id: int | None = None

    @property
    def filas_con_error(self) -> int:
        return len({error.fila for error in self.errores})


def importar_archivo(nombre_archivo: str, contenido: bytes) -> ResumenImportacion:
    """Importa un archivo. Lanza ErrorLectura si el archivo completo no se puede usar.

    Las filas con errores NO se guardan, pero se informan (fila, campo y motivo).
    """
    # 1. LEER: bytes del archivo -> lista de filas
    filas = lector.leer_archivo(nombre_archivo, contenido)

    faltantes = validacion.columnas_faltantes(filas)
    if faltantes:
        encontradas = ", ".join(filas[0].datos.keys()) or "ninguna"
        raise ErrorLectura(
            f"Faltan columnas obligatorias: {', '.join(faltantes)}. "
            f"Columnas encontradas: {encontradas}."
        )

    # 2. VALIDAR: separa filas válidas de filas con errores
    resultado = validacion.validar_filas(filas)

    # 3. PROCESAR: agrega los campos calculados
    ventas = [procesamiento.completar_venta(venta) for venta in resultado.validos]

    # 4. GUARDAR: todo junto en una transacción (si algo falla, no se guarda nada)
    with transaccion():
        importacion_id = importaciones_repositorio.registrar(
            nombre_archivo, len(filas), len(ventas), resultado.filas_con_error
        )
        ventas_repositorio.insertar_varias(ventas, importacion_id)

    return ResumenImportacion(
        nombre_archivo=nombre_archivo,
        filas_leidas=len(filas),
        filas_guardadas=len(ventas),
        errores=resultado.errores,
        importacion_id=importacion_id,
    )


def importar_desde_url(url: str, limite_bytes: int) -> ResumenImportacion:
    """Descarga los datos de una URL o API y los importa igual que un archivo."""
    nombre, contenido = lector.descargar(url, limite_bytes)
    return importar_archivo(nombre, contenido)
