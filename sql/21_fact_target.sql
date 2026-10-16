-- ============================================================
-- 21_fact_target.sql — Sesi 13, langkah 2a. Bagianmu.
--
-- GRAIN: satu baris = satu target omzet untuk satu bulan, satu channel, satu wilayah.
--
-- Kunci alaminya `bulan, channel, wilayah` — dan itulah yang membuat load aman dijalankan dua kali,
-- sama seperti aturan Sesi 4 dan Sesi 12.
--
-- Dua hal yang harus benar, dan keduanya dinilai di Cek 2a:
--   1. Nilai `wilayah` di `targets.csv` HARUS sama persis dengan yang dipakai `dim_store`.
--      Satu huruf beda, dan join-nya membuang baris tanpa pesan error.
--   2. Sel di `targets.csv` yang kosong tetap NULL di sini. Bukan 0.
--      Nol berarti "kita memang menargetkan nol". Kosong berarti "belum ada yang menetapkan".
--      Dua hal itu berbeda, dan dashboard yang mencampurnya berbohong dua kali.
--
-- TODO: tulis DDL fact_target dari targets.csv, lalu HAPUS kata TODO ini supaya loader boleh jalan.
SELECT
    '2025-01' AS bulan, '' AS channel, '' AS wilayah, CAST(NULL AS BIGINT) AS target_revenue,
    CAST(NULL AS INTEGER) AS target_sk
WHERE FALSE;

-- Bukti yang harus hijau di Cek 2a:
--   SELECT count(*) FROM fact_target WHERE target_revenue IS NULL;   -- > 0 (bulan APP yang kosong)
--   SELECT count(*) FROM fact_target WHERE target_revenue = 0;       -- harus 0
