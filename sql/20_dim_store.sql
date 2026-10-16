-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE dim_store AS
SELECT CAST(ROW_NUMBER() OVER (ORDER BY store_id) AS INTEGER) AS store_sk,
       store_id, nama, kota, wilayah, tipe,
       (upper(aktif) = 'YA') AS aktif
FROM read_csv_auto('{D}/stores.csv', all_varchar=true)
UNION ALL SELECT -1, 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI',
       'TIDAK DIKETAHUI', FALSE;
