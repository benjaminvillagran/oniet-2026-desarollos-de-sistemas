---
name: probar-en-navegador
description: Prueba el sistema web como lo haría el jurado, recorriendo todas las pantallas en el navegador con datos reales y con datos con errores, y reporta fallas con capturas. Usar después de terminar una funcionalidad y antes de la entrega.
---

# Probar el sistema en el navegador

Precondición: el sistema ya está corriendo en http://127.0.0.1:5000, iniciado por la persona en
su propia terminal con `python run.py`. **No inicies el servidor vos**: en Windows la terminal del
agente se queda en "Running…" con procesos que no terminan. Si no responde, pedí que lo inicien.

En Antigravity usá el agente de navegador (`/browser`). En Claude Code, si no hay navegador
disponible, hacé las mismas pruebas con el cliente de pruebas de Flask
(`app.test_client()`, como en `tests/test_rutas.py`).

## Recorrido

1. **Inicio**: carga sin errores y muestra el estado vacío o los indicadores.
2. **Importar** el archivo de datos de la consigna (en `data/ejemplos/`): verificá la cantidad de
   filas leídas y guardadas.
3. **Importar un archivo con errores**: el sistema no se rompe y muestra fila, campo y motivo.
4. **Listado**: buscar, filtrar, ordenar por cada columna, cambiar de página, eliminar un registro
   (tiene que pedir confirmación).
5. **Alta manual**: primero con campos vacíos (tienen que aparecer los errores) y después bien.
6. **Estadísticas**: los números coinciden con un cálculo hecho a mano sobre 2 o 3 registros; los
   gráficos se ven.
7. **Exportar CSV**: se descarga y se abre bien.
8. **Página inexistente** (`/no-existe`): muestra la página 404 del sistema.
9. **Pantalla angosta** (celular): nada se corta ni se superpone.

## Reporte

Tabla con: pantalla, qué se probó, resultado (OK o falla) y captura si falló. Ordená las fallas de
más grave (datos incorrectos o error) a menos grave (detalle visual).
