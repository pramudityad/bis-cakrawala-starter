"""checkpoint.py — daftar cek DoD per sesi, dijalankan mahasiswa SEBELUM keluar ruangan,
dan dijalankan dosen dengan perintah yang sama persis saat menilai.

    python checkpoint.py verify --sesi 8                    # UTS: design checkpoint (semua topik)
    python checkpoint.py verify --sesi 5 --topic t2         # D4: test kualitas
    python checkpoint.py verify --sesi 4 --topic t2 --slice k8   # D3: load idempoten

    python checkpoint.py verify --sesi 12 --step 2          # T4 langkah 1: staging bersih
    python checkpoint.py verify --sesi 13 --step 2          # T4 langkah 2: view attainment
    python checkpoint.py verify --sesi 14 --step 3b         # T4 langkah 3: jembatan omzet
    python checkpoint.py verify --sesi 15 --step 1          # T4 langkah 4: insight

Exit code 0 = semua syarat wajib terpenuhi. 1 = ada yang belum.

Sesi 12–15 memakai `--step` dan topik `t4` secara default. Langkahnya bertingkat, jadi `--step N`
memeriksa langkah 1..N sekaligus dan menunjukkan di langkah mana kamu berhenti.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pipeline import config  # noqa: E402

OK, NO, WARN = "\033[32m✓\033[0m", "\033[31m✗\033[0m", "\033[33m•\033[0m"

SESI_T4 = ("12", "13", "14", "15")
KOLOM_PRED = ["tanggal", "channel", "revenue", "zscore", "anomaly_flag", "model_version", "scored_at"]
KOLOM_KPI = ["bulan", "channel", "wilayah", "net_revenue", "orders", "return_rate",
             "target_revenue", "attainment_pct"]
KOLOM_BRIDGE = ["bulan", "channel", "volume_effect", "price_effect", "mix_effect"]
KOSONG = "____"


def baca(path: str) -> str:
    return open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def tunjukkan(syarat: str, lulus: bool, catatan: str = "", wajib: bool = True) -> bool:
    tanda = OK if lulus else (NO if wajib else WARN)
    print(f"  {tanda} {syarat}" + (f"  — {catatan}" if catatan else ""))
    return lulus or not wajib


def _isi_ddl(berkas: list[str]) -> bool:
    """Berkas DDL sudah diisi, bukan masih stub TODO."""
    return all("TODO" not in baca(p) for p in berkas)


def _tests_topik(topic: str) -> list[dict]:
    import yaml
    isi = baca(os.path.join(config.ROOT, "tests", "test_definitions.yml"))
    if not isi:
        return []
    data = yaml.safe_load(isi) or {}
    return [t for t in (data.get("tests") or []) if t.get("topic") == topic]


# ================================================================ Sesi 4/5/8 (T1–T3)

def sesi8(topic: str) -> list[bool]:
    print(f"DoD Sesi 8 — Design Checkpoint (desain saja, tidak ada yang dijalankan) · topik {topic}")
    hasil = []
    dim = sorted(glob.glob(os.path.join(config.SQL, "20_dim_*.sql")))
    fact = sorted(glob.glob(os.path.join(config.SQL, "30_fact_*.sql")))
    analitik = sorted(glob.glob(os.path.join(config.SQL, "40_analytics", "q*.sql")))
    isi_fact = baca(fact[0]) if fact else ""
    isi_dim = " ".join(baca(p) for p in dim)
    tests = _tests_topik(topic)
    kamus = baca(os.path.join(config.DOCS, "kamus_metrik.md"))
    d7 = baca(os.path.join(config.DOCS, "D7_scope_cut.md"))
    design = baca(os.path.join(config.ROOT, "pipeline", "DESIGN_load.md"))

    hasil.append(tunjukkan("DDL dimensi ada (sql/20_dim_*.sql)", len(dim) >= 3, f"{len(dim)} berkas"))
    hasil.append(tunjukkan("DDL fact ada (sql/30_fact_*.sql)", len(fact) >= 1, f"{len(fact)} berkas"))
    hasil.append(tunjukkan("DDL sudah diisi (bukan stub TODO)", _isi_ddl(dim + fact),
                           "masih ada berkas bertanda TODO"))
    hasil.append(tunjukkan("surrogate key dipakai di fact", bool(re.search(r"\w+_sk\b", isi_fact))))
    hasil.append(tunjukkan("ada dimensi Type 2 (valid_from/valid_to/is_current)",
                           all(k in isi_dim.lower() for k in ("valid_from", "valid_to", "is_current"))))
    hasil.append(tunjukkan("aditivitas ditandai (additive / semi / non-additive)",
                           bool(re.search(r"additive", isi_fact + isi_dim, re.I))))
    hasil.append(tunjukkan("pipeline/DESIGN_load.md terisi (tanpa TODO)", len(design) > 200 and "TODO" not in design,
                           f"{len(design)} karakter"))
    hasil.append(tunjukkan(f"6 test kualitas untuk topik {topic}", len(tests) >= 6, f"{len(tests)} test"))
    hasil.append(tunjukkan("setiap test punya severity + justifikasi",
                           bool(tests) and all(t.get("severity") in ("blocking", "warning") and t.get("justifikasi") for t in tests)))
    gagal = sum(1 for t in tests if t.get("expected") == "fail")
    hasil.append(tunjukkan("ada test yang diharapkan FAIL", gagal >= 1, f"{gagal} test"))
    hasil.append(tunjukkan("3 kueri analitik sudah diisi", len(analitik) >= 3 and
                           all("TODO" not in baca(p) for p in analitik), f"{len(analitik)} berkas"))
    sel = len(re.findall(r"\|\s*[0-9]+\s*\|[^|]*\|[^|]*\S", kamus))
    hasil.append(tunjukkan("kamus metrik: ≥10 dari 12 field terisi", sel >= 10, f"{sel} baris terisi"))
    hasil.append(tunjukkan("D7 scope cut: bagian AKAN dan TIDAK LAGI terisi",
                           "AKAN" in d7.upper() and "TIDAK" in d7.upper()))
    hasil.append(tunjukkan("D7 ditandatangani", "tanda tangan" in d7.lower()))
    return hasil


def sesi4(topic: str, slice_id: str) -> list[bool]:
    print(f"DoD Sesi 4 — D3 load idempoten ({topic}/{slice_id})")
    db = config.db_path(topic, slice_id)
    pakai_fallback = False
    if not os.path.exists(db):
        alternatif = os.path.join(config.WAREHOUSE, "fallback", f"{topic}_{slice_id}.duckdb")
        if os.path.exists(alternatif):
            db, pakai_fallback = alternatif, True
    hasil = [tunjukkan(f"warehouse ada ({os.path.relpath(db, config.ROOT)})", os.path.exists(db))]
    if pakai_fallback:
        hasil.append(tunjukkan("Pakai jalur penyelamat — artefak D3 tim belum ada", False,
                               "katakan terus terang ke dosen; fallback tidak bisa dijelaskan sebagai kerja tim",
                               wajib=False))
    if os.path.exists(db):
        import duckdb
        con = duckdb.connect(db, read_only=True)
        tabel = _tabel(con)
        fat = config.TOPICS[topic]["fact"]
        hasil.append(tunjukkan(f"fact `{fat}` ada", fat in tabel, ", ".join(sorted(tabel)[:6])))
        if fat in tabel:
            n = con.execute(f'SELECT count(*) FROM "{fat}"').fetchone()[0]
            hasil.append(tunjukkan("fact berisi baris", n > 0, f"{n:,} baris"))
            orbit = con.execute(f'SELECT count(*) FROM "{fat}" f WHERE f.date_sk IS NULL').fetchone()[0]
            hasil.append(tunjukkan("semua baris fact punya date_sk (dim_date ter-join)", orbit == 0,
                                   f"{orbit:,} baris tanpa tanggal"))
        con.close()
    return hasil


def sesi5(topic: str, slice_id: str) -> list[bool]:
    print(f"DoD Sesi 5 — D4 test kualitas ({topic}/{slice_id})")
    tests = _tests_topik(topic)
    isi = " ".join(str(t.get("sql", "")) for t in tests)
    hasil = [tunjukkan(f"≥6 test untuk topik {topic}", len(tests) >= 6, f"{len(tests)} test")]
    hasil.append(tunjukkan("≥1 test blocking", any(t.get("severity") == "blocking" for t in tests)))
    hasil.append(tunjukkan("≥1 test warning", any(t.get("severity") == "warning" for t in tests)))
    hasil.append(tunjukkan("≥1 test diharapkan FAIL", any(t.get("expected") == "fail" for t in tests)))
    hasil.append(tunjukkan("tidak ada test `WHERE 1=1`", "1=1" not in isi))
    hasil.append(tunjukkan("setiap test punya justifikasi", all(t.get("justifikasi") for t in tests)))
    return hasil


# ================================================================ Sesi 12–15 (T4)

def _tabel(con) -> list[str]:
    return [r[0] for r in con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()]


def _kolom(con, tabel: str) -> list[str]:
    return [r[0] for r in con.execute(f'DESCRIBE "{tabel}"').fetchall()]


def _satu(con, sql: str):
    return con.execute(sql).fetchone()[0]


def _catat_load(topic: str) -> dict:
    """Bukti `--twice` yang ditulis pipeline.load."""
    try:
        return json.loads(baca(os.path.join(config.WAREHOUSE, f"{topic}.load.json"))) or {}
    except ValueError:
        return {}


def buka_t4(topic: str):
    """(koneksi, path, pakai_fallback). Koneksi None kalau warehouse belum ada."""
    import duckdb
    db = config.db_path(topic)
    if os.path.exists(db):
        return duckdb.connect(db, read_only=True), db, False
    alternatif = os.path.join(config.WAREHOUSE, "fallback", f"{topic}.duckdb")
    if os.path.exists(alternatif):
        return duckdb.connect(alternatif, read_only=True), alternatif, True
    return None, db, False


def _cek_profil(hasil: list[bool], topic: str) -> None:
    """Langkah 1a — lima temuan dengan angka, satu soal waktu, satu soal identitas."""
    teks = baca(os.path.join(config.DOCS, "profile_t4.md"))
    baris = [b for b in teks.splitlines() if re.match(r"^\s*\|\s*[1-9]\s*\|", b)]
    berisi = [b for b in baris if re.search(r"\d{2,}", b.replace("|", " "))]
    hasil.append(tunjukkan("docs/profile_t4.md punya 5 baris temuan bernomor", len(baris) >= 5,
                           f"{len(baris)} baris"))
    hasil.append(tunjukkan("tiap temuan membawa angka", len(berisi) >= 5, f"{len(berisi)} baris berangka"))
    hasil.append(tunjukkan("ada temuan soal waktu (UTC/WIB/timestamp)",
                           bool(re.search(r"utc|wib|timestamp|waktu|zona", teks, re.I)),
                           "sebut salah satu: UTC, WIB, timestamp", wajib=False))
    hasil.append(tunjukkan("ada temuan soal identitas (email/handle/loyalty)",
                           bool(re.search(r"identitas|email|handle|loyalty", teks, re.I)),
                           "sebut salah satu: email, handle, loyalty_id", wajib=False))
    hasil.append(tunjukkan("satu temuan dibintangi", bool(re.search(r"bintang", teks, re.I)),
                           "", wajib=False))


def _cek_staging(hasil: list[bool], con) -> None:
    """Langkah 1b — staging bersih dan beralasan."""
    tabel = _tabel(con)
    ada = [t for t in ("stg_orders", "stg_order_items", "stg_returns") if t in tabel]
    hasil.append(tunjukkan("stg_orders, stg_order_items, stg_returns ada", len(ada) == 3,
                           ", ".join(ada) or "belum ada"))
    if "stg_orders" not in tabel:
        return
    kelebihan = _satu(con, "SELECT count(*) - count(DISTINCT order_id) FROM stg_orders")
    hasil.append(tunjukkan("tidak ada order_id kembar di stg_orders", kelebihan == 0, f"{kelebihan:,} kelebihan"))
    kosong = _satu(con, "SELECT count(*) FROM stg_orders WHERE order_ts_wib IS NULL")
    hasil.append(tunjukkan("semua waktu terbaca (UTC sudah jadi WIB)", kosong == 0, f"{kosong:,} baris kosong"))
    varian = _satu(con, "SELECT count(DISTINCT status_clean) FROM stg_orders")
    hasil.append(tunjukkan("status sudah dipetakan (≤4 nilai bersih)", varian <= 4, f"{varian} nilai"))
    if "quarantine_items" in tabel:
        n = _satu(con, "SELECT count(*) FROM quarantine_items")
        hasil.append(tunjukkan("quarantine_items terisi (kamu tahu apa yang disisihkan)", n > 0, f"{n:,} baris"))


def _cek_model(hasil: list[bool], con, topic: str) -> None:
    """Langkah 1c — dimensi, fact, dua kali, rekonsiliasi."""
    tabel = _tabel(con)
    perlu = ["dim_date", "dim_channel", "dim_product", "dim_store", "dim_customer",
             "bridge_customer_ref", "fact_order_line"]
    kurang = [t for t in perlu if t not in tabel]
    hasil.append(tunjukkan("lima dimensi + fact + jembatan identitas ada", not kurang,
                           ", ".join(kurang) or "semua ada"))
    if "fact_order_line" not in tabel:
        return
    if "stg_order_items" in tabel:
        n_fak = _satu(con, "SELECT count(*) FROM fact_order_line")
        n_stg = _satu(con, "SELECT count(*) FROM stg_order_items")
        hasil.append(tunjukkan("jumlah baris fact = staging (tidak ada baris beranak)", n_fak == n_stg,
                               f"{n_fak:,} vs {n_stg:,}"))
    selisih = _satu(con, """SELECT (SELECT coalesce(sum(neto), 0) FROM fact_order_line)
                                 - (SELECT coalesce(sum(neto), 0) FROM stg_order_items)""")
    hasil.append(tunjukkan("omzet fact = omzet staging bersih", selisih == 0, f"selisih {selisih:,.0f}"))
    tanpa_sk = _satu(con, "SELECT count(*) FROM fact_order_line WHERE date_sk IS NULL OR customer_sk IS NULL")
    hasil.append(tunjukkan("setiap baris fact punya kunci dimensi", tanpa_sk == 0, f"{tanpa_sk:,} baris"))
    catat = _catat_load(topic)
    if not catat:
        hasil.append(tunjukkan("bukti `load --twice` tersimpan", False,
                               "jalankan: python -m pipeline.load --topic t4 --twice"))
    else:
        hasil.append(tunjukkan("load dijalankan dengan --twice", catat.get("run2") is not None,
                               "tanpa --twice tidak ada buktinya"))
        hasil.append(tunjukkan("row count run-1 == run-2 (idempoten)", bool(catat.get("idempoten"))))


def _cek_pred(hasil: list[bool], con, cetak_tanggal: bool = False) -> None:
    """Langkah 1d — penanda anomali: kolom tepat, berversi, dan benar-benar menyala."""
    if "pred_anomaly_daily" not in _tabel(con):
        hasil.append(tunjukkan("tabel pred_anomaly_daily ada", False, "langkah 1d belum jadi"))
        return
    kolom = _kolom(con, "pred_anomaly_daily")
    hasil.append(tunjukkan("kolomnya tujuh dan sesuai kontrak", sorted(kolom) == sorted(KOLOM_PRED),
                           ", ".join(kolom)))
    n = _satu(con, "SELECT count(*) FROM pred_anomaly_daily")
    hasil.append(tunjukkan("tabel berisi baris", n > 0, f"{n:,} baris"))
    if n == 0:
        return
    hasil.append(tunjukkan("zscore terisi (hanya hari berjendela penuh)",
                           _satu(con, "SELECT count(*) FROM pred_anomaly_daily WHERE zscore IS NULL") == 0,
                           "hari tanpa riwayat penuh jangan diskor"))
    hasil.append(tunjukkan("model_version terisi",
                           _satu(con, "SELECT count(*) FROM pred_anomaly_daily WHERE coalesce(model_version, '') = ''") == 0))
    hasil.append(tunjukkan("scored_at terisi (angkanya bisa diaudit)",
                           _satu(con, "SELECT count(*) FROM pred_anomaly_daily WHERE scored_at IS NULL") == 0))
    nyala = _satu(con, "SELECT count(*) FROM pred_anomaly_daily WHERE anomaly_flag")
    hasil.append(tunjukkan("penanda menyala, tapi tidak di semua hari", 0 < nyala < n,
                           f"{nyala:,} dari {n:,} hari"))
    if cetak_tanggal and nyala:
        tanggal = [r[0] for r in con.execute(
            "SELECT DISTINCT tanggal FROM pred_anomaly_daily WHERE anomaly_flag ORDER BY 1").fetchall()]
        print(f"     tanggal menyala ({len(tanggal)}): " + ", ".join(str(t) for t in tanggal[:12])
              + (" …" if len(tanggal) > 12 else ""))
        print("     Untuk tiap tanggal itu kamu harus bisa bilang: anomali data, anomali bisnis, atau")
        print("     kampanye yang memang ada di kalender. Yang tidak bisa dijelaskan, itu temuannya.")


def sesi12(topic: str, sampai: int, cetak: bool = True) -> list[bool]:
    print(f"DoD Sesi 12 — langkah 1: fondasi ({topic})")
    hasil: list[bool] = []
    seed = config.topic_dir(topic)
    kurang = [b for b in config.TOPICS[topic]["files"] if not os.path.exists(os.path.join(seed, b))]
    hasil.append(tunjukkan("seed T4 lengkap (8 berkas)", not kurang, ", ".join(kurang) or "semua ada"))
    hasil.append(tunjukkan("sql/load_t4.sql ada", os.path.exists(os.path.join(config.SQL, "load_t4.sql"))))
    if sampai <= 0:
        return hasil

    con, db, fallback = buka_t4(topic)
    if con is None:
        hasil.append(tunjukkan(f"warehouse {os.path.relpath(db, config.ROOT)} ada", False,
                               "jalankan: python -m pipeline.load --topic t4 --twice"))
        hasil.append(tunjukkan("docs/profile_t4.md berisi lima temuan", False, "butuh profil dulu", wajib=False))
        return hasil
    if fallback:
        hasil.append(tunjukkan("Pakai jalur penyelamat (warehouse/fallback/t4.duckdb)", False,
                               "katakan terus terang ke dosen; fallback tidak bisa dijelaskan sebagai kerja tim",
                               wajib=False))
    if sampai >= 1:
        print("  — langkah 1a: profil dan lima temuan")
        _cek_profil(hasil, topic)
    if sampai >= 2:
        print("  — langkah 1b: staging bersih")
        _cek_staging(hasil, con)
    if sampai >= 3:
        print("  — langkah 1c: dimensi, fact, dua kali")
        _cek_model(hasil, con, topic)
    if sampai >= 4:
        print("  — langkah 1d: penanda anomali")
        _cek_pred(hasil, con, cetak_tanggal=cetak)
    con.close()
    return hasil


def sesi13(topic: str, sampai: int, cetak: bool = True) -> list[bool]:
    print(f"DoD Sesi 13 — langkah 2: KPI dan target ({topic})")
    if sampai == 0:
        return sesi12(topic, 4, cetak=False)
    hasil: list[bool] = []
    con, db, fallback = buka_t4(topic)
    if con is None:
        return [tunjukkan(f"warehouse {os.path.relpath(db, config.ROOT)} ada", False, "Sesi 12 dulu")]
    if fallback:
        hasil.append(tunjukkan("Pakai jalur penyelamat — artefak langkah 2 belum ada", False,
                               "katakan terus terang ke dosen", wajib=False))
    tabel = _tabel(con)

    if sampai >= 1:
        print("  — langkah 2a: tabel target")
        ada = [t for t in ("dim_target", "fact_target") if t in tabel]
        hasil.append(tunjukkan("dim_target dan fact_target ada", len(ada) == 2, ", ".join(ada) or "belum ada"))
        if "fact_target" in tabel:
            n = _satu(con, "SELECT count(*) FROM fact_target")
            hasil.append(tunjukkan("fact_target berisi baris", n > 0, f"{n:,} baris"))
            kosong = _satu(con, "SELECT count(*) FROM fact_target WHERE target_revenue IS NULL")
            hasil.append(tunjukkan("target yang tidak diset tetap NULL", kosong > 0, f"{kosong:,} baris NULL"))
            nol = _satu(con, "SELECT count(*) FROM fact_target WHERE target_revenue = 0")
            hasil.append(tunjukkan("tidak ada target bernilai 0 (0 itu keputusan, NULL itu fakta)",
                                   nol == 0, f"{nol:,} baris bernilai 0"))
        catat = _catat_load(topic)
        if catat:
            hasil.append(tunjukkan("load --twice masih idempoten setelah target masuk",
                                   bool(catat.get("idempoten")), "jalankan ulang load --twice"))
    if sampai >= 2:
        print("  — langkah 2b: view attainment")
        if "v_kpi_monthly" not in tabel:
            hasil.append(tunjukkan("v_kpi_monthly ada", False, "belum dibuat"))
        else:
            kolom = _kolom(con, "v_kpi_monthly")
            hasil.append(tunjukkan("delapan kolom sesuai kontrak", sorted(kolom) == sorted(KOLOM_KPI),
                                   ", ".join(kolom)))
            selisih = _satu(con, """SELECT (SELECT coalesce(sum(net_revenue), 0) FROM v_kpi_monthly)
                                         - (SELECT coalesce(sum(neto), 0) FROM fact_order_line)""")
            hasil.append(tunjukkan("net_revenue view = omzet fact (rekonsiliasi)", selisih == 0,
                                   f"selisih {selisih:,.0f}"))
            salah = _satu(con, """SELECT count(*) FROM v_kpi_monthly
                                  WHERE target_revenue IS NULL AND attainment_pct IS NOT NULL""")
            hasil.append(tunjukkan("target NULL → attainment NULL (bukan 0)", salah == 0,
                                   f"{salah:,} baris salah"))
    if sampai >= 3:
        print("  — langkah 2c: kamus metrik")
        kamus = baca(os.path.join(config.DOCS, "kamus_metrik.md"))
        blok = len(re.findall(r"^##\s*Metrik", kamus, re.M))
        hasil.append(tunjukkan("tiga KPI ada di kamus", blok >= 3, f"{blok} blok metrik"))
        # Baris field = "| nomor | nama field | isi |" dengan isi tidak kosong.
        terisi = len([b for b in kamus.splitlines()
                      if re.match(r"^\s*\|\s*\d+\s*\|", b) and
                      len(re.split(r"\|", b)) >= 4 and re.split(r"\|", b)[3].strip()])
        hasil.append(tunjukkan("≥30 baris field terisi (3 KPI × 10 field lebih)", terisi >= 30,
                               f"{terisi} baris terisi"))
        hasil.append(tunjukkan('ada baris "Definisi capaian vs target"', bool(re.search(r"capaian", kamus, re.I))))
        hasil.append(tunjukkan("satu KPI ditandai primary, dua supporting",
                               bool(re.search(r"\b(primary|utama)\b", kamus, re.I)), "", wajib=False))
        hasil.append(tunjukkan("owner berupa jabatan, bukan nama tim",
                               not re.search(r"owner[^\n|]*\|\s*(data team|tim data)\b", kamus, re.I),
                               "", wajib=False))
        hasil.append(tunjukkan("tidak ada placeholder yang tersisa", KOSONG not in kamus, "", wajib=False))
    if sampai >= 4:
        print("  — langkah 2d: lampiran tata kelola")
        d12 = baca(os.path.join(config.DOCS, "D12_governance.md"))
        bagian = len(re.findall(r"^\s*\d+\.\s*\*\*", d12, re.M))
        hasil.append(tunjukkan("sembilan bagian bernomor", bagian >= 9, f"{bagian} bagian"))
        hasil.append(tunjukkan("pemilik berupa jabatan, bukan tim",
                               bool(re.search(r"jabatan", d12, re.I)), "", wajib=False))
        hasil.append(tunjukkan("ada satu kolom bertanda tidak di-ingest",
                               bool(re.search(r"tidak di-?ingest", d12, re.I))))
        hasil.append(tunjukkan("jawaban retensi tahan terhadap dimensi Type 2",
                               bool(re.search(r"type\s*2", d12, re.I)), "", wajib=False))
        hasil.append(tunjukkan("tidak ada bagian yang dibiarkan kosong", KOSONG not in d12))
    con.close()
    return hasil


def sesi14(topic: str, step: str) -> list[bool]:
    print(f"DoD Sesi 14 — langkah 3: dashboard dan diagnosis ({topic}) · step {step}")
    hasil: list[bool] = []
    con, db, _ = buka_t4(topic)
    if con is None:
        return [tunjukkan(f"warehouse {os.path.relpath(db, config.ROOT)} ada", False, "Sesi 12–13 dulu")]
    tabel = _tabel(con)

    if step == "3a":
        print("  — 3a: tiga tile dasar (tren, target vs aktual, anomali)")
        hasil.append(tunjukkan("view Sesi 13 ada (v_kpi_monthly)", "v_kpi_monthly" in tabel))
        hasil.append(tunjukkan("tabel anomali Sesi 12 ada (pred_anomaly_daily)", "pred_anomaly_daily" in tabel))
        hasil.append(tunjukkan("tile Metabase tidak bisa diperiksa skrip", True,
                               "tile ditandai dosen di papan; yang diperiksa di sini view-nya"))
    if step == "3b":
        print("  — 3b: jembatan omzet (volume, harga, mix)")
        berkas = os.path.join(config.SQL, "31_v_revenue_bridge.sql")
        if not os.path.exists(berkas):
            hasil.append(tunjukkan("sql/31_v_revenue_bridge.sql ada", False, "belum dibuat"))
        else:
            hasil.append(tunjukkan("berkasnya sudah diisi (tanpa TODO)", "TODO" not in baca(berkas)))
        if "v_revenue_bridge" not in tabel:
            hasil.append(tunjukkan("view v_revenue_bridge ada", False,
                                   "lengkapi sql/31_v_revenue_bridge.sql lalu jalankan load"))
        else:
            kolom = _kolom(con, "v_revenue_bridge")
            hasil.append(tunjukkan("kolomnya sesuai kontrak", sorted(kolom) == sorted(KOLOM_BRIDGE),
                                   ", ".join(kolom)))
            if sorted(kolom) == sorted(KOLOM_BRIDGE) and "v_kpi_monthly" in tabel:
                # Perubahan yang harus dijelaskan jembatan: selisih omzet bulan ini vs bulan sebelumnya,
                # per channel (grain jembatan = bulan × channel, jadi wilayah dijumlahkan dulu).
                salah = _satu(con, """
                    WITH omzet_channel AS (
                        SELECT bulan, channel, sum(net_revenue) AS omzet
                        FROM v_kpi_monthly GROUP BY 1, 2
                    ),
                    banding AS (
                        SELECT bulan, channel,
                               omzet - lag(omzet) OVER (PARTITION BY channel ORDER BY bulan) AS perubahan
                        FROM omzet_channel
                    )
                    SELECT count(*) FROM v_revenue_bridge b
                    JOIN banding x ON x.bulan = b.bulan AND x.channel = b.channel
                    WHERE x.perubahan IS NOT NULL
                      AND abs(b.volume_effect + b.price_effect + b.mix_effect - x.perubahan) > 1""")
                hasil.append(tunjukkan("volume + harga + mix = perubahan omzet", salah == 0,
                                       f"{salah:,} baris tidak rekonsiliasi"))
    if step == "3c":
        print("  — 3c: satu kalimat per hari yang ditandai")
        dok = baca(os.path.join(config.DOCS, "diagnosis_s14.md"))
        # Baris petunjuk (`>`) dan baris tabel kosong tidak dihitung: yang dihitung isi tulisanmu.
        isi = _isi_nyata(dok)
        kalimat = [b for b in isi.splitlines() if len(b.strip()) > 40]
        baris_tabel = [b for b in dok.splitlines()
                       if b.strip().startswith("|") and len(re.findall(r"\w", b)) > 20
                       and not re.match(r"^\s*\|[\s|:-]+\|\s*$", b)]
        hasil.append(tunjukkan("ada baris diagnosis terisi (tabel atau kalimat)", len(baris_tabel) + len(kalimat) >= 3,
                               f"{len(baris_tabel)} baris tabel · {len(kalimat)} kalimat"))
        # Verdict-nya ditulis di dalam tabel, jadi pencariannya harus ikut baris tabel —
        # yang dibuang hanya baris petunjuk `>` dan judul, yang memang ada di templat.
        tanpa_petunjuk = "\n".join(b for b in dok.splitlines()
                                   if b.strip() and not b.strip().startswith((">", "#")))
        hasil.append(tunjukkan("menyebut jenis harinya (data / bisnis / kampanye)",
                               bool(re.search(r"anomali data|anomali bisnis|kampanye", tanpa_petunjuk, re.I))))
        con2, _, _ = buka_t4(topic)
        if con2 is not None and "pred_anomaly_daily" in _tabel(con2):
            n_nyala = _satu(con2, "SELECT count(DISTINCT tanggal) FROM pred_anomaly_daily WHERE anomaly_flag")
            con2.close()
            hasil.append(tunjukkan("jumlah kalimat sebanding dengan hari yang ditandai",
                                   len(baris_tabel) + len(kalimat) >= n_nyala,
                                   f"{len(baris_tabel) + len(kalimat)} kalimat untuk {n_nyala} hari",
                                   wajib=False))
    con.close()
    return hasil


def _isi_nyata(teks: str) -> str:
    """Teks yang benar-benar ditulis mahasiswa: tanpa judul, tanpa baris petunjuk `>`."""
    baris = [b for b in teks.splitlines()
             if b.strip() and not b.strip().startswith((">", "#", "|", "---"))]
    return "\n".join(baris)


def _bagian_insight(dok: str) -> dict[str, str]:
    """Pecah dokumen per judul jadi {nama bagian: isi nyata (tanpa petunjuk)}."""
    potongan = re.split(r"^#+\s*(Temuan|Bukti|Rekomendasi|Pemilik[^\n]*)\s*$", dok, flags=re.M | re.I)
    hasil = {}
    for i in range(1, len(potongan) - 1, 2):
        nama = potongan[i].strip().lower()
        hasil[nama.split()[0]] = _isi_nyata(potongan[i + 1])
    return hasil


def sesi15(topic: str, step: int) -> list[bool]:
    print(f"DoD Sesi 15 — langkah 4: insight dan pembekuan ({topic}) · step {step}")
    hasil: list[bool] = []
    dok = baca(os.path.join(config.DOCS, "insights_s15.md"))
    bagian = _bagian_insight(dok)
    hasil.append(tunjukkan("empat bagian ada (temuan, bukti, rekomendasi, pemilik)",
                           len(bagian) >= 4, f"{len(bagian)} bagian terbaca"))
    # Bagian yang dihitung hanya isi yang ditulis sendiri — baris petunjuk `>` tidak dihitung,
    # supaya berkas templat yang belum disentuh TIDAK lolos.
    kata_isi = {n: len(re.findall(r"\w+", t)) for n, t in bagian.items()}
    tipis = {n: k for n, k in kata_isi.items() if k < 20}
    hasil.append(tunjukkan("setiap bagian berisi (≥20 kata)", not tipis,
                           ", ".join(f"{n}={k} kata" for n, k in tipis.items()) or
                           " · ".join(f"{n}={k}" for n, k in kata_isi.items())))
    total = sum(kata_isi.values())
    hasil.append(tunjukkan("cukup pendek untuk dibaca satu menit (≤ 400 kata)", total <= 400, f"{total} kata"))
    hasil.append(tunjukkan("pemilik tindakan berupa jabatan, bukan tim",
                           bool(re.search(r"jabatan|head of|lead|manager|kepala",
                                          bagian.get("pemilik", ""), re.I)), "", wajib=False))
    hasil.append(tunjukkan("bukti menyebut tile atau tabelnya",
                           bool(re.search(r"v_kpi_monthly|pred_anomaly_daily|v_revenue_bridge|tile",
                                          bagian.get("bukti", ""), re.I)),
                           "sebut tile dan view di belakangnya"))
    hasil.append(tunjukkan("tidak ada bagian yang dibiarkan kosong", KOSONG not in dok))
    con, _, _ = buka_t4(topic)
    if con is not None:
        tabel = _tabel(con)
        hasil.append(tunjukkan("dashboard dibekukan di atas warehouse yang utuh",
                               all(t in tabel for t in ("v_kpi_monthly", "pred_anomaly_daily",
                                                        "v_revenue_bridge")), "", wajib=False))
        con.close()
    tanda = subprocess.run(["git", "tag", "--list", "s15-final"], cwd=config.ROOT,
                           capture_output=True, text=True).stdout.strip()
    hasil.append(tunjukkan("tag s15-final dibuat", bool(tanda),
                           "git tag s15-final && git push origin s15-final", wajib=False))
    return hasil


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["verify"])
    ap.add_argument("--sesi", required=True, choices=["4", "5", "8", "12", "13", "14", "15"])
    ap.add_argument("--topic", default=None, choices=sorted(config.TOPICS))
    ap.add_argument("--slice", default=None)
    ap.add_argument("--step", default=None,
                    help="Sesi 12–15: 1..4 (12, 13), 3a/3b/3c (14), 1 (15). Kosong = langkah terakhir.")
    args = ap.parse_args()

    topic = args.topic or ("t4" if args.sesi in SESI_T4 else "t2")
    slice_id = args.slice or (config.slice_ids(topic) or [None])[0]

    if args.sesi == "8":
        hasil = sesi8(topic)
    elif args.sesi == "4":
        hasil = sesi4(topic, slice_id)
    elif args.sesi == "5":
        hasil = sesi5(topic, slice_id)
    elif args.sesi == "12":
        hasil = sesi12(topic, int(args.step) if args.step else 4)
    elif args.sesi == "13":
        hasil = sesi13(topic, int(args.step) if args.step else 4)
    elif args.sesi == "14":
        hasil = sesi14(topic, args.step or "3a")
    else:
        hasil = sesi15(topic, int(args.step) if args.step else 1)

    lulus, total = sum(1 for h in hasil if h), len(hasil)
    print(f"\n{lulus}/{total} syarat terpenuhi")
    if args.sesi == "8" and lulus < total:
        print("Desain belum bisa dieksekusi orang lain. Perbaiki yang bertanda ✗ sebelum keluar ruangan.")
    if args.sesi in SESI_T4 and lulus < total:
        print("Belum hijau. Kalau waktunya habis: tarik tag aman langkah sebelumnya, tulis satu baris")
        print("apa yang kamu lewati, lalu lanjut ke langkah berikutnya. Jangan berhenti di sini.")
    sys.exit(0 if lulus == total else 1)


if __name__ == "__main__":
    main()
