-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE quarantine_items AS
SELECT i.item_id, i.order_id, i.product_id,
       TRY_CAST(i.qty AS INTEGER)         AS qty,
       TRY_CAST(i.harga_satuan AS BIGINT) AS harga_satuan,
       TRY_CAST(i.diskon AS BIGINT)       AS diskon,
       CASE WHEN NOT EXISTS (SELECT 1 FROM stg_orders o WHERE o.order_id = i.order_id)
            THEN 'tanpa order induk' ELSE 'qty negatif' END AS alasan
FROM read_csv_auto('{D}/order_items.csv', all_varchar=true) i
WHERE NOT EXISTS (SELECT 1 FROM stg_orders o WHERE o.order_id = i.order_id)
   OR TRY_CAST(i.qty AS INTEGER) < 0;

CREATE OR REPLACE TABLE stg_order_items AS
SELECT i.item_id, i.order_id, i.product_id,
       TRY_CAST(i.qty AS INTEGER)         AS qty,
       TRY_CAST(i.harga_satuan AS BIGINT) AS harga_satuan,
       TRY_CAST(i.diskon AS BIGINT)       AS diskon,
       TRY_CAST(i.qty AS INTEGER) * TRY_CAST(i.harga_satuan AS BIGINT)
           - TRY_CAST(i.diskon AS BIGINT) AS neto
FROM read_csv_auto('{D}/order_items.csv', all_varchar=true) i
WHERE i.item_id NOT IN (SELECT item_id FROM quarantine_items WHERE item_id IS NOT NULL);
