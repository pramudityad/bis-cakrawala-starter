-- ============================================================
-- sql/load_t4_langkah2.sql — URUTAN EKSEKUSI T4, Sesi 13 (langkah 2)
--
-- Jalankan MALAM SESI 13:
--   python -m pipeline.load --topic t4 --twice --sql sql/load_t4_langkah2.sql
--
-- Isinya = seluruh langkah 1, ditambah tabel target dan view KPI. Karena semuanya
-- CREATE OR REPLACE, menjalankan ulang seluruh rantai tetap idempoten dan hasilnya sama.
--
-- Kenapa berkas terpisah per langkah: gerbang pekerjaan-belum-selesai memeriksa SELURUH berkas yang ikut terbaca.
-- Kalau langkah 2 dan 3 ikut di sini, malam Sesi 12 tidak akan bisa load — padahal bagian itu
-- memang belum kamu kerjakan. Berkas per langkah membuat tiap malam punya satu perintah yang jelas.
-- ============================================================

SOURCE sql/load_t4.sql;              -- seluruh langkah 1 (Sesi 12)

SOURCE sql/20_dim_target.sql;        -- bagianmu: definisi target + arti nilai kosong
SOURCE sql/21_fact_target.sql;       -- bagianmu: grain bulan × channel × wilayah
SOURCE sql/30_v_kpi_monthly.sql;     -- bagianmu: attainment, dan NULL saat target NULL
