-- Relacionamentos
CREATE TABLE manifestation_products (
    manifestation_id  INT NOT NULL REFERENCES manifestations(id) ON DELETE CASCADE,
    product_id        INT NOT NULL REFERENCES products_services(id) ON DELETE RESTRICT,
    PRIMARY KEY (manifestation_id, product_id)
);

CREATE INDEX idx_manifestations_channel   ON manifestations(channel_id);
CREATE INDEX idx_manifestations_type      ON manifestations(manifestation_type_id);
CREATE INDEX idx_manifestations_created   ON manifestations(created_at);
CREATE INDEX idx_manifestations_sentiment ON manifestations(sentiment);
CREATE INDEX idx_manif_products_product   ON manifestation_products(product_id);