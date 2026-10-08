"""PASO 2 - VALIDACIÓN de los registros de SERVICIOS logísticos.

1. COLUMNAS: qué columnas trae el archivo (se usan para validar y para la ayuda en pantalla).
2. ALIAS: otros nombres con los que puede venir una columna.
3. validar_servicio(): las reglas de cada campo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from app.servicios.lector import VALORES_DE_MAS, FilaLeida
from app.utils.conversiones import a_decimal, a_entero, es_vacio, normalizar_texto, redondear_dinero

COLUMNAS = [
    {
        "campo": "numero_registro",
        "descripcion": "Número correlativo del servicio (único)",
        "ejemplo": "1",
    },
    {
        "campo": "operador_logistico",
        "descripcion": "Empresa que realizó los envíos",
        "ejemplo": "LogisticaSur",
    },
    {"campo": "anio", "descripcion": "Año de los servicios", "ejemplo": "2024"},
    {"campo": "mes", "descripcion": "Mes (1 a 12)", "ejemplo": "1"},
    {
        "campo": "cantidad_envios",
        "descripcion": "Cantidad de envíos (entero, 0 o más)",
        "ejemplo": "314",
    },
    {"campo": "region", "descripcion": "Región de los servicios", "ejemplo": "Centro"},
    {
        "campo": "costo_por_envio",
        "descripcion": "Costo de cada envío (0 o más)",
        "ejemplo": "2707.33",
    },
    {
        "campo": "porcentaje_entregas_atiempo",
        "descripcion": "% de envíos entregados a tiempo (0 a 100)",
        "ejemplo": "73",
    },
]

# El lector convierte "PorcentajeEntregasATiempo" en "porcentaje_entregas_atiempo".
ALIAS = {
    "porcentaje_entregas_a_tiempo": "porcentaje_entregas_atiempo",
    "operador": "operador_logistico",
    "ano": "anio",
    "envios": "cantidad_envios",
}

LARGO_MAXIMO_TEXTO = 100

# La consigna dice que NumeroRegistro es un número correlativo: no se puede repetir.
CLAVE_UNICA: str | None = "numero_registro"

# campo -> (función que convierte, mínimo, máximo o None si no tiene)
REGLAS_NUMERICAS: dict[str, tuple[Callable[[Any], float], float, float | None]] = {
    "numero_registro": (a_entero, 1, None),
    "anio": (a_entero, 2000, 2100),
    "mes": (a_entero, 1, 12),
    "cantidad_envios": (a_entero, 0, None),
    "costo_por_envio": (a_decimal, 0, None),
    "porcentaje_entregas_atiempo": (a_decimal, 0, 100),
}
CAMPOS_TEXTO = ("operador_logistico", "region")


@dataclass
class ErrorValidacion:
    fila: int
    campo: str
    mensaje: str


@dataclass
class ResultadoValidacion:
    validos: list[dict[str, Any]] = field(default_factory=list)
    filas_validas: list[int] = field(default_factory=list)  # número de fila de cada válido
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


def validar_numero(valor: Any, convertir: Callable, minimo: float, maximo: float | None):
    """Convierte un valor y revisa su rango. Devuelve (numero, None) o (None, mensaje)."""
    try:
        numero = convertir(valor)
    except ValueError as error:
        return None, str(error)
    if numero < minimo or (maximo is not None and numero > maximo):
        if maximo is None:
            return None, f"Debe ser {minimo} o más."
        return None, f"Debe estar entre {minimo} y {maximo}."
    return numero, None


def validar_servicio(datos: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, str]]:
    """Valida UN servicio. Devuelve (servicio_limpio, {}) o (None, {campo: mensaje})."""
    datos = aplicar_alias(datos)
    errores: dict[str, str] = {}
    servicio: dict[str, Any] = {}

    for columna in COLUMNAS:
        if es_vacio(datos.get(columna["campo"])):
            errores[columna["campo"]] = "Es obligatorio."

    for campo in CAMPOS_TEXTO:
        if campo not in errores:
            texto = normalizar_texto(datos[campo])
            if len(texto) > LARGO_MAXIMO_TEXTO:
                errores[campo] = f"No puede superar {LARGO_MAXIMO_TEXTO} caracteres."
            else:
                servicio[campo] = texto

    for campo, (convertir, minimo, maximo) in REGLAS_NUMERICAS.items():
        if campo not in errores:
            numero, mensaje = validar_numero(datos[campo], convertir, minimo, maximo)
            if mensaje:
                errores[campo] = mensaje
            else:
                servicio[campo] = numero

    if "costo_por_envio" in servicio:
        servicio["costo_por_envio"] = redondear_dinero(servicio["costo_por_envio"])

    if errores:
        return None, errores
    return servicio, {}


def validar_filas(filas: list[FilaLeida]) -> ResultadoValidacion:
    """Valida todas las filas: separa las válidas de las que tienen errores."""
    resultado = ResultadoValidacion()
    for fila in filas:
        if VALORES_DE_MAS in fila.datos:
            resultado.errores.append(
                ErrorValidacion(
                    fila=fila.numero,
                    campo="fila",
                    mensaje="Tiene más valores que columnas (¿coma decimal sin comillas?).",
                )
            )
            continue
        servicio, errores = validar_servicio(fila.datos)
        if errores:
            resultado.errores.extend(
                ErrorValidacion(fila=fila.numero, campo=campo, mensaje=mensaje)
                for campo, mensaje in errores.items()
            )
        else:
            resultado.validos.append(servicio)
            resultado.filas_validas.append(fila.numero)
    return resultado
