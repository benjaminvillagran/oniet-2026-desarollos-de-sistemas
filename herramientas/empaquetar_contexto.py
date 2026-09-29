"""Junta el código del proyecto en un solo archivo de texto para pegarlo en un chat de IA.

Sirve como plan B si en la PC del laboratorio solo tenemos IA por navegador
(claude.ai, chat.deepseek.com, gemini.google.com): se pega el contenido de
contexto_ia.txt y la IA conoce todo el proyecto.

Uso:
    python herramientas/empaquetar_contexto.py              todo el proyecto
    python herramientas/empaquetar_contexto.py app/servicios   solo una carpeta
"""

from __future__ import annotations

import sys
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
ARCHIVO_SALIDA = CARPETA_PROYECTO / "contexto_ia.txt"
EXTENSIONES = {".py", ".sql", ".html", ".css", ".js", ".md", ".txt", ".toml"}
IGNORAR = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    "instance",
    "vendor",
}
SIEMPRE_PRIMERO = ["AGENTS.md", "README.md", "app/schema.sql"]


def archivos_de(carpetas: list[Path]) -> list[Path]:
    encontrados = []
    for carpeta in carpetas:
        rutas = [carpeta] if carpeta.is_file() else sorted(carpeta.rglob("*"))
        for ruta in rutas:
            relativa = ruta.relative_to(CARPETA_PROYECTO)
            if (
                ruta.is_file()
                and ruta.suffix in EXTENSIONES
                and not IGNORAR.intersection(relativa.parts)
                and ruta != ARCHIVO_SALIDA
                and "docs" not in relativa.parts
            ):
                encontrados.append(ruta)
    return encontrados


def main() -> None:
    pedidas = [CARPETA_PROYECTO / arg for arg in sys.argv[1:]] or [
        CARPETA_PROYECTO / "app",
        CARPETA_PROYECTO / "tests",
    ]
    primeros = [CARPETA_PROYECTO / nombre for nombre in SIEMPRE_PRIMERO]
    archivos = list(dict.fromkeys(p for p in primeros + archivos_de(pedidas) if p.exists()))

    partes = [
        "Este es el código completo de nuestro proyecto (Flask + SQLite). "
        "Respetá las reglas de AGENTS.md. Cuando propongas cambios, indicá el archivo "
        "y mostrá la función o el bloque completo a reemplazar.\n"
    ]
    for archivo in archivos:
        relativa = archivo.relative_to(CARPETA_PROYECTO).as_posix()
        partes.append(f"\n===== ARCHIVO: {relativa} =====\n{archivo.read_text(encoding='utf-8')}")

    texto = "".join(partes)
    ARCHIVO_SALIDA.write_text(texto, encoding="utf-8")
    print(f"Listo: {ARCHIVO_SALIDA.name} ({len(archivos)} archivos, ~{len(texto) // 4:,} tokens)")


if __name__ == "__main__":
    main()
