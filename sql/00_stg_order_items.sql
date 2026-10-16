-- ============================================================
-- 00_stg_order_items.sql — Sesi 12, langkah 1b (Bersihkan)
--
-- Dua keputusan di berkas ini milikmu, dan keduanya harus punya alasan satu baris.
-- Hasilnya: `stg_order_items` bersih + `quarantine_items` untuk yang sengaja disisihkan.
--
-- Aturan besinya: measure `neto` di sini adalah omzet yang nanti dibandingkan dengan fact.
-- Kalau satu baris saja berbeda, Cek 1c tidak akan hijau — dan itu memang tujuannya.
-- ============================================================

-- Langkah A — sisihkan item yang tidak punya order induk.
-- Ada baris item yang menunjuk order_id yang tidak ada di stg_orders. Kalau ikut masuk fact,
-- join ke stg_orders menggagalkan baris itu tanpa pesan error — omzetnya hilang diam-diam.
CREATE OR REPLACE TABLE quarantine_items AS
SELECT
    i.item_id,
    i.order_id,
    i.product_id,
    TRY_CAST(i.qty AS INTEGER)      AS qty,
    TRY_CAST(i.harga_satuan AS BIGINT) AS harga_satuan,
    TRY_CAST(i.diskon AS BIGINT)    AS diskon,
    'tanpa order induk'             AS alasan
FROM read_csv_auto('{D}/order_items.csv', all_varchar=true) i
WHERE NOT EXISTS (SELECT 1 FROM stg_orders o WHERE o.order_id = i.order_id);

-- Langkah B — keputusanmu: qty negatif.
-- Retur resmi sudah punya berkasnya sendiri (`returns.csv`), jadi qty negatif di sini bukan retur.
-- Pilih satu: buang (masuk karantina), atau pertahankan (measure boleh negatif). Apa pun pilihanmu,
-- tulis alasannya satu baris di bawah.
--
-- TODO: putuskan qty negatif dan tulis alasannya, lalu HAPUS kata TODO ini.
--       Alasan: ______________________________________________________________
INSERT INTO quarantine_items
SELECT
    i.item_id, i.order_id, i.product_id,
    TRY_CAST(i.qty AS INTEGER), TRY_CAST(i.harga_satuan AS BIGINT), TRY_CAST(i.diskon AS BIGINT),
    'qty negatif'
FROM read_csv_auto('{D}/order_items.csv', all_varchar=true) i
WHERE TRY_CAST(i.qty AS INTEGER) < 0;

-- Langkah C — item bersih, satu baris per item_id.
-- Dua syarat: punya order induk, dan tidak kamu sisihkan di Langkah B.
-- Kalau keputusanmu di Langkah B adalah "pertahankan qty negatif", hapus blok INSERT Langkah B —
-- maka baris-baris itu otomatis ikut ke sini, dan tidak perlu diubah lagi.
CREATE OR REPLACE TABLE stg_order_items AS
SELECT
    i.item_id,
    i.order_id,
    i.product_id,
    TRY_CAST(i.qty AS INTEGER)         AS qty,           -- ADDITIVE
    TRY_CAST(i.harga_satuan AS BIGINT) AS harga_satuan,  -- NON-ADDITIVE (harga: pakai min/max/avg)
    TRY_CAST(i.diskon AS BIGINT)       AS diskon,        -- ADDITIVE
    TRY_CAST(i.qty AS INTEGER) * TRY_CAST(i.harga_satuan AS BIGINT)
        - TRY_CAST(i.diskon AS BIGINT) AS neto           -- ADDITIVE
FROM read_csv_auto('{D}/order_items.csv', all_varchar=true) i
WHERE EXISTS (SELECT 1 FROM stg_orders o WHERE o.order_id = i.order_id)
  AND i.item_id NOT IN (SELECT item_id FROM quarantine_items WHERE item_id IS NOT NULL);

-- Bukti yang harus hijau di Cek 1b:
--   SELECT count(*) FROM quarantine_items;                          -- > 0, dan kamu tahu kenapa
--   SELECT count(*) - count(DISTINCT item_id) FROM stg_order_items; -- harus 0
