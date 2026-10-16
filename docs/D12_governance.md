# D12 — Lampiran tata kelola (9 bagian)

Sembilan bagian, ditulis untuk warehouse T4 dan dashboard di atasnya.

1. **Pemilik data.** Isi dan kualitas dataset ini milik Retail Planning Lead; yang menjaga definisi
   metrik adalah Data Steward, dan yang menjalankan sistemnya Data Engineer (custodian). Head of
   Omnichannel Retail hanya membaca angkanya — ia pemakai, bukan pemilik.

2. **Klasifikasi PII.** `customers.email`, `customers.telepon`, `customers.handle`, dan
   `orders.customer_ref` adalah data pribadi menurut UU PDP No. 27/2022: semuanya bisa menunjuk satu
   orang. `customer_id` dan `loyalty_id` adalah kunci pseudonim — bukan PII selama pemetaannya
   disimpan terpisah. Kolom yang tidak menyentuh orang: `products`, `stores`, `targets`.

3. **Hak akses.** Akses diberikan per peran, bukan per orang, dan seluas yang dibutuhkan pekerjaan
   (least privilege). Analis wilayah hanya melihat wilayahnya — aturan row-level pada kolom
   `wilayah` di `v_kpi_monthly`. Nomor telepon penuh hanya untuk peran Customer Experience; peran
   lain melihat bentuk tersamar (`0812****789`).

4. **Lineage.** Satu metrik dari hulu ke hilir: `targets.csv` kolom `target_revenue` →
   `fact_target.target_revenue` → `v_kpi_monthly.target_revenue` → tile "target vs aktual". Sisi
   aktualnya: `orders.csv` → `stg_orders` → `fact_order_line.neto` → `v_kpi_monthly.net_revenue`.
   Kolomnya disebut, bukan hanya tabelnya.

5. **Retensi.** Data transaksi disimpan 5 tahun; data pribadi pelanggan 2 tahun sejak transaksi
   terakhir. Permintaan penghapusan **tidak** dijalankan dengan `DELETE`: `dim_customer` menyimpan
   setiap versi (Type 2), jadi DELETE hari ini tidak menghapus versi kemarin. Yang dijalankan:
   hitung ulang kunci pseudonim pelanggan itu, ganti nilai PII-nya di semua versi, lalu cabut
   pemetaannya. Bukti penghapusan disimpan tanpa PII.

6. **Penghentian.** Kalau warehouse ini dimatikan, tabel fakta dan dimensi disimpan sebagai arsip
   read-only selama 5 tahun; yang dihapus lebih dulu adalah kolom PII. Yang diberi tahu: Retail
   Planning Lead (pemilik data), Data Steward (pemilik definisi), dan Head of Omnichannel Retail
   sebagai pemakai dashboard. Workbook Metabase-nya diarsipkan bersama definisi metriknya.

7. **Pemilik target.** Target omzet ditetapkan **Retail Planning Lead**, berlaku per bulan kalender,
   dan hanya jabatan itu yang boleh merevisinya — dengan catatan tanggal revisi. Periode berlakunya
   tercatat di `dim_target` (`valid_from`, `valid_to`). Angka target tanpa jabatan pemilik tidak
   dipakai di dashboard.

8. **Identitas lintas channel.** Yang di-ingest ke lapisan BI: `customer_id`, `loyalty_id`, `handle`,
   `email`, `kota`, `wilayah`. Yang **tidak di-ingest**: `telepon` — tidak satu pun tile di dashboard
   membutuhkannya, jadi lebih baik tidak pernah masuk. Penyatuan identitas lewat
   `bridge_customer_ref` (satu baris per `customer_ref`, dipilih deterministik), bukan lewat join OR
   ke `dim_customer` — itu membuat baris fact beranak dua. Tampilan memakai `email_tersamar`, kunci
   join memakai `email`.

9. **Matriks akses.**

   | Peran | channel | wilayah | Akses |
   |---|---|---|---|
   | Retail Planning Lead | STORE, WEB, APP, MARKETPLACE | semua | baca + tulis target |
   | Analis wilayah | semua | satu wilayah saja | baca |
   | Customer Experience Lead | semua | semua | baca, termasuk kolom telepon penuh |
   | Data Steward | semua | semua | baca definisi metrik, tidak melihat PII |
   | Auditor internal | semua | semua | baca, hanya lewat `email_tersamar` |

## Khusus data publik (tim T3)

Tidak berlaku — dataset T4 sintetis buatan dosen, bukan data publik dan bukan data prodi.
