-- KEADAAN SELESAI (tag aman). Diambil dari reference-sql dosen.
-- Dipakai kalau kamu harus menarik tag langkah ini: `git checkout <tag>`.
-- Setelah menariknya, tetap tulis satu baris apa yang kamu lewati.

CREATE OR REPLACE TABLE dim_target AS
SELECT * FROM (VALUES
    (1, 'Target omzet bersih bulanan per channel per wilayah', 'Retail Planning Lead',
     DATE '2025-01-01', DATE '9999-12-31', 'Retail Planning Lead')
) AS t(target_sk, definisi, pemilik_jabatan, valid_from, valid_to, boleh_revisi_oleh)
UNION ALL SELECT -1, 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI', DATE '1900-01-01', DATE '9999-12-31', 'TIDAK DIKETAHUI';
