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
    filas_con_error INTEGER NOT NULL,
    hash_contenido  TEXT                                   -- huella del archivo: detecta repetidos
);

-- Datos del problema: servicios logísticos (consigna ONIET 2026 "Logística Nacional").
CREATE TABLE IF NOT EXISTS servicios (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_registro             INTEGER NOT NULL UNIQUE,              -- correlativo del archivo
    operador_logistico          TEXT    NOT NULL,
    anio                        INTEGER NOT NULL,
    mes                         INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    cantidad_envios             INTEGER NOT NULL CHECK (cantidad_envios >= 0),
    region                      TEXT    NOT NULL,
    costo_por_envio             REAL    NOT NULL CHECK (costo_por_envio >= 0),
    porcentaje_entregas_atiempo REAL    NOT NULL CHECK (porcentaje_entregas_atiempo BETWEEN 0 AND 100),
    costo_total                 REAL    NOT NULL,             -- calculado: cantidad_envios * costo_por_envio
    importacion_id              INTEGER REFERENCES importaciones (id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_servicios_periodo ON servicios (anio, mes);

-- Usuarios: solo se usan si la consigna pide login (LOGIN_OBLIGATORIO = True en config.py)
CREATE TABLE IF NOT EXISTS usuarios (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT    NOT NULL UNIQUE,
    clave_hash     TEXT    NOT NULL,                        -- nunca se guarda la clave real
    creado         TEXT    NOT NULL,
    ultimo_acceso  TEXT
);
