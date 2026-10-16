# sql/

T1–T3 (Sesi 2–7):

| Berkas | Pemilik | Sesi |
|---|---|---|
| `00_profiling.sql` | dosen | 2 — profiling data mentah |
| `10_dim_date.sql` | dosen | diberikan lengkap, bukan checkpoint |
| `20_dim_<entitas>.sql` | **kamu** | 3 (DDL) → 4 (load) |
| `30_fact_<x>.sql` | **kamu** | 3 (DDL) → 4 (load) |
| `40_analytics/q01..q08.sql` | **kamu** | 6 |
| `50_metrics/<metrik>.sql` | **kamu** | 7 — satu berkas per metrik di kamus |

T4 (Sesi 12–15). Satu proyek, empat langkah, tiga berkas urutan load:

| Berkas | Pemilik | Langkah |
|---|---|---|
| `00_stg_returns.sql` | dosen | 1b — retur punya berkasnya sendiri |
| `00_stg_orders.sql` | dosen + **kamu** | 1b — aturan waktu & status diberikan; dedup `order_id` bagianmu |
| `00_stg_order_items.sql` | **kamu** | 1b — item yatim dan qty negatif |
| `20_dim_channel.sql` | dosen | 1c — 4 channel + Unknown |
| `20_dim_product.sql` | dosen | 1c — SCD Type 2 lewat `harga_berlaku_dari` |
| `20_dim_store.sql` | **kamu** | 1c — gerai yang sudah tutup tetap masuk |
| `20_dim_customer.sql` | **kamu** | 1c — satu orang lintas channel + jembatan identitas |
| `30_fact_order_line.sql` | **kamu** | 1c — surrogate key pada versi yang berlaku saat pesanan terjadi |
| `40_analytics/trend_per_channel.sql` | dosen | 1d — pertanyaan pertama yang bisa dijawab |
| `40_analytics/pred_anomaly_daily.sql` | **kamu** | 1d — z-score 28 hari, jendela tidak memuat hari yang dinilai |
| `20_dim_target.sql`, `21_fact_target.sql` | **kamu** | 2a — target jadi tabelnya sendiri |
| `30_v_kpi_monthly.sql` | **kamu** | 2b — attainment; target kosong → capaian kosong |
| `31_v_revenue_bridge.sql` | **kamu** | 3b — volume, harga, mix |
| `load_t4.sql` | dosen | urutan eksekusi langkah 1 |
| `load_t4_langkah2.sql`, `load_t4_langkah3.sql` | dosen | urutan untuk malam Sesi 13 dan 14 |

`load_t4*.sql` boleh memuat baris `SOURCE sql/berkas.sql;` — loader membacanya dan menyisipkan isi
berkasnya (Python DuckDB tidak bisa menjalankan `SOURCE` sendiri). Satu penanda `TODO` di berkas
mana pun yang ikut terbaca menahan seluruh load: itu memang gerbangnya, bukan gangguan.
