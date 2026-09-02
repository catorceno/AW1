-- 1. restaurantes
CREATE TABLE restaurantes (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(120) NOT NULL,
    ciudad      VARCHAR(80)  NOT NULL,
    direccion   VARCHAR(200),
    telefono    VARCHAR(30)
);

-- 2. platos
CREATE TABLE platos (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(120)  NOT NULL,
    precio          NUMERIC(10,2) NOT NULL,
    disponible      BOOLEAN       NOT NULL DEFAULT TRUE,
    restaurante_id  INTEGER       NOT NULL,

    CONSTRAINT chk_platos_precio_positivo CHECK (precio > 0),
    CONSTRAINT fk_platos_restaurante
        FOREIGN KEY (restaurante_id)
        REFERENCES restaurantes (id)
        ON DELETE CASCADE
);