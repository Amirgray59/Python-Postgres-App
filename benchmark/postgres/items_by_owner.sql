-- BEFORE
DROP INDEX IF EXISTS ix_items_owner_id;

EXPLAIN ANALYZE
SELECT *
FROM items
WHERE owner_id = 1;

-- AFTER
CREATE INDEX ix_items_owner_id ON items (owner_id);

EXPLAIN ANALYZE
SELECT *
FROM items
WHERE owner_id = 1;
