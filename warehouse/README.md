# warehouse/

Hasil kerja, bukan sumber. Berkas `.duckdb` **tidak** di-commit (lihat `.gitignore`).

```
python -m pipeline.load --topic t2 --slice k8            # → warehouse/t2_k8.duckdb
python -m pipeline.load --topic t2 --slice k8 --twice    # bukti idempoten
python -m pipeline.load --topic t2 --slice k8 --fallback # → warehouse/fallback/t2.duckdb (jalur penyelamat)
```

## T4 (Sesi 12–15) — satu dataset, tiga langkah load

T4 tidak punya slice, jadi warehouse-nya `warehouse/t4.duckdb`. Urutan load-nya tumbuh per sesi:

```
python -m pipeline.load --topic t4 --twice                                # Sesi 12: langkah 1
python -m pipeline.load --topic t4 --twice --sql sql/load_t4_langkah2.sql # Sesi 13: + target & KPI
python -m pipeline.load --topic t4 --twice --sql sql/load_t4_langkah3.sql # Sesi 14: + jembatan omzet
```

Setiap run menulis `warehouse/t4.load.json` — itulah bukti run-1 = run-2 yang dibaca
`checkpoint.py`. Tanpa `--twice`, buktinya tidak ada dan langkah 1c tidak akan hijau.

`warehouse/fallback/t4.duckdb` adalah T4 yang sudah jadi. Dipakai **hanya** kalau pipeline-mu jebol;
memakainya menggantikan artefakmu, jadi katakan terus terang ke dosen — bukan diklaim sebagai hasil
kerja sendiri.
