"""PASO 4 - ALMACENAMIENTO: acceso a la tabla `ventas`. Solo SQL, sin reglas de negocio.

Importante:
  - Todas las consultas usan parámetros (?) -> protege contra inyección SQL.
  - Estas funciones NO hacen commit: quien las llama usa `with transaccion():`.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from app.db import obtener_db
from app.utils.conversiones import a_fecha_iso_o_vacio, normalizar_texto

COLUMNAS_ORDENABLES = ("fecha", "producto", "categoria", "cantidad", "precio_unitario", "total")

SQL_INSERTAR = """
    INSERT INTO ventas
        (fecha, producto, categoria, cantidad, precio_unitario, total, importacion_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""


@dataclass
class FiltrosVentas:
    busqueda: str = ""  # texto a buscar en producto o categoría
    categoria: str = ""
    desde: str = ""  # AAAA-MM-DD
    hasta: str = ""  # AAAA-MM-DD

    @classmethod
    def desde_diccionario(cls, datos: Mapping[str, Any]) -> FiltrosVentas:
        """Arma los filtros a partir de los parámetros de la URL (?busqueda=...&desde=...)."""
        return cls(
            busqueda=normalizar_texto(datos.get("busqueda")),
            categoria=normalizar_texto(datos.get("categoria")),
            desde=a_fecha_iso_o_vacio(datos.get("desde")),
            hasta=a_fecha_iso_o_vacio(datos.get("hasta")),
        )

    def como_diccionario(self) -> dict[str, str]:
        """Solo los filtros usados (para armar links que conserven los filtros)."""
        return {clave: valor for clave, valor in asdict(self).items() if valor}

    @property
    def activos(self) -> bool:
        return bool(self.como_diccionario())


def _condiciones(filtros: FiltrosVentas | None) -> tuple[str, list[Any]]:
    """Arma el WHERE de la consulta según los filtros."""
    if filtros is None:
        return "", []
    condiciones: list[str] = []
    parametros: list[Any] = []
    if filtros.busqueda:
        condiciones.append("(producto LIKE ? OR categoria LIKE ?)")
        parametros += [f"%{filtros.busqueda}%"] * 2
    if filtros.categoria:
        condiciones.append("categoria = ?")
        parametros.append(filtros.categoria)
    if filtros.desde:
        condiciones.append("fecha >= ?")
        parametros.append(filtros.desde)
    if filtros.hasta:
        condiciones.append("fecha <= ?")
        parametros.append(filtros.hasta)
    where = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    return where, parametros


def _como_tupla(venta: dict[str, Any], importacion_id: int | None) -> tuple:
    return (
        venta["fecha"],
        venta["producto"],
        venta["categoria"],
        venta["cantidad"],
        venta["precio_unitario"],
        venta["total"],
        importacion_id,
    )


def insertar(venta: dict[str, Any], importacion_id: int | None = None) -> int:
    cursor = obtener_db().execute(SQL_INSERTAR, _como_tupla(venta, importacion_id))
    return cursor.lastrowid


def insertar_varias(ventas: list[dict[str, Any]], importacion_id: int | None = None) -> int:
    obtener_db().executemany(SQL_INSERTAR, [_como_tupla(v, importacion_id) for v in ventas])
    return len(ventas)


def listar_pagina(
    filtros: FiltrosVentas,
    orden: str = "fecha",
    direccion: str = "desc",
    pagina: int = 1,
    por_pagina: int = 20,
) -> tuple[list[dict[str, Any]], int]:
    """Devuelve (ventas_de_la_pagina, cantidad_total_que_cumplen_los_filtros)."""
    where, parametros = _condiciones(filtros)
    db = obtener_db()
    total = db.execute(f"SELECT COUNT(*) FROM ventas{where}", parametros).fetchone()[0]

    # ORDER BY no acepta parámetros (?): por eso solo se permiten columnas de una lista fija.
    columna = orden if orden in COLUMNAS_ORDENABLES else "fecha"
    sentido = "ASC" if direccion == "asc" else "DESC"
    filas = db.execute(
        f"SELECT * FROM ventas{where} ORDER BY {columna} {sentido}, id {sentido} LIMIT ? OFFSET ?",
        [*parametros, por_pagina, (max(pagina, 1) - 1) * por_pagina],
    ).fetchall()
    return [dict(fila) for fila in filas], total


def listar_todas(filtros: FiltrosVentas | None = None) -> list[dict[str, Any]]:
    where, parametros = _condiciones(filtros)
    filas = obtener_db().execute(f"SELECT * FROM ventas{where} ORDER BY fecha, id", parametros)
    return [dict(fila) for fila in filas]


def obtener_por_id(venta_id: int) -> dict[str, Any] | None:
    fila = obtener_db().execute("SELECT * FROM ventas WHERE id = ?", (venta_id,)).fetchone()
    return dict(fila) if fila else None


def listar_categorias() -> list[str]:
    filas = obtener_db().execute("SELECT DISTINCT categoria FROM ventas ORDER BY categoria")
    return [fila["categoria"] for fila in filas]


def eliminar(venta_id: int) -> bool:
    cursor = obtener_db().execute("DELETE FROM ventas WHERE id = ?", (venta_id,))
    return cursor.rowcount > 0


def eliminar_todas() -> int:
    return obtener_db().execute("DELETE FROM ventas").rowcount
