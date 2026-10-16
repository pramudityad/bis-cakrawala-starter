# bis-cakrawala-starter — Business Intelligence Systems (SDA2161)

Repo template untuk 9 tim. Satu repo per tim (`Use this template`), semua artefak dikerjakan **di
dalam sesi** dan dibuktikan lewat commit bertanggal sebelum 20:00.

## Setup 5 menit

```bash
pip install -r requirements.txt
python -m pipeline.profile --topic t3 --slice k1      # D1: profil data sebelum transformasi
python -m pipeline.load    --topic t3 --slice k1 --twice   # D3: load 2x, cek row count
python tests/run_tests.py  --topic t3                 # D4: 6 quality test, PASS/FAIL + severity
python checkpoint.py verify --sesi 8                  # DoD UTS (design checkpoint)
```

Semua perintah **offline** — data seed sudah ada di `data/raw/`, tidak ada unduhan saat lab.

## Tiga topik (dataset dari dosen, bukan pilihan sendiri)

| Topik | Folder | Slice |
|---|---|---|
| **T1** Kampus: Presensi & Kelulusan | `data/raw/t1_kampus/` | `--slice k4` (angkatan 2024) · `k5` (2023) · `k7` (2022) |
| **T2** POS UMKM Multi-Outlet | `data/raw/t2_umkm/` | `--slice k8` (outlet A+B+C, 12 bulan) · `k9` (outlet A, 6 bulan, scope −20%) |
| **T3** Cuaca Ekstrem per Desa (BMKG) | `data/raw/t3_publik/<slice>/` | `--slice k1` Kota Bogor · `k2` Kota Semarang · `k3` Kota Makassar · `k6` Kota Denpasar |
| **T4** Ritel Omnichannel (Sesi 12–15) | `data/raw/t4_omni/` | **tidak ada slice** — satu dataset untuk seluruh kelas |

## T4 — satu proyek, empat langkah (Sesi 12–15)

Mulai Sesi 12 kamu mengerjakan **satu proyek**, bukan latihan terpisah per pertemuan: satu dataset,
satu stakeholder (Head of Omnichannel Retail), satu pertanyaan, empat langkah yang saling menopang.

> "Which channel drives our target miss this quarter, and what should we do about it?"

| Langkah | Sesi | Yang kamu bangun |
|---|---|---|
| 1 · fondasi | 12 | profil, bersihkan, bintang, `fact_order_line`, `pred_anomaly_daily` |
| 2 · KPI & target | 13 | `dim_target`, `fact_target`, `v_kpi_monthly`, kamus metrik, D12 |
| 3 · dashboard & diagnosis | 14 | dashboard Metabase (maks 4 tile), `v_revenue_bridge` |
| 4 · insight | 15 | `docs/insights_s15.md`, tag `s15-final` |

```bash
# Sesi 12
python -m pipeline.profile --topic t4                  # tulis docs/profile_t4.md
python -m pipeline.load    --topic t4 --twice          # T4 tidak pakai --slice
python checkpoint.py verify --sesi 12 --step 1         # lalu step 2, 3, 4

# Sesi 13 dan 14 memakai berkas urutan yang berbeda (lihat warehouse/README.md)
python -m pipeline.load --topic t4 --twice --sql sql/load_t4_langkah2.sql
python checkpoint.py verify --sesi 13 --step 2
python -m pipeline.load --topic t4 --twice --sql sql/load_t4_langkah3.sql
python checkpoint.py verify --sesi 14 --step 3b
python checkpoint.py verify --sesi 15 --step 1
```

**Aturan yang berlaku sepanjang empat langkah.** Kamu bekerja di branch `<nim>` sendiri. Tiap
langkah berakhir dengan **tag aman** (`s12-step1a-ok` … `s15-final`). Kalau waktumu habis dan
`checkpoint` masih merah: tarik tag langkah sebelumnya (`git checkout s12-step1b-ok`), tulis satu
baris apa yang kamu lewati, lalu ikut langkah berikutnya — **jangan berhenti**. Yang dinilai adalah
penjelasanmu di pembelaan, bukan kecepatanmu.

`warehouse/fallback/t4.duckdb` adalah T4 yang sudah jadi untuk keadaan darurat. Kalau kamu memakainya,
katakan terus terang ke dosen: itu menggantikan artefakmu, dan tidak bisa diklaim sebagai kerja
sendiri.

## Struktur

```
├── data/raw/            seed (jangan diubah; baca saja)
├── sql/
│   ├── 00_profiling.sql        DIBERIKAN — 6 query profil
│   ├── 10_dim_date.sql         DIBERIKAN — generator dimensi tanggal
│   ├── 20_dim_*.sql            TUGAS tim (D2) — DDL dimensi
│   ├── 30_fact_*.sql           TUGAS tim (D2) — DDL fact
│   ├── 40_analytics/q0N.sql    TUGAS tim (D5 + UTS item 4)
│   ├── 50_metrics/*.sql        TUGAS tim (D6) — satu berkas per metrik
│   └── load.sql                URUTAN EKSEKUSI tim (D3) — loader menolak jalan selama masih TODO
├── pipeline/
│   ├── profile.py       D1 + UTS item 3 (angka untuk test)
│   └── load.py          D3 — idempoten, `--twice`
├── tests/
│   ├── test_definitions.yml    TUGAS tim (D4 + UTS item 3)
│   └── run_tests.py            eksekutor, cetak PASS/FAIL + exit code
├── checkpoint.py        daftar cek DoD per sesi (design & build)
├── docs/                D0, D6, D7, D12 — template terisi contoh
└── warehouse/           hasil kerja: <topik>_<slice>.duckdb + fallback/
```

## Aturan yang dinilai

- **Idempotensi adalah syarat, bukan bonus.** `--twice` harus mencetak row count yang sama. Kalau tim mau membuktikan bahwa `INSERT` polos menggandakan baris, jalankan `--strategy insert_only` — itu contoh yang sengaja salah.
- **Test wajib punya severity.** `blocking` menghentikan load; `warning` hanya memberi tahu. Test tanpa severity diabaikan.
- **`WHERE 1=1` bukan test.** Test harus gagal ketika datanya salah, bukan ketika tabel kosong.
- **Desain dulu (UTS), bangun kemudian (UAS).** `checkpoint.py verify --sesi 8` untuk desain; `--sesi 4|5` untuk artefak build.

## Jalur penyelamat

`warehouse/fallback/<topik>_<slice>.duckdb` adalah warehouse yang **sudah jadi** untuk topikmu —
dipakai **hanya** kalau pipeline tim jebol di tengah sesi dan kamu butuh lanjut ke Sesi 9–10.
Catatan penting:

- **Tidak ada berkas `.sql` acuan di repo ini.** SQL lengkapnya tidak dibagikan; yang ada hanya
  hasil jadinya. Kalau kamu memakai fallback, itu menggantikan artefak D3-mu — katakan terus terang
  ke dosen, jangan mengaku sebagai hasil tim.
- Dosen menanyakan bagian mana pun dari artefak yang kamu kumpulkan. Yang tidak bisa dijelaskan
  bernilai 0 (RPS butir 5), dan fallback ini tidak bisa dijelaskan sebagai kerja tim.
