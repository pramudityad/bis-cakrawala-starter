-- ============================================================
-- 30_v_kpi_monthly.sql — Sesi 13, langkah 2b. Bagianmu.
--
-- Satu view, satu pertanyaan: apakah channel ini mencapai targetnya bulan ini?
-- Kolomnya sudah ditetapkan dan tidak boleh ditambah:
--     v_kpi_monthly(bulan, channel, wilayah, net_revenue, orders, return_rate,
--                   target_revenue, attainment_pct)
--
-- Sisi aktual: fact_order_line (hasil Sesi 12). Sisi target: fact_target.
-- Join-nya LEFT JOIN. Kalau INNER, bulan-bulan APP yang targetnya belum ditetapkan akan hilang
-- dari view — padahal justru bulan itulah yang harus terlihat: bisnis lupa menetapkannya.
--
-- Bagian yang harus kamu putuskan: attainment_pct saat targetnya NULL.
--   Target ada, omzet nol        → 0.0   (nyata, dan buruk)
--   Target NULL, omzet berapa pun → NULL  (tidak terdefinisi: tidak ada pembandingnya)
-- Jangan pakai COALESCE ke 0. Itu mengubah "belum ditetapkan" jadi "gagal total".
--
-- TODO: tulis view-nya, terutama CASE attainment-nya, lalu HAPUS kata TODO ini.
CREATE OR REPLACE VIEW v_kpi_monthly AS
SELECT
    CAST(NULL AS VARCHAR) AS bulan,
    CAST(NULL AS VARCHAR) AS channel,
    CAST(NULL AS VARCHAR) AS wilayah,
    CAST(NULL AS BIGINT)  AS net_revenue,
    CAST(NULL AS BIGINT)  AS orders,
    CAST(NULL AS DOUBLE)  AS return_rate,
    CAST(NULL AS BIGINT)  AS target_revenue,
    CAST(NULL AS DOUBLE)  AS attainment_pct
WHERE FALSE;

-- Bukti yang harus hijau di Cek 2b:
--   SELECT count(*) FROM v_kpi_monthly WHERE target_revenue IS NULL AND attainment_pct IS NOT NULL;  -- 0
--   SELECT sum(net_revenue) FROM v_kpi_monthly;   -- sama dengan sum(neto) di fact_order_line
