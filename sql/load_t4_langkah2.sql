-- KEADAAN SELESAI (tag aman) — urutan load langkah 2 (Sesi 13).
-- Jalankan: python -m pipeline.load --topic t4 --twice --sql sql/load_t4_langkah2.sql

SOURCE sql/load_t4.sql;
SOURCE sql/20_dim_target.sql;
SOURCE sql/21_fact_target.sql;
