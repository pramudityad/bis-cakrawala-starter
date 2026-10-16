-- ============================================================
-- 40_analytics/trend_per_channel.sql — Sesi 12, langkah 1d. DIBERIKAN.
--
-- Ini pertanyaan PERTAMA yang bisa dijawab warehouse-mu, dan jawabannya belum bisa diberikan
-- oleh satu angka gabungan di slide pembuka: omzet per channel per pekan.
--
-- Jalankan setelah load selesai:
--   python -c "import duckdb;print(duckdb.connect('warehouse/t4.duckdb').sql(open('sql/40_analytics/trend_per_channel.sql').read()))"
-- ============================================================

SELECT
    date_trunc('week', f.order_ts) AS awal_pekan,
    c.channel,
    sum(f.neto)                    AS omzet,
    count(DISTINCT f.order_id)     AS pesanan
FROM fact_order_line f
JOIN dim_channel c ON c.channel_sk = f.channel_sk
GROUP BY 1, 2
ORDER BY 1, 2;
