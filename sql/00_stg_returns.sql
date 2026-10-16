-- ============================================================
-- 00_stg_returns.sql — Sesi 12, langkah 1b. DIBERIKAN.
--
-- Retur punya berkasnya sendiri karena retur bukan baris penjualan negatif: ia punya waktu
-- sendiri, alasan sendiri, dan channel sendiri. Beli di WEB, kembalikan di toko, itu biasa.
-- Karena itu retur TIDAK dikurangkan dari neto di fact — ia dipakai untuk `return_rate`.
-- ============================================================

CREATE OR REPLACE TABLE stg_returns AS
SELECT
    return_id,
    item_id,
    TRY_STRPTIME(return_ts, '%Y-%m-%d %H:%M:%S') AS return_ts,
    reason                                       AS alasan,
    return_channel                               AS channel_retur
FROM read_csv_auto('{D}/returns.csv', all_varchar=true);

-- Catatan untuk langkah 1d dan Sesi 13: satu kategori di satu channel punya retur yang jauh
-- lebih padat daripada yang lain. Itu bahan analisis faktor, bukan kesalahan data.
