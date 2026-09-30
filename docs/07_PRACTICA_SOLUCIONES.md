# 07 · Soluciones de la práctica (no mirar antes de terminar el simulacro)

Resultados calculados por un programa independiente de la plantilla. Si su sistema da otra cosa, revisen la regla de la consigna o su cálculo.

## Práctica 1 · Biblioteca escolar

- Filas leídas: **33**; válidas: **30**; con error: **3** (filas 32, 33, 34).
- Préstamos pendientes (sin devolver): **3**.
- Préstamos con atraso: **17** (56,7 %).
- Total de multas: **$ 34.350,00**.
- Libros más prestados: Cien años de soledad (8); Rayuela (7); El túnel (4).
- Socios con más multas: Diego Sosa ($ 9.900,00); Ana Gómez ($ 8.850,00); Franco Vera ($ 8.850,00).

## Práctica 2 · Estación meteorológica

- Lecturas: **84**; válidas: **81**; descartadas: **3** (elementos 6, 12, 21).

| Estación | Temp. promedio | Máxima | Mínima | Lluvia total |
|---|---|---|---|---|
| Centro | 29,5 °C | 40,2 °C | 18,9 °C | 108,3 mm |
| Norte | 31,4 °C | 43,8 °C | 21,4 °C | 90,3 mm |
| Sierras | 22,9 °C | 33,1 °C | 12,4 °C | 93,6 mm |

- Alertas de calor (≥ 35 °C): **16** lecturas.
- Día más lluvioso (suma de todas las estaciones): **14/01/2026** con 67,2 mm.

## Práctica 3 · Torneo intercolegial

- Partidos válidos: **15**; rechazados: **2** (filas 17, 18).
- Goles totales: **41**; promedio por partido: **2,73**.
- Partido con más goles (el primero si hay empate): **Colegio Nacional 2 - 3 Instituto San José** (07/08/2026).

| Pos | Equipo | PJ | PG | PE | PP | GF | GC | DG | Pts |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Instituto San José | 5 | 4 | 0 | 1 | 11 | 9 | +2 | **12** |
| 2 | Escuela Técnica 1 | 5 | 2 | 2 | 1 | 7 | 4 | +3 | **8** |
| 3 | Colegio del Sol | 5 | 2 | 2 | 1 | 7 | 6 | +1 | **8** |
| 4 | Escuela Normal | 5 | 2 | 1 | 2 | 7 | 5 | +2 | **7** |
| 5 | Colegio Nacional | 5 | 1 | 1 | 3 | 6 | 11 | -5 | **4** |
| 6 | IPEM 25 | 5 | 0 | 2 | 3 | 3 | 6 | -3 | **2** |

## Práctica 4 · Taller mecánico y aseguradoras (estilo ONIET 2025)

- Registros: **60** (48 del CSV + 12 del JSON). Período **01/2024 a 06/2026**.

Reporte 1 · compañías por total de cobertura (facturado × porcentaje / 100):

| Pos | Compañía | Facturado | Total cobertura |
|---|---|---|---|
| 1 | Cobertura Total | $ 31.315.250,00 | **$ 27.617.332,50** |
| 2 | Aseguradora Andina | $ 26.565.000,00 | **$ 23.863.575,00** |
| 3 | La Protectora | $ 26.972.250,00 | **$ 20.218.587,50** |
| 4 | Seguros del Plata | $ 15.355.500,00 | **$ 12.590.725,00** |

Reporte 2 · regiones por cantidad de servicios:

| Pos | Región | Servicios |
|---|---|---|
| 1 | NOA | **417** |
| 2 | Centro | **387** |
| 3 | Patagonia | **348** |
| 4 | Cuyo | **162** |

## Práctica 5 · Barrios populares y paquetes de ayuda (estilo ONIET 2021)

- Barrios: **27** en 4 provincias.

Totales por provincia (antes de asignar paquetes):

| Provincia | Barrios | Familias |
|---|---|---|
| Buenos Aires | 7 | 1733 |
| Córdoba | 9 | 1700 |
| Mendoza | 7 | 1722 |
| Tucumán | 4 | 1120 |

Las asignaciones de paquetes las carga cada equipo, así que el ranking depende de lo que asignen: verifiquen a mano 2 o 3 barrios (paquetes asignados ÷ familias).
