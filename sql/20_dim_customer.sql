-- ============================================================
-- 20_dim_customer.sql — Sesi 12, langkah 1c. Bagianmu.
--
-- Grain: satu baris = satu orang (satu customer_id), BUKAN satu identitas.
--
-- Masalahnya nyata dan ini inti langkah ini: orang yang sama datang dengan identitas berbeda
-- menurut channel-nya.
--     STORE        → loyalty_id   (LYL…)
--     WEB / APP    → email
--     MARKETPLACE  → handle       (@…)
-- Dan ada 20 email yang dipakai oleh DUA customer_id (lihat temuan 1a soal identitas), serta
-- 30 pelanggan yang tidak punya handle sama sekali.
--
-- Jebakannya ada di sini, dan ini penyebab "omzet fact ≠ omzet staging" yang paling sering
-- tertukar dengan masalah harga:
--   Kalau fact join dengan OR (loyalty_id ATAU email ATAU handle), email yang dipakai dua
--   customer_id membuat satu baris fact BERANAK DUA. Jumlah baris fact jadi lebih besar dari
--   stg_order_items, dan omzetnya ikut menggelembung.
--
-- Jalan yang aman, dan yang dipakai contoh dosen: bikin tabel jembatan `bridge_customer_ref`
-- yang isinya SATU baris per customer_ref (pilih customer_sk terkecil supaya deterministik).
-- Fact join ke jembatan itu, bukan langsung ke dim_customer.
--
-- TODO: tulis `dim_customer` dan `bridge_customer_ref` di bawah, tulis alasanmu,
--       lalu HAPUS kata TODO ini supaya loader boleh jalan.
--       Kolom wajib: customer_sk, customer_id, loyalty_id, email, telepon, handle, kota, wilayah.
--       PII: email dan telepon JANGAN disimpan mentah — mask atau potong (D12 menilai ini).
--       Alasan: ______________________________________________________________

-- Kerangka jembatan (sudah benar bentuknya; sesuaikan nama kolom dengan dim_customer-mu):
CREATE OR REPLACE TABLE bridge_customer_ref AS
WITH kandidat AS (
    SELECT loyalty_id AS customer_ref, customer_sk FROM dim_customer WHERE loyalty_id <> ''
    UNION ALL
    SELECT email,      customer_sk FROM dim_customer WHERE email <> ''
    UNION ALL
    SELECT handle,     customer_sk FROM dim_customer WHERE handle <> ''
)
SELECT customer_ref, MIN(customer_sk) AS customer_sk
FROM kandidat
GROUP BY customer_ref;

-- Bukti yang harus hijau di Cek 1c:
--   SELECT count(*) - count(DISTINCT customer_ref) FROM bridge_customer_ref;   -- harus 0
