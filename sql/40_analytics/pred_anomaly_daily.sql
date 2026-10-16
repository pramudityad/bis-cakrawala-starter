-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE pred_anomaly_daily AS
WITH harian AS (
    SELECT CAST(f.order_ts AS DATE) AS tanggal, c.channel AS channel, sum(f.neto) AS revenue
    FROM fact_order_line f
    JOIN dim_channel c ON c.channel_sk = f.channel_sk
    GROUP BY 1, 2
),
jendela AS (
    SELECT tanggal, channel, revenue,
           avg(revenue)        OVER w AS rerata_28,
           stddev_pop(revenue) OVER w AS simpangan_28,
           count(*)            OVER w AS hari_dalam_jendela
    FROM harian
    WINDOW w AS (PARTITION BY channel ORDER BY tanggal
                 ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING)
)
SELECT tanggal, channel, revenue,
       (revenue - rerata_28) / NULLIF(simpangan_28, 0) AS zscore,
       abs((revenue - rerata_28) / NULLIF(simpangan_28, 0)) > 2 AS anomaly_flag,
       'z28-v1' AS model_version,
       now()    AS scored_at
FROM jendela
WHERE hari_dalam_jendela = 28;
