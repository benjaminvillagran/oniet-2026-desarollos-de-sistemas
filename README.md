# Logística Nacional · Análisis de servicios

[![Verificación](https://github.com/benjaminvillagran/oniet-2026-desarollos-de-sistemas/actions/workflows/verificacion.yml/badge.svg)](https://github.com/benjaminvillagran/oniet-2026-desarollos-de-sistemas/actions/workflows/verificacion.yml)

Sistema web desarrollado para **ONIET 2026 · Desarrollo de Sistemas** por el **Equipo 14**.

| Integrante | Rol |
|---|---|
| Benjamin Francisco Villagran | Integración y procesamiento de datos |
| Damian Alvaro Arena | Interfaz y usabilidad |
| Ruben Daniel Tapia | Pruebas, datos y documentación |

## Problema que resuelve

La empresa Logística Nacional tiene un registro histórico de sus servicios de distribución de
2024, 2025 y 2026: operador logístico, año, mes, cantidad de envíos, región, costo por envío y
porcentaje de entregas a tiempo. El sistema **carga** ese archivo (CSV o JSON), **valida** cada
registro, **calcula** el costo total, lo **guarda** en una base de datos y **genera los 3 informes**
de la consigna para el período que elija el usuario, sin modificar el código fuente.

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Abrir http://127.0.0.1:5000. En Windows también se puede hacer doble clic en `iniciar.bat`
(crea el entorno, instala y abre el sistema).

### Cómo usarlo

1. **Importar** → *Elegir archivo* → `data/ejemplos/ONIET-2026-Logistica.csv` (o el `.json`).
   Resultado: "Se guardaron 180 de 180 filas".
2. **Informes** → los 3 informes con sus gráficos. El período se elige con los botones
   *Todo el período / 2024 / 2025 / 2026* o con *Desde* y *Hasta* (mes y año).
3. **Servicios** → todos los registros con filtros (período, operador, región), orden por columna,
   fila de totales, detalle de cada registro y exportación a CSV.
4. Para ver la validación: importar `data/ejemplos/servicios_con_errores.csv`. El sistema no se
   rompe: guarda las filas válidas e informa fila, campo y motivo de cada error.

## Funcionalidades

| Requisito de la consigna | Dónde se cumple |
|---|---|
| Cargar los datos desde el archivo (CSV o JSON) | Pantalla *Importar* (`app/servicios/lector.py`, `app/servicios/validacion.py`) |
| Procesar: Costo total = CantidadEnvios × CostoPorEnvio | Se calcula al importar (`completar_servicio` en `app/servicios/procesamiento.py`) |
| Almacenar la información | SQLite (`app/schema.sql`, `app/repositorios/servicios_repositorio.py`) |
| Reporte 1 — Ranking de operadores: Posición, Operador, Total envíos, Costo total | Pantalla *Informes* (`ranking_operadores`) |
| Reporte 2 — Ranking de regiones: Posición, Región, Cantidad de envíos | Pantalla *Informes* (`ranking_regiones`) |
| Reporte 3 — Nivel de cumplimiento: Operador, Promedio entregas a tiempo | Pantalla *Informes* (`cumplimiento_por_operador`) |
| Seleccionar el período a analizar | *Informes* y *Servicios*: desde/hasta mes y año, y botones por año |
| Sin modificar el código fuente | Todo se carga, se elige y se consulta desde la interfaz |
| Extras | Gráficos, listado con filtros y totales, exportación CSV, API JSON (`/api/informes`), historial de importaciones |

## Cómo está hecho

- **Python + Flask + SQLite**: SQLite viene con Python, así que no hace falta instalar un servidor
  de base de datos.
- **Capas**: `rutas/` (páginas) → `servicios/` (leer, validar, procesar) → `repositorios/` (SQL).
- **Estructuras de datos**: diccionarios para acumular por operador y por región, y listas
  ordenadas para los rankings (`app/servicios/procesamiento.py`).
- **Validación fila por fila**: los datos con errores no se guardan y se informa fila, campo y motivo.
- **Seguridad**: consultas SQL con parámetros (sin inyección SQL) y transacciones.
- **Calidad**: tests automáticos con pytest (`python -m pytest`) y workflow de GitHub Actions en
  cada push.

## Decisiones y supuestos

- **Costo total** se calcula por registro al importar y se guarda. Los rankings se calculan al
  consultar, sobre el período elegido.
- **Promedio de entregas a tiempo**: promedio simple de los registros del operador en el período.
- **Empates**: comparten la posición (1, 2, 2, 4) y se ordenan por nombre. Con todos los datos,
  EnvioExpress y TransRuta empatan en 88,64 % (3191 / 36) y los dos figuran en la posición 1.
- **NumeroRegistro no se repite**: un número repetido, en el archivo o ya guardado, se rechaza y
  se informa.
- **Validaciones**: todos los campos son obligatorios; mes entre 1 y 12, año entre 2000 y 2100,
  envíos y costos no negativos, porcentaje entre 0 y 100.
- El archivo de la consigna usa punto decimal (`2707.33`); el sistema también acepta coma decimal.
- Si se importa dos veces el mismo archivo, se detecta y no se duplican los datos.

## Resultados con los datos de la consigna (todo el período)

| Reporte 1 | Operador | Total envíos | Costo total |
|---|---|---|---|
| 1 | AndesLog | 12.426 | $ 37.827.869,23 |
| 2 | CargaNacional | 11.985 | $ 35.815.616,13 |
| 3 | TransRuta | 11.055 | $ 31.535.360,06 |
| 4 | LogisticaSur | 9.673 | $ 30.821.853,80 |
| 5 | EnvioExpress | 10.425 | $ 25.441.637,02 |

| Reporte 2 | Región | Cantidad de envíos |
|---|---|---|
| 1 | Centro | 19.383 |
| 2 | Litoral | 10.718 |
| 3 | Norte | 8.706 |
| 4 | Sur | 8.425 |
| 5 | Cuyo | 8.332 |

| Reporte 3 | Operador | Promedio entregas a tiempo |
|---|---|---|
| 1 | EnvioExpress | 88,64 % |
| 1 | TransRuta | 88,64 % |
| 3 | AndesLog | 87,58 % |
| 4 | CargaNacional | 86,69 % |
| 5 | LogisticaSur | 85,39 % |

Estos valores se calcularon aparte y se comprueban con un test automático
(`tests/test_rutas.py`).

## Limitaciones conocidas

- El promedio de entregas a tiempo no se pondera por la cantidad de envíos (la consigna pide el
  porcentaje promedio).
- Archivos de hasta 5 MB.

## Uso de inteligencia artificial

Usamos asistentes de IA (Claude Code, DeepSeek vía Ollama y Google Antigravity) como herramienta de
apoyo, de acuerdo con el punto 15 del reglamento. Partimos de una plantilla propia preparada antes
de la competencia y la adaptamos a esta consigna. El detalle está en [docs/USO_IA.md](docs/USO_IA.md).
Revisamos y probamos el resultado: comparamos los informes con valores calculados aparte y el
proyecto tiene tests automáticos.