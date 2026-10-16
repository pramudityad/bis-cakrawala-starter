-- ============================================================
-- 20_dim_target.sql — Sesi 13, langkah 2a. Bagianmu.
--
-- Grain: satu baris = satu definisi target.
--
-- Kenapa target punya TABEL SENDIRI dan bukan satu kolom di fact penjualan:
-- bisnis menetapkan ulang target setiap periode tanpa menyentuh satu pun baris pesanan.
-- Siklus hidupnya berbeda, jadi tabelnya berbeda.
--
-- Yang wajib ada: surrogate key, pemilik target (JABATAN, bukan tim), periode berlaku,
-- dan siapa yang boleh merevisi.
--
-- TODO: tulis DDL dim_target + anggota Unknown, lalu HAPUS kata TODO ini supaya loader boleh jalan.
--       Tulis juga di sini, sebagai komentar, arti nilai kosong pada target_revenue:
--         "target kosong berarti: ________________________________________"
SELECT
    1 AS target_sk, '' AS definisi, '' AS pemilik_jabatan,
    DATE '2025-01-01' AS valid_from, DATE '9999-12-31' AS valid_to, '' AS boleh_revisi_oleh
WHERE FALSE;
