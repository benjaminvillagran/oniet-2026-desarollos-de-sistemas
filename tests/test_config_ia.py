"""Valida la configuración para las IAs: skills, reglas de Antigravity y CLAUDE.md.

Las restricciones salen de la documentación oficial:
- Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  (name: máx. 64, minúsculas/números/guiones, sin "anthropic" ni "claude";
   description: no vacía, máx. 1024 caracteres).
- Skills en Claude Code: https://code.claude.com/docs/en/skills (.claude/skills/<nombre>/SKILL.md).
- Reglas de Antigravity: trigger always_on | model_decision | glob | manual (.agents/rules/*.md).
- CLAUDE.md importa AGENTS.md con @AGENTS.md: https://code.claude.com/docs/en/memory
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
SKILLS_CLAUDE = RAIZ / ".claude" / "skills"
SKILLS_ANTIGRAVITY = RAIZ / ".agents" / "skills"
REGLAS_ANTIGRAVITY = RAIZ / ".agents" / "rules"
NOMBRE_VALIDO = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TRIGGERS_VALIDOS = {"always_on", "model_decision", "glob", "manual"}


def leer_frontmatter(archivo: Path) -> dict[str, str]:
    """Lee el bloque YAML simple (clave: valor) entre las dos primeras líneas '---'."""
    lineas = archivo.read_text(encoding="utf-8").splitlines()
    assert lineas and lineas[0] == "---", f"{archivo}: la primera línea tiene que ser ---"
    fin = lineas.index("---", 1)
    datos = {}
    for linea in lineas[1:fin]:
        clave, _, valor = linea.partition(":")
        datos[clave.strip()] = valor.strip().strip('"')
    return datos


def carpetas_de_skills(carpeta: Path) -> list[Path]:
    return sorted(ruta for ruta in carpeta.iterdir() if ruta.is_dir())


SKILLS = carpetas_de_skills(SKILLS_CLAUDE)


def test_hay_skills():
    assert len(SKILLS) >= 1


@pytest.mark.parametrize("carpeta", SKILLS, ids=lambda carpeta: carpeta.name)
def test_skill_cumple_la_especificacion(carpeta):
    archivo = carpeta / "SKILL.md"
    assert archivo.exists(), f"falta {archivo}"
    datos = leer_frontmatter(archivo)
    nombre = datos.get("name", "")
    descripcion = datos.get("description", "")

    assert nombre == carpeta.name, "name tiene que ser igual al nombre de la carpeta"
    assert len(nombre) <= 64 and NOMBRE_VALIDO.match(nombre), "name: minúsculas, números y guiones"
    assert "claude" not in nombre and "anthropic" not in nombre, "palabras reservadas en name"
    assert 0 < len(descripcion) <= 1024, "description obligatoria y de máximo 1024 caracteres"
    assert "<" not in descripcion and ">" not in descripcion, "description sin etiquetas XML"
    assert len(archivo.read_text(encoding="utf-8").splitlines()) < 500, "SKILL.md muy largo"


def test_skills_de_antigravity_son_copia_exacta():
    nombres_claude = [carpeta.name for carpeta in SKILLS]
    nombres_antigravity = [carpeta.name for carpeta in carpetas_de_skills(SKILLS_ANTIGRAVITY)]
    assert nombres_claude == nombres_antigravity, (
        "correr: python herramientas/sincronizar_skills.py"
    )
    for carpeta in SKILLS:
        for archivo in carpeta.rglob("*"):
            if archivo.is_file():
                copia = SKILLS_ANTIGRAVITY / archivo.relative_to(SKILLS_CLAUDE)
                assert copia.read_bytes() == archivo.read_bytes(), f"{copia} desactualizado"


@pytest.mark.parametrize(
    "archivo", sorted(REGLAS_ANTIGRAVITY.glob("*.md")), ids=lambda archivo: archivo.name
)
def test_reglas_de_antigravity(archivo):
    datos = leer_frontmatter(archivo)
    assert datos.get("trigger") in TRIGGERS_VALIDOS, "trigger inválido (Antigravity la ignoraría)"
    assert len(archivo.read_bytes()) < 12_000, "regla demasiado larga"


def test_claude_md_importa_agents_md():
    assert (RAIZ / "CLAUDE.md").read_text(encoding="utf-8").splitlines()[0] == "@AGENTS.md"
    assert (RAIZ / "AGENTS.md").exists()


def test_rutas_mencionadas_en_agents_md_existen():
    texto = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
    rutas = set(re.findall(r"`((?:app|tests|herramientas|data|docs)/[\w./-]+)`", texto))
    faltantes = sorted(ruta for ruta in rutas if "*" not in ruta and not (RAIZ / ruta).exists())
    assert not faltantes, f"AGENTS.md menciona rutas que no existen: {faltantes}"


DOCUMENTOS = [RAIZ / "README.md", RAIZ / "AGENTS.md", *sorted((RAIZ / "docs").rglob("*.md"))]


@pytest.mark.parametrize("documento", DOCUMENTOS, ids=lambda documento: documento.name)
def test_links_y_rutas_de_la_documentacion_existen(documento):
    """Los links [texto](ruta) y las rutas `docs/...` citadas apuntan a archivos que existen."""
    texto = documento.read_text(encoding="utf-8")
    faltantes = []
    for destino in re.findall(r"\]\(([^)#\s]+)\)", texto):
        if not destino.startswith(("http://", "https://", "mailto:")):
            if not (documento.parent / destino).exists():
                faltantes.append(destino)
    for ruta in re.findall(r"`(docs/[\w./-]+\.md)`", texto):
        if not (RAIZ / ruta).exists() and ruta not in (
            "docs/ANALISIS.md",
            "docs/USO_IA.md",
            "docs/CONSIGNA.md",
        ):
            faltantes.append(ruta)
    assert not faltantes, f"{documento.name} apunta a archivos que no existen: {faltantes}"
