-- ============================================================
-- 30_fact_order_line.sql — Sesi 12, langkah 1c. Bagianmu.
--
-- GRAIN (sudah ditulis dosen di Sesi 12, langkah 1c — format baku UTS item 1.1):
--   Satu baris di fact_order_line berarti satu produk terjual per pesanan per waktu pesanan.
--
-- Konsekuensi grain itu, dan inilah yang dinilai:
--   * Kunci dimensi diambil dari versi yang BERLAKU SAAT pesanan terjadi, bukan versi hari ini.
--     Untuk dim_product artinya syarat tanggal ikut di ON (lihat 20_dim_product.sql).
--   * `order_id` dan `item_id` tidak punya dimensi sendiri. Keduanya tetap ditulis di fact dan
--     diberi label degenerate. `item_id` bukan hiasan: `return_rate` di Sesi 13 menyambung
--     `returns.csv` ke fact lewat kolom itu — retur menunjuk item, bukan pesanan.
--   * Measure diberi label aditivitas di komentar: qty, diskon, neto = ADDITIVE;
--     harga_satuan = NON-ADDITIVE.
--
-- Dua hal yang paling sering salah di sini:
--   1. Join harga ke versi hari ini → omzet historis berubah (leakage).
--   2. Masuknya item tanpa order induk → hilangnya omzet tanpa pesan error.
--      Di berkas ini keduanya sudah dijaga: stg_order_items sudah bersih dan dim_product
--      di-join dengan syarat tanggal.
--
-- TODO: tulis DDL fact_order_line lengkap, lalu HAPUS kata TODO ini supaya loader boleh jalan.
SELECT
    1 AS date_sk, 1 AS channel_sk, 1 AS store_sk, 1 AS product_sk, 1 AS customer_sk,
    '' AS order_id, 0 AS qty, 0 AS harga_satuan, 0 AS diskon, 0 AS neto,
    '' AS status, now() AS order_ts
WHERE FALSE;

-- Bukti yang harus hijau di Cek 1c (dua-duanya harus nol):
--   SELECT (SELECT sum(neto) FROM fact_order_line) - (SELECT sum(neto) FROM stg_order_items);
--   SELECT count(*) FROM fact_order_line WHERE date_sk IS NULL OR customer_sk IS NULL;
