-- ============================================================
-- 20_dim_store.sql — Sesi 12, langkah 1c. Bagianmu (3 dari 5 dimensi dimulai di sini).
--
-- Grain: satu baris = satu gerai.
-- Kolom yang wajib ada: surrogate key, kunci bisnis (store_id), nama, kota, wilayah, tipe, aktif.
--
-- Satu keputusan yang harus kamu ambil dan tulis alasannya:
--   Ada satu gerai yang sudah TUTUP. Apakah ia tetap masuk dimensi?
--   Pikirkan baris fact tahun ini yang menunjuk ke gerai itu. Kalau gerainya hilang dari dimensi,
--   ke mana omzet historisnya pergi?
--
-- TODO: tulis DDL dim_store + anggota Unknown (store_sk = -1), tulis alasan satu baris,
--       lalu HAPUS kata TODO ini supaya loader boleh jalan.
--       Alasan: ______________________________________________________________
SELECT
    1 AS store_sk, '' AS store_id, '' AS nama, '' AS kota, '' AS wilayah, '' AS tipe, TRUE AS aktif
WHERE FALSE;
