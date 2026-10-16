-- ============================================================
-- 20_dim_product.sql — Sesi 12, langkah 1c. DIBERIKAN (2 dari 5 dimensi).
--
-- Ini satu-satunya dimensi Type 2 di proyek ini, dan alasannya nyata: sebagian produk menaikkan
-- harga pada 1 Juli 2025. `products.csv` sudah memuat DUA baris untuk produk seperti itu — satu
-- per `harga_berlaku_dari`. Tugasmu bukan menebak harganya: tugasmu menyimpan DUA versinya.
--
-- Kalau dimensi ini dibuat Type 1 (satu baris per produk, harga hari ini), maka baris fact bulan
-- Januari akan ikut memakai harga Juli. Omzet historis berubah sendiri, dan jawaban proyek salah.
-- Nama teknisnya leakage: barisnya tahu masa depan yang seharusnya belum ia ketahui.
--
-- Grain: satu baris = satu versi harga satu produk.
-- ============================================================

CREATE OR REPLACE TABLE dim_product AS
WITH versi AS (
    SELECT
        product_id,
        nama,
        kategori,
        TRY_CAST(harga_satuan AS BIGINT)      AS harga_satuan,
        TRY_CAST(harga_berlaku_dari AS DATE)  AS valid_from
    FROM read_csv_auto('{D}/products.csv', all_varchar=true)
),
rentang AS (
    SELECT
        *,
        -- versi ini berlaku sampai sehari sebelum versi berikutnya; versi terakhir berlaku selamanya
        COALESCE(LEAD(valid_from) OVER (PARTITION BY product_id ORDER BY valid_from) - 1,
                 DATE '9999-12-31')           AS valid_to
    FROM versi
)
SELECT
    CAST(ROW_NUMBER() OVER (ORDER BY product_id, valid_from) AS INTEGER) AS product_sk,  -- surrogate key
    product_id,                                                                          -- kunci bisnis
    nama,
    kategori,
    harga_satuan,
    valid_from,
    valid_to,
    (valid_to = DATE '9999-12-31') AS is_current
FROM rentang
UNION ALL
SELECT -1, 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI', NULL,
       DATE '1900-01-01', DATE '9999-12-31', TRUE;

-- Cara join yang benar nanti di fact — perhatikan syarat tanggalnya:
--   LEFT JOIN dim_product p
--          ON p.product_id = i.product_id
--         AND CAST(o.order_ts_wib AS DATE) BETWEEN p.valid_from AND p.valid_to
