# Sumber Data — T3 Kemiskinan (Track B: K1, K2, K3, K6)

> Baca ini sebelum menulis satu baris SQL. Di Sesi 13 kamu akan diminta menjelaskan
> **dari mana angka ini datang dan apa yang belum diverifikasi** — jawabannya ada di sini.

## Berkas

| Berkas | Indikator | Satuan | Cakupan tahun | Baris |
|---|---|---|---|---|
| `jumlah_penduduk_miskin_kabupaten_kota_2004-2024.csv` | Jumlah penduduk miskin | ribu jiwa | 2004–2024 | 581 |
| `persentase_penduduk_miskin_p0_kabupaten_kota_2004-2024.csv` | Persentase penduduk miskin (P0) | persen | 2004–2024 | 581 |
| `garis_kemiskinan_kabupaten_kota_2016-2023.csv` | Garis kemiskinan | Rp/kapita/bulan | **2016–2023** | 580 |

**Perhatikan:** cakupan tahun berkas ketiga **berbeda**. Ini bukan kesalahan unduh. Keputusan
apa yang kamu lakukan terhadap tahun yang tidak lengkap adalah bagian dari nilai D3 dan D4.

## Asal-usul — baca dengan jujur

- **Produsen data:** Badan Pusat Statistik (BPS), berdasarkan Survei Sosial Ekonomi Nasional
  (Susenas). Tabel: *Jumlah/Persentase Penduduk Miskin Menurut Kabupaten/Kota* dan
  *Garis Kemiskinan Menurut Kabupaten/Kota*.
- **Cara diperoleh:** portal BPS menyajikan tabel secara interaktif dan tidak memberi tautan
  unduh CSV langsung yang stabil. Berkas ini karenanya diambil dari **salinan pihak ketiga** di
  GitHub (`frzxw/EDA-data-mining-6`, cabang `main`, folder `dataset/kemiskinan`) pada
  **2026-09-11**.
- **Status verifikasi:** ⚠️ **angka belum dicocokkan baris-per-baris dengan BPS.** Struktur
  berkas konsisten dengan ekspor asli BPS (ada BOM, header dua baris, baris catatan kaki
  ber-HTML, tanda `-` untuk data kosong), tetapi itu bukti bentuk, bukan bukti isi.
- **Checksum SHA-256** (supaya bisa dibuktikan berkas tidak berubah sejak diunduh):

```
009f8710…5bffd5d32  jumlah_penduduk_miskin_kabupaten_kota_2004-2024.csv
4a44c457…86b5919ff4  persentase_penduduk_miskin_p0_kabupaten_kota_2004-2024.csv
a9dd7eb9…85e237a50a  garis_kemiskinan_kabupaten_kota_2016-2023.csv
```

- **Lisensi:** statistik resmi BPS umumnya boleh dipakai ulang dengan menyebut sumber.
  Salinan pihak ketiga tidak mengubah kewajiban itu — **sebut BPS, bukan GitHub**, saat kamu
  mengutip angka.

### Apa artinya untuk pekerjaanmu

Di dashboard dan memo, sumber ditulis: **"BPS, Susenas — via salinan pihak ketiga,
snapshot 11 Sep 2026, belum diverifikasi"**. Menulis "Sumber: BPS" tanpa kualifikasi itu
**salah** — kamu belum pernah membuka bps.go.id. Kejujuran soal ini persis yang dinilai
D12 (lineage) dan butir 5 (pembelaan).

## Kotoran yang sudah diketahui — jangan "dibersihkan" diam-diam

Semua ini **sengaja dibiarkan**. Menemukannya adalah pekerjaan Sesi 2 dan Sesi 5.

1. **Header dua baris.** Baris 1 judul tabel, baris 2 daftar tahun. Baris 1 bukan nama kolom.
2. **BOM UTF-8** di awal berkas — `Nama Wilayah` bisa terbaca `﻿Nama Wilayah`.
3. **Format lebar (wide).** Tahun jadi kolom, bukan baris. Butuh unpivot sebelum masuk fact.
4. **Hierarki wilayah tidak punya kolom sendiri.** Provinsi ditulis **HURUF BESAR**
   (`JAWA BARAT`), kabupaten/kota dengan huruf biasa (`Simeulue`). 38 provinsi dan 540
   kabupaten/kota bercampur dalam satu kolom. `dim_wilayah` harus kamu turunkan dari konvensi
   ini — dan konvensi bukan kontrak.
5. **`-` sebagai penanda kosong**, bukan `NULL` atau string kosong. Ada 1.240 kemunculan.
6. **Baris kosong** menjelang akhir berkas.
7. **Baris `Catatan`** berisi teks HTML (`<br />`) — catatan kaki BPS soal Kabupaten Nduga
   yang angka 2015-nya memakai angka 2014. Ini bukan data; ini peringatan metodologis yang
   harus masuk ke lampiran tata kelolamu.
8. **Pemekaran wilayah.** Sebagian kabupaten baru muncul di tahun akhir saja (contoh:
   Pegunungan Bintang hanya punya angka 2024). Inilah alasan `dim_wilayah` perlu SCD Type 2.

## Slice per kelompok

Ambil hanya provinsimu. Skema sama, angka berbeda — jadi kamu boleh saling bantu teknis,
tetapi temuan dan rekomendasimu tidak bisa disalin.

| Kelompok | Provinsi |
|---|---|
| K1 | JAWA BARAT |
| K2 | JAWA TENGAH |
| K3 | SULAWESI SELATAN |
| K6 | NUSA TENGGARA TIMUR |
