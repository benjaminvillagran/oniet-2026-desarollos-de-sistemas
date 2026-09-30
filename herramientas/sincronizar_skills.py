"""Copia las skills de Claude Code (.claude/skills) a Antigravity (.agents/skills).

La fuente de verdad es .claude/skills: editar ahí y después ejecutar
    python herramientas/sincronizar_skills.py
El test tests/test_config_ia.py falla si las dos copias no son iguales.
"""

from __future__ import annotations

import shutil
from pathlib import Path

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
ORIGEN = CARPETA_PROYECTO / ".claude" / "skills"
DESTINO = CARPETA_PROYECTO / ".agents" / "skills"


def main() -> None:
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    shutil.copytree(ORIGEN, DESTINO)
    nombres = sorted(carpeta.name for carpeta in DESTINO.iterdir() if carpeta.is_dir())
    print(f"Skills sincronizadas ({len(nombres)}): {', '.join(nombres)}")


if __name__ == "__main__":
    main()
