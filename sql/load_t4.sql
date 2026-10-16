-- KEADAAN SELESAI (tag aman) — urutan load langkah 1.
-- Hanya memuat berkas yang sudah selesai pada langkah ini.
-- Jalankan: python -m pipeline.load --topic t4 --twice

SOURCE sql/00_stg_returns.sql;
SOURCE sql/20_dim_channel.sql;
SOURCE sql/20_dim_product.sql;
SOURCE sql/10_dim_date.sql;
SOURCE sql/00_stg_orders.sql;
SOURCE sql/00_stg_order_items.sql;
SOURCE sql/20_dim_store.sql;
SOURCE sql/20_dim_customer.sql;
SOURCE sql/30_fact_order_line.sql;
