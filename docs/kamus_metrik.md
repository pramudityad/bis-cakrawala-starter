# D6 — Kamus metrik (12 field + definisi capaian)

> UTS item 5 menilai **satu** metrik lengkap; UAS menilai tiga. Setiap metrik wajib punya berkas SQL
> di `sql/50_metrics/` — definisi yang tidak bisa dijalankan belum tentu benar.
>
> Untuk T4 (Sesi 13), tiga metriknya sudah ditetapkan: **Net Revenue**, **Orders per Channel**, dan
> **Return Rate**. Satu di antaranya kamu tandai **primary** — yang paling langsung menjawab
> pertanyaan proyek — dan dua lainnya **supporting**. Pertanyaan proyeknya soal target yang meleset,
> jadi pikirkan metrik mana yang punya pembanding target.
>
> Kolom 6 wajib jabatan bernama. Kolom 11 wajib sama persis dengan perilaku view-mu, supaya dua
> analis menghitung angka yang sama. Baris terakhir (Definisi capaian vs target) wajib untuk ketiganya.

## Metrik 1 — ______________________

| # | Field | Isi |
|---|---|---|
| 1 | Nama metrik |  |
| 2 | Definisi (satu kalimat, tanpa jargon) |  |
| 3 | Rumus (SQL-nya, bukan bahasa manusia) |  |
| 4 | Grain |  |
| 5 | Tabel sumber |  |
| 6 | Owner (jabatan bernama) |  |
| 7 | Time basis | per hari kalender WIB / per bulan / … |
| 8 | Satuan |  |
| 9 | Dimensi yang boleh dipotong |  |
| 10 | Filter default |  |
| 11 | Arti nilai kosong | 0 / tidak ada data / tidak dihitung — pilih satu |
| 12 | Versi | v1, tanggal berlaku |
| 13 | **Definisi capaian vs target** | capaian = metrik ÷ target; target kosong memberi capaian kosong |
| 14 | Peran di proyek | primary / supporting + alasannya satu baris |

### Cara metrik ini di-gaming
Tulis satu cara orang bisa membuat metrik ini terlihat bagus tanpa benar-benar membaik:
______________________________________________________________________________

### Guard test-nya
Satu test yang menangkap cara itu:
______________________________________________________________________________

## Metrik 2 — ______________________

| # | Field | Isi |
|---|---|---|
| 1 | Nama metrik |  |
| 2 | Definisi (satu kalimat, tanpa jargon) |  |
| 3 | Rumus (SQL-nya, bukan bahasa manusia) |  |
| 4 | Grain |  |
| 5 | Tabel sumber |  |
| 6 | Owner (jabatan bernama) |  |
| 7 | Time basis | per hari kalender WIB / per bulan / … |
| 8 | Satuan |  |
| 9 | Dimensi yang boleh dipotong |  |
| 10 | Filter default |  |
| 11 | Arti nilai kosong | 0 / tidak ada data / tidak dihitung — pilih satu |
| 12 | Versi | v1, tanggal berlaku |
| 13 | **Definisi capaian vs target** |  |
| 14 | Peran di proyek | primary / supporting + alasannya satu baris |

## Metrik 3 — ______________________

| # | Field | Isi |
|---|---|---|
| 1 | Nama metrik |  |
| 2 | Definisi (satu kalimat, tanpa jargon) |  |
| 3 | Rumus (SQL-nya, bukan bahasa manusia) |  |
| 4 | Grain |  |
| 5 | Tabel sumber |  |
| 6 | Owner (jabatan bernama) |  |
| 7 | Time basis | per hari kalender WIB / per bulan / … |
| 8 | Satuan |  |
| 9 | Dimensi yang boleh dipotong |  |
| 10 | Filter default |  |
| 11 | Arti nilai kosong | 0 / tidak ada data / tidak dihitung — pilih satu |
| 12 | Versi | v1, tanggal berlaku |
| 13 | **Definisi capaian vs target** |  |
| 14 | Peran di proyek | primary / supporting + alasannya satu baris |
