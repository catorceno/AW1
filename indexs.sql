
CREATE INDEX idx_menu_items_menu_category_id ON content.menu_items (menu_category_id);
CREATE INDEX idx_menu_item_prices_menu_item_id ON content.menu_item_prices (menu_item_id);
CREATE INDEX idx_orders_customer_id ON content.orders (customer_id);
CREATE INDEX idx_order_items_order_id ON content.order_items (order_id);
CREATE INDEX idx_order_items_menu_item_price_id ON content.order_items (menu_item_price_id);
