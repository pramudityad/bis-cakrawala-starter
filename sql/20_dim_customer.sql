-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE dim_customer AS
SELECT CAST(ROW_NUMBER() OVER (ORDER BY customer_id) AS INTEGER) AS customer_sk,
       customer_id, loyalty_id, email,
       regexp_replace(email, '^(.).*?(@.*)$', '\1***\2') AS email_tersamar,
       CASE WHEN telepon IS NULL OR telepon = '' THEN NULL
            ELSE regexp_replace(telepon, '(\d{2})\d+(\d{2})', '\1****\2') END AS telepon_tersamar,
       handle, kota, wilayah
FROM read_csv_auto('{D}/customers.csv', all_varchar=true)
UNION ALL SELECT -1, 'TIDAK DIKETAHUI', '', '', '', NULL, '', 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI';

CREATE OR REPLACE TABLE bridge_customer_ref AS
WITH kandidat AS (
    SELECT loyalty_id AS customer_ref, customer_sk FROM dim_customer WHERE loyalty_id <> ''
    UNION ALL SELECT email,  customer_sk FROM dim_customer WHERE email <> ''
    UNION ALL SELECT handle, customer_sk FROM dim_customer WHERE handle <> ''
)
SELECT customer_ref, MIN(customer_sk) AS customer_sk FROM kandidat GROUP BY customer_ref;
