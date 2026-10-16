-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE fact_target AS
SELECT bulan,
       channel,
       wilayah,
       CASE WHEN trim(target_revenue) = '' THEN NULL
            ELSE TRY_CAST(target_revenue AS BIGINT) END AS target_revenue,
       1 AS target_sk
FROM read_csv_auto('{D}/targets.csv', all_varchar=true);
