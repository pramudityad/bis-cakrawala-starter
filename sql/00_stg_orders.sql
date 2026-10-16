-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE stg_orders AS
WITH sumber AS (
    SELECT order_id, channel, store_id, customer_ref,
           CASE WHEN order_ts LIKE '%Z'
                THEN TRY_STRPTIME(order_ts, '%Y-%m-%dT%H:%M:%SZ') + INTERVAL 7 HOUR
                ELSE TRY_STRPTIME(order_ts, '%Y-%m-%d %H:%M:%S') END AS order_ts_wib,
           status, fulfillment, payment_method
    FROM read_csv_auto('{D}/orders.csv', all_varchar=true)
),
bersih AS (
    SELECT *,
           CASE upper(trim(status))
               WHEN 'DELIVERED' THEN 'DELIVERED'
               WHEN 'DELIVRD'   THEN 'DELIVERED'
               WHEN 'SELESAI'   THEN 'DELIVERED'
               WHEN 'CANCELLED' THEN 'CANCELLED'
               WHEN 'SHIPPED'   THEN 'SHIPPED'
               WHEN 'PENDING'   THEN 'PENDING'
               ELSE 'TIDAK DIKETAHUI'
           END AS status_clean
    FROM sumber
)
SELECT * FROM bersih
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_ts_wib) = 1;
