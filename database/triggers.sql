-- Mantiene sincronizada content.orders.total con la suma de content.order_items.subtotal.
--
-- content.orders.total no se carga a mano: se recalcula automáticamente cada vez que
-- se agrega, modifica o elimina una línea de pedido (order_item). Así una orden nunca
-- queda con un total desactualizado respecto de sus líneas.

-- 1. Función que recalcula el total de UNA orden puntual.
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION content.fn_recalcular_total_orden()
RETURNS TRIGGER AS $$
DECLARE
    id_orden_afectada UUID;
BEGIN
    -- En DELETE, la fila afectada viaja en OLD; en INSERT/UPDATE, en NEW.
    IF TG_OP = 'DELETE' THEN
        id_orden_afectada := OLD.order_id;
    ELSE
        id_orden_afectada := NEW.order_id;
    END IF;

    -- NULLIF(..., 0): si la orden se queda sin items el total pasa a NULL en vez de 0,
    -- porque la restricción ck_orders_total exige total > 0 (y NULL sí la satisface).
    UPDATE content.orders
    SET total = NULLIF(
        (SELECT COALESCE(SUM(subtotal), 0)
         FROM content.order_items
         WHERE order_id = id_orden_afectada),
        0
    )
    WHERE order_id = id_orden_afectada;

    -- Si un UPDATE reasigna el item a otra orden (cambia order_id), la orden de origen
    -- también perdió una línea y hay que recalcularla aparte.
    IF TG_OP = 'UPDATE' AND OLD.order_id <> NEW.order_id THEN
        UPDATE content.orders
        SET total = NULLIF(
            (SELECT COALESCE(SUM(subtotal), 0)
             FROM content.order_items
             WHERE order_id = OLD.order_id),
            0
        )
        WHERE order_id = OLD.order_id;
    END IF;

    RETURN NULL; -- trigger AFTER: el valor de retorno se ignora
END;
$$ LANGUAGE plpgsql;

-- 2. Trigger sobre order_items que dispara la función anterior.
-- ---------------------------------------------------------------------
DROP TRIGGER IF EXISTS trg_order_items_actualizar_total ON content.order_items;

CREATE TRIGGER trg_order_items_actualizar_total
AFTER INSERT OR DELETE OR UPDATE OF quantity, unit_price, order_id
ON content.order_items
FOR EACH ROW
EXECUTE FUNCTION content.fn_recalcular_total_orden();
