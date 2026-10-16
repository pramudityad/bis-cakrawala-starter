-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE fact_order_line AS
SELECT d.date_sk,
       ch.channel_sk,
       COALESCE(st.store_sk, -1)   AS store_sk,
       COALESCE(p.product_sk, -1)  AS product_sk,
       COALESCE(cu.customer_sk, -1) AS customer_sk,
       o.order_id                  AS order_id_degenerate,
       i.item_id                   AS item_id_degenerate,
       i.qty,                                   
       i.harga_satuan,                          
       i.diskon,                                
       i.neto,                                  
       o.status_clean AS status,
       o.order_ts_wib AS order_ts
FROM stg_order_items i
JOIN stg_orders o ON o.order_id = i.order_id
LEFT JOIN dim_date d ON d.full_date = CAST(o.order_ts_wib AS DATE)
LEFT JOIN dim_channel ch ON ch.channel = o.channel
LEFT JOIN dim_store st ON st.store_id = o.store_id
LEFT JOIN dim_product p ON p.product_id = i.product_id
     AND CAST(o.order_ts_wib AS DATE) BETWEEN p.valid_from AND p.valid_to
LEFT JOIN bridge_customer_ref b ON b.customer_ref = o.customer_ref
LEFT JOIN dim_customer cu ON cu.customer_sk = b.customer_sk;
