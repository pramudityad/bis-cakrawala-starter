-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE VIEW v_revenue_bridge AS
WITH bulanan AS (
    SELECT substr(CAST(f.order_ts AS VARCHAR), 1, 7) AS bulan,
           c.channel,
           sum(f.qty)          AS qty,
           sum(f.neto)         AS omzet,
           sum(f.neto) / NULLIF(sum(f.qty), 0) AS harga_rata2
    FROM fact_order_line f
    JOIN dim_channel c ON c.channel_sk = f.channel_sk
    GROUP BY 1, 2
),
banding AS (
    SELECT *,
           lag(bulan)  OVER (PARTITION BY channel ORDER BY bulan) AS bulan_lalu,
           lag(qty)    OVER (PARTITION BY channel ORDER BY bulan) AS qty_lalu,
           lag(omzet)  OVER (PARTITION BY channel ORDER BY bulan) AS omzet_lalu,
           lag(harga_rata2) OVER (PARTITION BY channel ORDER BY bulan) AS harga_lalu
    FROM bulanan
)
SELECT bulan,
       channel,
       
       (qty - qty_lalu) * harga_lalu                        AS volume_effect,
       
       (harga_rata2 - harga_lalu) * qty_lalu                AS price_effect,
       
       
       
       (omzet - omzet_lalu)
         - ((qty - qty_lalu) * harga_lalu)
         - ((harga_rata2 - harga_lalu) * qty_lalu)         AS mix_effect
FROM banding
WHERE bulan_lalu IS NOT NULL;
