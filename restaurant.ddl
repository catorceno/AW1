CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS content;

-- 1. menu_categories
-- ---------------------------------------------------------------------
CREATE TABLE content.menu_categories (
    menu_category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name               TEXT NOT NULL,
    creation_date      TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT uq_menu_categories_name UNIQUE (name)
);

-- 2. menu_items
-- ---------------------------------------------------------------------
CREATE TABLE content.menu_items (
    menu_item_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_category_id UUID NOT NULL REFERENCES content.menu_categories (menu_category_id),
    name             TEXT NOT NULL,
    description      TEXT,
    status           TEXT NOT NULL DEFAULT 'available',
    creation_date    TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT uq_menu_items_category_name UNIQUE (menu_category_id, name),
    CONSTRAINT ck_menu_items_status CHECK (status IN ('available', 'sold_out', 'discontinued'))
);

-- 3. menu_item_prices
-- ---------------------------------------------------------------------
CREATE TABLE content.menu_item_prices (
    menu_item_price_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    menu_item_id       UUID NOT NULL REFERENCES content.menu_items (menu_item_id),
    name               TEXT NOT NULL DEFAULT 'único',
    price              NUMERIC(10,2) NOT NULL,
    creation_date      TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT uq_menu_item_prices_item_name UNIQUE (menu_item_id, name),
    CONSTRAINT ck_menu_item_prices_name CHECK (name IN ('único', 'simple', 'doble')),
    CONSTRAINT ck_menu_item_prices_price CHECK (price > 0)
);

-- 4. customers
-- ---------------------------------------------------------------------
CREATE TABLE content.customers (
    customer_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name    TEXT,
    last_name     TEXT,
    email         TEXT NOT NULL,
    creation_date TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT uq_customers_email UNIQUE (email) 
);

-- 5. orders
-- ---------------------------------------------------------------------
CREATE TABLE content.orders (
    order_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id   UUID NOT NULL REFERENCES content.customers (customer_id),
    status        TEXT NOT NULL DEFAULT 'preparing',
    total         NUMERIC(10,2),
    creation_date TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT ck_orders_status CHECK (status IN ('preparing', 'served', 'paid')),
    CONSTRAINT ck_orders_total CHECK (total > 0) 
);

-- 6. order_items
-- ---------------------------------------------------------------------
CREATE TABLE content.order_items (
    order_item_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id           UUID NOT NULL REFERENCES content.orders (order_id),
    menu_item_price_id UUID NOT NULL REFERENCES content.menu_item_prices (menu_item_price_id),
    quantity           INTEGER NOT NULL,
    unit_price         NUMERIC(10,2) NOT NULL,
    subtotal           NUMERIC(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    creation_date      TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_order_items_quantity CHECK (quantity > 0),
    CONSTRAINT ck_order_items_unit_price CHECK (unit_price > 0)
);