-- Estructura de la base de datos (SQLite).
-- Se ejecuta sola al iniciar el sistema. Si cambian una tabla, reinicien la base:
--     flask --app run reiniciar-db      (o borren el archivo instance/datos.db)

-- Registro de cada archivo importado (sirve para auditar qué se cargó y cuándo)
CREATE TABLE IF NOT EXISTS importaciones (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_archivo  TEXT    NOT NULL,
    fecha_hora      TEXT    NOT NULL,
    filas_leidas    INTEGER NOT NULL,
    filas_guardadas INTEGER NOT NULL,
    filas_con_error INTEGER NOT NULL
);

-- Datos del problema. En la plantilla: ventas de un comercio.
CREATE TABLE IF NOT EXISTS ventas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha           TEXT    NOT NULL,                      -- formato AAAA-MM-DD
    producto        TEXT    NOT NULL,
    categoria       TEXT    NOT NULL,
    cantidad        INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario REAL    NOT NULL CHECK (precio_unitario >= 0),
    total           REAL    NOT NULL,                      -- calculado: cantidad * precio_unitario
    importacion_id  INTEGER REFERENCES importaciones (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_ventas_fecha ON ventas (fecha);
CREATE INDEX IF NOT EXISTS idx_ventas_categoria ON ventas (categoria);
