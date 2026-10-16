-- ============================================================
-- sql/load_t4_langkah3.sql — URUTAN EKSEKUSI T4, Sesi 14 (langkah 3)
--
-- Jalankan MALAM SESI 14:
--   python -m pipeline.load --topic t4 --twice --sql sql/load_t4_langkah3.sql
--
-- Isinya = seluruh langkah 1 dan 2 (lewat include bersarang), ditambah jembatan omzet.
-- ============================================================

SOURCE sql/load_t4_langkah2.sql;         -- langkah 1 (Sesi 12) + langkah 2 (Sesi 13)

SOURCE sql/31_v_revenue_bridge.sql;      -- bagianmu: volume, harga, mix
