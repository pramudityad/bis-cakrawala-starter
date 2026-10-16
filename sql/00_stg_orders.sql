-- ============================================================
-- 00_stg_orders.sql — Sesi 12, langkah 1b (Bersihkan)
--
-- Dua aturan sudah ditulis untukmu (waktu dan status). Satu bagian masih pekerjaanmu.
-- Aturan repo ini: setiap aturan pembersihan membawa SATU BARIS ALASAN. Aturan tanpa alasan
-- adalah aturan yang belum kamu mengerti, dan akan ditanya di pembelaan (RPS butir 5).
-- ============================================================

-- ATURAN 1 (sudah ditulis) — semua waktu disimpan dalam WIB.
-- Alasan: sebagian baris datang bertanda UTC (`…Z`). Kalau dibiarkan, satu hari bergeser 7 jam,
-- total harian ikut bergeser, dan penanda anomali di langkah 1d menilai hari yang salah.
CREATE OR REPLACE TABLE stg_orders AS
WITH sumber AS (
    SELECT
        order_id,
        channel,
        store_id,
        customer_ref,
        CASE
            WHEN order_ts LIKE '%Z' THEN TRY_STRPTIME(order_ts, '%Y-%m-%dT%H:%M:%SZ') + INTERVAL 7 HOUR
            ELSE TRY_STRPTIME(order_ts, '%Y-%m-%d %H:%M:%S')
        END AS order_ts_wib,
        status,
        fulfillment,
        payment_method
    FROM read_csv_auto('{D}/orders.csv', all_varchar=true)
),

-- ATURAN 2 (sudah ditulis) — lima ejaan untuk satu ide dipetakan ke satu daftar bersih.
-- Alasan: satu ide yang ditulis lima cara membuat KPI per status pecah dan angka gabungan menipu.
bersih AS (
    SELECT
        *,
        CASE upper(trim(status))
            WHEN 'DELIVERED' THEN 'DELIVERED'
            WHEN 'DELIVRD'   THEN 'DELIVERED'
            WHEN 'SELESAI'   THEN 'DELIVERED'
            WHEN 'CANCELLED' THEN 'CANCELLED'
            WHEN 'SHIPPED'   THEN 'SHIPPED'
            WHEN 'PENDING'   THEN 'PENDING'
            ELSE 'TIDAK DIKETAHUI'
        END AS status_clean
    FROM sumber
)

-- ATURAN 3 — bagianmu. Duplikasi order_id.
-- Ada baris yang tersalin apa adanya, dan satu toko mengirim batch POS-nya DUA KALI. Lihat
-- temuan 1a: baris dengan "kelebihan" terbesar adalah satu toko pada satu tanggal.
-- Kalau dibiarkan, omzet channel itu dihitung dua kali.
--
-- TODO: sisakan SATU baris per order_id (pakai ROW_NUMBER() … ORDER BY order_ts_wib, ambil = 1).
--       Tulis alasannya satu baris di bawah, lalu HAPUS kata TODO ini supaya loader boleh jalan.
--       Alasan: ______________________________________________________________
SELECT *
FROM bersih;

-- Bukti yang harus hijau di Cek 1b — jalankan sendiri sebelum mengangkat tangan:
--   SELECT count(*) - count(DISTINCT order_id) AS kelebihan FROM stg_orders;   -- harus 0
--   SELECT count(*) FILTER (WHERE order_ts_wib IS NULL) FROM stg_orders;       -- harus 0
