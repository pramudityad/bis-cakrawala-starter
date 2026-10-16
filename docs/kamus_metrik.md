# D6 — Kamus metrik (12 field + definisi capaian)

Tiga KPI proyek T4, satu primary dan dua supporting. Kolom 11 disamakan dengan
perilaku `v_kpi_monthly` supaya dua analis menghitung angka yang sama.

## Metrik 1 — Net Revenue

| # | Field | Isi |
|---|---|---|
| 1 | Nama metrik | Net Revenue |
| 2 | Definisi (satu kalimat, tanpa jargon) | Omzet bersih: jumlah nilai baris pesanan setelah diskon, tanpa retur. |
| 3 | Rumus (SQL-nya, bukan bahasa manusia) | `SUM(fact_order_line.neto)` |
| 4 | Grain | bulan × channel × wilayah |
| 5 | Tabel sumber | `fact_order_line` |
| 6 | Owner (jabatan bernama) | Retail Planning Lead |
| 7 | Time basis | per hari kalender WIB, dilaporkan per bulan |
| 8 | Satuan | rupiah |
| 9 | Dimensi yang boleh dipotong | bulan, channel, wilayah, kategori produk |
| 10 | Filter default | tidak ada — semua baris pesanan yang sah ikut |
| 11 | Arti nilai kosong | bulan tanpa pesanan = 0; bulan tanpa target = NULL |
| 12 | Versi | v1, 2025-10-16 |
| 13 | **Definisi capaian vs target** | net_revenue ÷ target_revenue; target kosong memberi capaian kosong |
| 14 | Peran di proyek | primary — satu-satunya KPI yang punya pembanding target, dan pertanyaan proyeknya soal target meleset |

## Metrik 2 — Orders per Channel

| # | Field | Isi |
|---|---|---|
| 1 | Nama metrik | Orders per Channel |
| 2 | Definisi (satu kalimat, tanpa jargon) | Jumlah pesanan berbeda per channel pada satu bulan. |
| 3 | Rumus (SQL-nya, bukan bahasa manusia) | `COUNT(DISTINCT fact_order_line.order_id_degenerate)` |
| 4 | Grain | bulan × channel × wilayah |
| 5 | Tabel sumber | `fact_order_line` |
| 6 | Owner (jabatan bernama) | Retail Planning Lead |
| 7 | Time basis | per hari kalender WIB, dilaporkan per bulan |
| 8 | Satuan | pesanan |
| 9 | Dimensi yang boleh dipotong | bulan, channel, wilayah |
| 10 | Filter default | tidak ada |
| 11 | Arti nilai kosong | bulan tanpa pesanan = 0 |
| 12 | Versi | v1, 2025-10-16 |
| 13 | **Definisi capaian vs target** | tidak punya tabel target; KPI ini menjelaskan kenapa omzet berubah |
| 14 | Peran di proyek | supporting — menjelaskan sisi volume dari selisih omzet |

## Metrik 3 — Return Rate

| # | Field | Isi |
|---|---|---|
| 1 | Nama metrik | Return Rate |
| 2 | Definisi (satu kalimat, tanpa jargon) | Bagian pesanan yang punya retur pada bulan itu. |
| 3 | Rumus (SQL-nya, bukan bahasa manusia) | `COUNT(DISTINCT returns.return_id) ÷ COUNT(DISTINCT fact_order_line.order_id_degenerate)` |
| 4 | Grain | bulan × channel × wilayah |
| 5 | Tabel sumber | `stg_returns + fact_order_line` |
| 6 | Owner (jabatan bernama) | Customer Experience Lead |
| 7 | Time basis | per hari kalender WIB, dilaporkan per bulan |
| 8 | Satuan | rasio (0–1) |
| 9 | Dimensi yang boleh dipotong | bulan, channel, wilayah, alasan retur |
| 10 | Filter default | semua retur, bukan hanya yang kembali ke channel pembeliannya |
| 11 | Arti nilai kosong | bulan tanpa pesanan = 0; bulan tanpa retur = 0 |
| 12 | Versi | v1, 2025-10-16 |
| 13 | **Definisi capaian vs target** | tidak punya tabel target; KPI ini menjelaskan sisi kualitas dari selisih omzet |
| 14 | Peran di proyek | supporting — menjelaskan kenapa omzet terkikis walau pesanan naik |

## Catatan versi

Ketiganya v1 sejak 2025-10-16. Yang berubah bersama: definisi capaian dan arti nilai
kosong — kalau view berubah, dua baris itu yang lebih dulu harus disamakan.
