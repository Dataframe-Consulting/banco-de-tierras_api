-- TABLES
CREATE TABLE IF NOT EXISTS user_model (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS propietario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    rfc VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS socio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS propietario_socio (
    propietario_id INT NOT NULL REFERENCES propietario(id) ON DELETE CASCADE,
    socio_id INT NOT NULL REFERENCES socio(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (propietario_id, socio_id)
);
CREATE TABLE IF NOT EXISTS sociedad (
    id SERIAL PRIMARY KEY,
    -- 12.50, 20, 45, 100
    porcentaje_participacion DECIMAL(5, 2) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS situacion_fisica (
    id SERIAL PRIMARY KEY,
    -- BREÑA, CONSTRUIDO, ETC.
    nombre VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS vocacion (
    id SERIAL PRIMARY KEY,
    -- COMERCIALIZACIÓN, DESARROLLO, ETC.
    valor VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS vocacion_especifica (
    id SERIAL PRIMARY KEY,
    -- VENTA/APORTACIÓN, VENTA/RENTA, ETC.
    valor VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS proyecto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    superficie_total FLOAT NOT NULL,
    esta_activo BOOLEAN NOT NULL DEFAULT TRUE,
    comentarios TEXT,
    situacion_fisica_id INT NOT NULL REFERENCES situacion_fisica(id) ON DELETE CASCADE,
    vocacion_id INT NOT NULL REFERENCES vocacion(id) ON DELETE CASCADE,
    vocacion_especifica_id INT NOT NULL REFERENCES vocacion_especifica(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS propietario_proyecto (
    propietario_id INT NOT NULL REFERENCES propietario(id) ON DELETE CASCADE,
    proyecto_id INT NOT NULL REFERENCES proyecto(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (propietario_id, proyecto_id)
);
CREATE TABLE IF NOT EXISTS ubicacion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS garantia (
    id SERIAL PRIMARY KEY,
    beneficiario VARCHAR(255) NOT NULL,
    monto FLOAT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS proceso_legal (
    id SERIAL PRIMARY KEY,
    abogado VARCHAR(255) NOT NULL,
    tipo_proceso VARCHAR(255) NOT NULL,
    estatus VARCHAR(255) NOT NULL,
    comentarios TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS propiedad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    superficie FLOAT NOT NULL,
    valor_comercial FLOAT NOT NULL,
    anio_valor_comercial SMALLINT,
    clave_catastral VARCHAR(255) NOT NULL UNIQUE,
    base_predial DECIMAL(10, 2) NOT NULL,
    adeudo_predial DECIMAL(10, 2),
    anios_pend_predial INT,
    comentarios TEXT,
    proyecto_id INT NOT NULL REFERENCES proyecto(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS ubicacion_propiedad (
    ubicacion_id INT NOT NULL REFERENCES ubicacion(id) ON DELETE CASCADE,
    propiedad_id INT NOT NULL REFERENCES propiedad(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ubicacion_id, propiedad_id)
);
CREATE TABLE IF NOT EXISTS garantia_propiedad (
    garantia_id INT NOT NULL REFERENCES garantia(id) ON DELETE CASCADE,
    propiedad_id INT NOT NULL REFERENCES propiedad(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (garantia_id, propiedad_id)
);
CREATE TABLE IF NOT EXISTS proceso_legal_propiedad (
    proceso_legal_id INT NOT NULL REFERENCES proceso_legal(id) ON DELETE CASCADE,
    propiedad_id INT NOT NULL REFERENCES propiedad(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (proceso_legal_id, propiedad_id)
);
CREATE TABLE IF NOT EXISTS sociedad_propiedad (
    sociedad_id INT NOT NULL REFERENCES sociedad(id) ON DELETE CASCADE,
    propiedad_id INT NOT NULL REFERENCES propiedad(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS renta(
    id SERIAL PRIMARY KEY,
    nombre_comercial VARCHAR(255) NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    renta_sin_iva DECIMAL(10, 2) NOT NULL,
    meses_deposito_garantia INT NOT NULL,
    -- deposito_garantia_monto DECIMAL(10, 2), SE CALCULA (renta_sin_iva * meses_deposito_garantia)
    meses_gracia INT NOT NULL,
    meses_gracia_fecha_inicio DATE,
    meses_gracia_fecha_fin DATE,
    meses_renta_anticipada INT NOT NULL,
    renta_anticipada_fecha_inicio DATE,
    renta_anticipada_fecha_fin DATE,
    -- renta_anticipada_renta_sin_iva FLOAT, SE CALCULA (renta_sin_iva * meses_renta_anticipada)
    incremento_mes VARCHAR(255) NOT NULL,
    incremento_nota VARCHAR(255),
    inicio_vigencia DATE NOT NULL,
    fin_vigencia_forzosa DATE NOT NULL,
    fin_vigencia_no_forzosa DATE,
    vigencia_nota VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS propiedad_renta(
    propiedad_id INT NOT NULL REFERENCES propiedad(id) ON DELETE CASCADE,
    renta_id INT NOT NULL REFERENCES renta(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (propiedad_id, renta_id)
);
-- INDEXES
CREATE INDEX IF NOT EXISTS idx_propietario_socio ON propietario_socio(propietario_id, socio_id);
CREATE INDEX IF NOT EXISTS idx_socio_propietario ON propietario_socio(socio_id, propietario_id);
CREATE INDEX IF NOT EXISTS idx_propietario_proyecto ON propietario_proyecto(propietario_id, proyecto_id);
CREATE INDEX IF NOT EXISTS idx_proyecto_propietario ON propietario_proyecto(proyecto_id, propietario_id);
CREATE INDEX IF NOT EXISTS idx_ubicacion_propiedad ON ubicacion_propiedad(ubicacion_id, propiedad_id);
CREATE INDEX IF NOT EXISTS idx_propiedad_ubicacion ON ubicacion_propiedad(propiedad_id, ubicacion_id);
CREATE INDEX IF NOT EXISTS idx_garantia_propiedad ON garantia_propiedad(garantia_id, propiedad_id);
CREATE INDEX IF NOT EXISTS idx_propiedad_garantia ON garantia_propiedad(propiedad_id, garantia_id);
CREATE INDEX IF NOT EXISTS idx_proceso_legal_propiedad ON proceso_legal_propiedad(proceso_legal_id, propiedad_id);
CREATE INDEX IF NOT EXISTS idx_propiedad_proceso_legal ON proceso_legal_propiedad(propiedad_id, proceso_legal_id);
CREATE INDEX IF NOT EXISTS idx_propiedad_renta ON propiedad_renta(propiedad_id, renta_id);
CREATE INDEX IF NOT EXISTS idx_renta_propiedad ON propiedad_renta(renta_id, propiedad_id);
-- TRIGGERS
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER AS $$ BEGIN IF NEW.* IS DISTINCT
FROM OLD.* THEN NEW.updated_at = CURRENT_TIMESTAMP;
END IF;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;
DROP TRIGGER IF EXISTS set_updated_at ON user_model;
DROP TRIGGER IF EXISTS set_updated_at ON propietario;
DROP TRIGGER IF EXISTS set_updated_at ON socio;
DROP TRIGGER IF EXISTS set_updated_at ON sociedad;
DROP TRIGGER IF EXISTS set_updated_at ON situacion_fisica;
DROP TRIGGER IF EXISTS set_updated_at ON vocacion;
DROP TRIGGER IF EXISTS set_updated_at ON vocacion_especifica;
DROP TRIGGER IF EXISTS set_updated_at ON proyecto;
DROP TRIGGER IF EXISTS set_updated_at ON ubicacion;
DROP TRIGGER IF EXISTS set_updated_at ON propiedad;
DROP TRIGGER IF EXISTS set_updated_at ON garantia;
DROP TRIGGER IF EXISTS set_updated_at ON proceso_legal;
DROP TRIGGER IF EXISTS set_updated_at ON renta;
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON user_model FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON propietario FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON socio FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON sociedad FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON situacion_fisica FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON vocacion FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON vocacion_especifica FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON proyecto FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON ubicacion FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON propiedad FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON garantia FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON proceso_legal FOR EACH ROW EXECUTE FUNCTION set_updated_at();
CREATE TRIGGER set_updated_at BEFORE
UPDATE ON renta FOR EACH ROW EXECUTE FUNCTION set_updated_at();