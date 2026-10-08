"""PASO 4 - ALMACENAMIENTO: acceso a la tabla `servicios`. Solo SQL, sin reglas de negocio.

Importante:
  - Todas las consultas usan parámetros (?) -> protege contra inyección SQL.
  - Estas funciones NO hacen commit: quien las llama usa `with transaccion():`.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from app.db import obtener_db
from app.utils.conversiones import normalizar_texto

COLUMNAS_ORDENABLES = (
    "numero_registro",
    "operador_logistico",
    "anio",
    "mes",
    "cantidad_envios",
    "region",
    "costo_por_envio",
    "porcentaje_entregas_atiempo",
    "costo_total",
)

SQL_INSERTAR = """
    INSERT INTO servicios
        (numero_registro, operador_logistico, anio, mes, cantidad_envios, region,
         costo_por_envio, porcentaje_entregas_atiempo, costo_total, importacion_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# El período se compara como un número AAAAMM: marzo de 2025 -> 202503
SQL_PERIODO = "(anio * 100 + mes)"


def _a_periodo(valor: Any) -> str:
    """Acepta 'AAAA-MM' (ej.: 2025-03); cualquier otra cosa se ignora."""
    texto = normalizar_texto(valor)
    return texto if re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", texto) else ""


@dataclass
class FiltrosServicios:
    operador: str = ""
    region: str = ""
    desde: str = ""  # AAAA-MM
    hasta: str = ""  # AAAA-MM

    @classmethod
    def desde_diccionario(cls, datos: Mapping[str, Any]) -> FiltrosServicios:
        """Arma los filtros a partir de los parámetros de la URL (?desde=2025-01&hasta=...)."""
        return cls(
            operador=normalizar_texto(datos.get("operador")),
            region=normalizar_texto(datos.get("region")),
            desde=_a_periodo(datos.get("desde")),
            hasta=_a_periodo(datos.get("hasta")),
        )

    def como_diccionario(self) -> dict[str, str]:
        """Solo los filtros usados (para armar links que conserven los filtros)."""
        return {clave: valor for clave, valor in asdict(self).items() if valor}

    @property
    def activos(self) -> bool:
        return bool(self.como_diccionario())


def _condiciones(filtros: FiltrosServicios | None) -> tuple[str, list[Any]]:
    """Arma el WHERE de la consulta según los filtros."""
    if filtros is None:
        return "", []
    condiciones: list[str] = []
    parametros: list[Any] = []
    if filtros.operador:
        condiciones.append("operador_logistico = ?")
        parametros.append(filtros.operador)
    if filtros.region:
        condiciones.append("region = ?")
        parametros.append(filtros.region)
    if filtros.desde:
        condiciones.append(f"{SQL_PERIODO} >= ?")
        parametros.append(int(filtros.desde.replace("-", "")))
    if filtros.hasta:
        condiciones.append(f"{SQL_PERIODO} <= ?")
        parametros.append(int(filtros.hasta.replace("-", "")))
    where = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    return where, parametros


def _como_tupla(servicio: dict[str, Any], importacion_id: int | None) -> tuple:
    return (
        servicio["numero_registro"],
        servicio["operador_logistico"],
        servicio["anio"],
        servicio["mes"],
        servicio["cantidad_envios"],
        servicio["region"],
        servicio["costo_por_envio"],
        servicio["porcentaje_entregas_atiempo"],
        servicio["costo_total"],
        importacion_id,
    )


def insertar_varias(servicios: list[dict[str, Any]], importacion_id: int | None = None) -> int:
    obtener_db().executemany(SQL_INSERTAR, [_como_tupla(s, importacion_id) for s in servicios])
    return len(servicios)


def listar_pagina(
    filtros: FiltrosServicios,
    orden: str = "numero_registro",
    direccion: str = "asc",
    pagina: int = 1,
    por_pagina: int = 20,
) -> tuple[list[dict[str, Any]], int]:
    """Devuelve (servicios_de_la_pagina, cantidad_total_que_cumplen_los_filtros)."""
    where, parametros = _condiciones(filtros)
    db = obtener_db()
    total = db.execute(f"SELECT COUNT(*) FROM servicios{where}", parametros).fetchone()[0]

    # ORDER BY no acepta parámetros (?): por eso solo se permiten columnas de una lista fija.
    columna = orden if orden in COLUMNAS_ORDENABLES else "numero_registro"
    sentido = "ASC" if direccion == "asc" else "DESC"
    filas = db.execute(
        f"SELECT * FROM servicios{where} ORDER BY {columna} {sentido}, id {sentido} LIMIT ? OFFSET ?",
        [*parametros, por_pagina, (max(pagina, 1) - 1) * por_pagina],
    ).fetchall()
    return [dict(fila) for fila in filas], total


def totales(filtros: FiltrosServicios | None = None) -> dict[str, float]:
    """Cantidad de registros, envíos y costo total de los que cumplen los filtros."""
    where, parametros = _condiciones(filtros)
    fila = (
        obtener_db()
        .execute(
            "SELECT COUNT(*) AS registros, COALESCE(SUM(cantidad_envios), 0) AS envios, "
            f"COALESCE(SUM(costo_total), 0) AS costo_total FROM servicios{where}",
            parametros,
        )
        .fetchone()
    )
    return dict(fila)


def listar_todas(filtros: FiltrosServicios | None = None) -> list[dict[str, Any]]:
    where, parametros = _condiciones(filtros)
    filas = obtener_db().execute(
        f"SELECT * FROM servicios{where} ORDER BY numero_registro", parametros
    )
    return [dict(fila) for fila in filas]


def obtener_por_id(servicio_id: int) -> dict[str, Any] | None:
    fila = obtener_db().execute("SELECT * FROM servicios WHERE id = ?", (servicio_id,)).fetchone()
    return dict(fila) if fila else None


def valores_de(columna: str) -> set[Any]:
    """Todos los valores guardados de una columna (sirve para detectar claves repetidas)."""
    if columna not in COLUMNAS_ORDENABLES:  # solo columnas conocidas: nunca texto del usuario
        raise ValueError(f"Columna desconocida: {columna}")
    return {fila[0] for fila in obtener_db().execute(f"SELECT {columna} FROM servicios")}


def listar_distintos(columna: str) -> list[str]:
    """Valores distintos de una columna de texto (para los filtros de operador y región)."""
    if columna not in ("operador_logistico", "region"):
        raise ValueError(f"Columna desconocida: {columna}")
    filas = obtener_db().execute(f"SELECT DISTINCT {columna} FROM servicios ORDER BY {columna}")
    return [fila[0] for fila in filas]


def listar_periodos() -> list[str]:
    """Los períodos (AAAA-MM) que tienen datos, del más viejo al más nuevo."""
    filas = obtener_db().execute(
        "SELECT DISTINCT printf('%04d-%02d', anio, mes) FROM servicios ORDER BY anio, mes"
    )
    return [fila[0] for fila in filas]


def eliminar(servicio_id: int) -> bool:
    cursor = obtener_db().execute("DELETE FROM servicios WHERE id = ?", (servicio_id,))
    return cursor.rowcount > 0


def eliminar_todas() -> int:
    return obtener_db().execute("DELETE FROM servicios").rowcount
