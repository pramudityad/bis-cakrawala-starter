# Business Intelligence Systems — Starter

**SDA2161 · Sains Data · Semester 5 · Universitas Cakrawala**

Repo ini adalah tempat kerja kelompokmu selama 16 sesi. Semua artefak D0–D13, UTS, dan UAS
dikerjakan **di dalam sesi** dan di-commit sebelum kelas selesai. Tidak ada pekerjaan rumah.

---

## Setup (sekali saja, sebelum Sesi 3)

Ini **administratif**, bukan tugas — sama seperti membawa laptop.

```bash
# 1. Di GitHub: buka repo template, klik "Use this template"
#    Nama repo: bis-2026-kNN   (NN = nomor kelompokmu, contoh bis-2026-k04)

# 2. Clone repo KELOMPOKMU (bukan template-nya)
git clone https://github.com/<username-kamu>/bis-2026-kNN
cd bis-2026-kNN

# 3. Jalankan setup
python bootstrap.py
```

Kalau berhasil, kamu dapat satu baris `OK | python ... | duckdb ...`.
**Paste baris itu ke thread LMS.**

Kalau gagal, skrip mencetak pesan error lengkap. **Salin seluruh pesan itu ke thread LMS.**
Dibereskan di 5 menit pertama lab Sesi 3 — jangan panik, jangan begadang.

> Windows: saat install Python dari python.org, **centang "Add Python to PATH"**.
> Kalau `python` tidak dikenali, coba `py bootstrap.py`.

---

## Dua perintah yang dipakai sepanjang semester

```bash
python -m pipeline.load --topic tX --twice   # jalankan pipeline 2x, bandingkan row count
python checkpoint.py verify --sesi N         # cek sendiri DoD sesi ini sebelum keluar
```

`checkpoint.py verify` adalah perintah **yang sama persis** yang dipakai dosen untuk menilai.
Kalau hijau di laptopmu, hijau juga saat dinilai.

---

## Berkas siapa

| Punya kamu — kerjakan | Punya dosen — jangan diubah |
|---|---|
| `sql/20_dim_*.sql`, `sql/30_fact_*.sql` | `sql/00_profiling.sql`, `sql/10_dim_date.sql` |
| `sql/40_analytics/`, `sql/50_metrics/` | `pipeline/`, `checkpoint.py` |
| `dashboard/config.yml` | `dashboard/build.py`, `dashboard/charts.py` |
| `tests/test_definitions.yml` | `tests/run_tests.py` |
| `docs/` (semua artefak D0–D13) | `models/`, `data/raw/` |

`python bootstrap.py --update` memperbarui berkas milik dosen saja. Kerjamu tidak disentuh.

---

## Peta sesi

| Sesi | Artefak | Yang kamu hasilkan |
|---|---|---|
| 1 | D0 | Inventaris keputusan — 5 keputusan, 1 dilingkari, pengambil keputusan bernama |
| 2 | D1 | 8 pertanyaan bisnis + peta sumber & grain |
| 3 | D2 | Star schema + kalimat grain + aditivitas + tipe SCD · **grain dikunci** |
| 4 | D3 | Pemuatan idempoten 1 dimensi + 1 fact · **demo live** |
| 5 | D4 | 6 pengujian kualitas data, 1 sengaja GAGAL · **demo live** |
| 6 | D5 | 8 kueri analitik + keputusan pra-agregasi · **demo live** |
| 7 | D6 | Kamus metrik 5 metrik × 12 field |
| **8** | **UTS + D7** | **Ujian Tengah Semester + scope cut ditandatangani** |
| 9 | D8 | Wireframe dashboard beranotasi |
| 10 | D9 | Dashboard live di atas warehouse kelompokmu |
| 11 | D10 | Dashboard revisi + cerita data 3 menit |
| 12 | D11 | Kolom hasil penskoran + versi model · **demo live** |
| 13 | D12 | Lampiran tata kelola 6 bagian |
| 14 | D13 | Memo komparatif 1 halaman |
| 15 | — | Presentasi & pembelaan capstone |
| **16** | **UAS** | **Ujian Akhir Semester** |

---

## Aturan yang paling sering bikin nilai hilang

1. **Artefak wajib bisa dipertahankan.** Artefak yang tidak bisa kamu jelaskan bernilai **0**,
   sebagus apa pun hasilnya. Berlaku untuk bagian yang dikerjakan anggota lain juga.
2. **Pipeline dinilai dengan dijalankan dua kali.** Kalau row count berubah di run kedua,
   pipeline-mu tidak idempoten.
3. **Tidak bisa dijalankan = 0 fungsionalitas.** Kueri atau pipeline yang error, dan dokumen
   yang tidak lengkap, tidak mendapat nilai fungsionalitas.
4. **AI assistant** boleh saat praktikum dengan pengungkapan singkat. **Dilarang saat UTS dan UAS.**
5. **Commit sebelum keluar.** Waktu commit adalah bukti kerjamu dilakukan di dalam sesi.
   Biasakan tiap anggota commit dari akunnya sendiri, atau pakai
   `Co-authored-by:` — kontribusi individu dinilai dari sini.

---

## Kalau pipeline-mu jebol

`warehouse/fallback/` berisi database yang sudah jadi untuk tiap topik. Pakai itu supaya kamu
tetap bisa mengerjakan sesi berikutnya, lalu perbaiki pipeline-mu belakangan. Memakai fallback
tidak menghapus nilai sesi lain — berhenti total yang menghapusnya.
