-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE VIEW v_kpi_monthly AS
WITH aktual AS (
    SELECT substr(CAST(f.order_ts AS VARCHAR), 1, 7) AS bulan,
           c.channel,
           coalesce(nullif(st.wilayah, 'TIDAK DIKETAHUI'), cu.wilayah) AS wilayah,
           sum(f.neto)                AS net_revenue,
           count(DISTINCT f.order_id_degenerate) AS orders
    FROM fact_order_line f
    JOIN dim_channel c  ON c.channel_sk = f.channel_sk
    JOIN dim_store st   ON st.store_sk = f.store_sk
    JOIN dim_customer cu ON cu.customer_sk = f.customer_sk
    GROUP BY 1, 2, 3
),
retur AS (
    
    
    SELECT substr(CAST(f.order_ts AS VARCHAR), 1, 7) AS bulan,
           c.channel,
           coalesce(nullif(st.wilayah, 'TIDAK DIKETAHUI'), cu.wilayah) AS wilayah,
           count(DISTINCT r.return_id) AS jumlah_retur
    FROM stg_returns r
    JOIN fact_order_line f ON f.item_id_degenerate = r.item_id
    JOIN dim_channel c   ON c.channel_sk = f.channel_sk
    JOIN dim_store st    ON st.store_sk = f.store_sk
    JOIN dim_customer cu ON cu.customer_sk = f.customer_sk
    GROUP BY 1, 2, 3
)
SELECT a.bulan,
       a.channel,
       a.wilayah,
       a.net_revenue,
       a.orders,
       
       
       coalesce(r.jumlah_retur, 0)::DOUBLE / NULLIF(a.orders, 0) AS return_rate,
       t.target_revenue,
       CASE WHEN t.target_revenue IS NULL THEN NULL
            ELSE CAST(a.net_revenue AS DOUBLE) / t.target_revenue * 100 END AS attainment_pct
FROM aktual a
LEFT JOIN fact_target t
       ON t.bulan = a.bulan AND t.channel = a.channel AND t.wilayah = a.wilayah
LEFT JOIN retur r
       ON r.bulan = a.bulan AND r.channel = a.channel AND r.wilayah = a.wilayah;
