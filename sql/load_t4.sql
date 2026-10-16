-- ============================================================
-- sql/load_t4.sql — URUTAN EKSEKUSI T4 (Sesi 12 → 15)
--
-- Jalankan:  python -m pipeline.load --topic t4 --twice
--
-- Aturan urutan: staging dulu, lalu dimensi, fact terakhir, prediksi paling akhir.
--   stg_*          harus ada sebelum dim_customer (jembatan identitas) dan fact
--   dim_product    harus ada sebelum fact (syarat tanggal SCD2)
--   pred_anomaly_daily  membaca fact, jadi ia paling akhir
--
-- Loader membaca baris SOURCE di berkas ini dan menyisipkan isi berkasnya (DuckDB Python tidak
-- bisa menjalankan SOURCE sendiri). Kalau ada satu penanda pekerjaan-belum-selesai di berkas mana pun di bawah ini,
-- loader menolak jalan — itu memang tujuannya.
-- ============================================================

SOURCE sql/00_stg_returns.sql;      -- DIBERIKAN
SOURCE sql/00_stg_orders.sql;       -- aturan waktu + status diberikan; dedup bagianmu
SOURCE sql/00_stg_order_items.sql;  -- bagianmu (yatim + qty negatif)

SOURCE sql/10_dim_date.sql;         -- DIBERIKAN
SOURCE sql/20_dim_channel.sql;      -- DIBERIKAN
SOURCE sql/20_dim_product.sql;      -- DIBERIKAN (SCD Type 2)
SOURCE sql/20_dim_store.sql;        -- bagianmu
SOURCE sql/20_dim_customer.sql;     -- bagianmu (resolusi identitas lintas channel)

SOURCE sql/30_fact_order_line.sql;  -- bagianmu

SOURCE sql/40_analytics/pred_anomaly_daily.sql;   -- bagianmu (langkah 1d)
