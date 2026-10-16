"""D3 — load idempoten: satu dimensi + satu fact, dijalankan dua kali tanpa menggandakan baris.

Dua mode:

    full        CREATE OR REPLACE TABLE  (idempoten secara konstruksi — acuan repo ini)
    insert_only INSERT polos pada run kedua — MENGGANDAKAN baris. Hanya untuk demonstrasi Sesi 4.

Strategi lain (upsert lewat natural key, DELETE partisi + INSERT) **ditulis tim sendiri** di
`pipeline/DESIGN_load.md` dan di SQL mereka — repo ini tidak menyediakan flag untuk itu, karena
memilihnya adalah bagian dari penilaian, bukan pengaturan.

Berkas SQL boleh menyusun urutan eksekusi lewat include, jadi skeleton tetap terpisah per langkah
Sesi 12–15 tanpa perlu menyalin-tempel:

    SOURCE sql/00_stg_orders.sql;
    SOURCE sql/20_dim_channel.sql;

DuckDB Python tidak bisa mengeksekusi `SOURCE` (itu perintah CLI), jadi loader ini yang membacanya
dan menyisipkan isi berkasnya. Include bersarang diizinkan; include berputar ditolak.

Pakai:
    python -m pipeline.load --topic t2 --slice k8 --twice
    python -m pipeline.load --topic t4 --twice              # T4 tanpa slice (Sesi 12–15)
    python -m pipeline.load --topic t2 --slice k8 --strategy insert_only --twice   # demo jebol
    python -m pipeline.load --topic t1 --slice k4 --fallback                       # tulis warehouse/fallback/

Setiap run menulis `warehouse/<db>.load.json` berisi jumlah baris run-1 (dan run-2): itulah bukti
`--twice` yang dibaca `checkpoint.py`, bukan lagi dipercaya dari layar.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import time

import duckdb

from pipeline import config

# `SOURCE sql/x.sql;` (gaya CLI DuckDB) atau `-- include: sql/x.sql`.
# Komentar di ujung baris diizinkan — `SOURCE sql/x.sql;   -- DIBERIKAN` itu wajar ditulis orang,
# dan kalau tidak diizinkan barisnya lolos ke DuckDB lalu meledak sebagai Parser Error.
INCLUDE_RE = re.compile(
    r"^[ \t]*(?:SOURCE|\.read|--[ \t]*include:)[ \t]+(\S+?)[ \t]*;?[ \t]*(?:--[^\n]*)?$",
    re.I | re.M)


def render(sql: str, ctx: dict) -> str:
    """Isi {D} (folder seed) dan {SLICE_<nama>} (predikat slice, TRUE kalau tidak dipakai)."""
    where = {}
    if ctx["slice"]:
        where = ctx["cfg"].get("slices", {}).get(ctx["slice"], {}).get("where", {})
    sql = sql.replace("{D}", ctx["dir"])
    for key in re.findall(r"\{SLICE_([a-z_]+)\}", sql):
        sql = sql.replace(f"{{SLICE_{key}}}", where.get(key, "TRUE"))
    return sql


def expand(sql: str, ctx: dict, seen: list[str]) -> str:
    """Ganti tiap baris include dengan isi berkasnya, rekursif. `seen` menolak include berputar."""
    def satu(m: re.Match) -> str:
        rel = m.group(1).strip("'\"")
        path = rel if os.path.isabs(rel) else os.path.join(config.ROOT, rel)
        if path in seen:
            raise SystemExit(f"include berputar: {rel} (sudah dibaca dari {seen[0]})")
        if not os.path.exists(path):
            raise SystemExit(f"include tidak ditemukan: {rel}")
        seen.append(path)
        return "\n" + expand(render(open(path, encoding="utf-8").read(), ctx), ctx, seen) + "\n"

    return INCLUDE_RE.sub(satu, sql)


def tanpa_komentar(sql: str) -> str:
    """Buang komentar `--` (di luar string literal).

    Ini bukan kerapian: pemisah pernyataan di repo ini `;`, jadi satu titik koma di dalam komentar
    — kalimat biasa seperti "catat; lanjut" — akan memotong pernyataan di tengah dan muncul sebagai
    Parser Error yang membingungkan. Lebih baik dijinakkan di sini sekali.
    """
    keluar, i, n, dalam_string = [], 0, len(sql), False
    while i < n:
        ch = sql[i]
        if dalam_string:
            keluar.append(ch)
            if ch == "'":
                dalam_string = False
            i += 1
        elif ch == "'":
            dalam_string = True
            keluar.append(ch)
            i += 1
        elif ch == "-" and i + 1 < n and sql[i + 1] == "-":
            while i < n and sql[i] != "\n":
                i += 1
            keluar.append("\n")
        else:
            keluar.append(ch)
            i += 1
    return "".join(keluar)


def berkas_sql(topic: str, diminta: str = None) -> str:
    """SQL topik: `sql/load_<topik>.sql` kalau ada, kalau tidak `sql/load.sql` (acuan lama)."""
    if diminta:
        return diminta
    khusus = os.path.join(config.SQL, f"load_{topic}.sql")
    return khusus if os.path.exists(khusus) else os.path.join(config.SQL, "load.sql")


def statements(sql: str) -> list[str]:
    """Pernyataan di antara `;`, setelah komentar dibuang."""
    return [s.strip() for s in tanpa_komentar(sql).split(";") if s.strip()]


def counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    tabel = [r[0] for r in con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='main' ORDER BY 1").fetchall()]
    return {t: con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] for t in tabel}


def run_once(con: duckdb.DuckDBPyConnection, stmts: list[str], strategy: str, sudah_ada: bool) -> None:
    """strategi `full`   = CREATE OR REPLACE (idempoten secara konstruksi)
       strategi `insert_only` = CREATE pada run-1, INSERT polos pada run-2 (contoh yang sengaja jebol)."""
    for stmt in stmts:
        if strategy == "insert_only" and sudah_ada and re.match(r"CREATE OR REPLACE TABLE \w+ AS", stmt, re.I):
            stmt = re.sub(r"^CREATE OR REPLACE TABLE", "INSERT INTO", stmt, flags=re.I)
        con.execute(stmt)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True, choices=sorted(config.TOPICS))
    ap.add_argument("--slice", default=None,
                    help="wajib untuk T1–T3; T4 tidak punya slice")
    ap.add_argument("--strategy", default="full", choices=["full", "insert_only"],
                    help="full = idempoten; insert_only = contoh yang sengaja menggandakan baris")
    ap.add_argument("--twice", action="store_true", help="jalankan dua kali lalu bandingkan row count")
    ap.add_argument("--sql", default=None,
                    help="berkas SQL tim (default: sql/load_<topik>.sql, kalau tidak ada sql/load.sql)")
    ap.add_argument("--fallback", action="store_true", help="tulis ke warehouse/fallback/ (jalur penyelamat)")
    args = ap.parse_args()

    slice_id = args.slice or (config.slice_ids(args.topic) or [None])[0]
    ctx = config.resolve(args.topic, slice_id)
    path = berkas_sql(args.topic, args.sql)
    if not os.path.exists(path):
        raise SystemExit(f"SQL tidak ditemukan: {path}")

    # Semua include disisipkan lebih dulu, lalu gerbang TODO diperiksa pada hasil gabungan —
    # jadi satu TODO di skeleton mana pun menahan seluruh load, bukan cuma di berkas urutan.
    dibaca = [os.path.abspath(path)]
    isi = expand(render(open(path, encoding="utf-8").read(), ctx), ctx, dibaca)
    if "TODO" in isi:
        raise SystemExit(
            f"{os.path.relpath(path, config.ROOT)} masih punya bagian bertanda TODO.\n"
            f"Tulis dulu bagian itu (staging, DDL dimensi/fact, atau pred_anomaly_daily), lalu\n"
            f"jalankan lagi. Berkas yang ikut terbaca:\n"
            + "\n".join(f"  - {os.path.relpath(p, config.ROOT)}" for p in dibaca))
    stmts = statements(isi)

    nama = f"{args.topic}_{slice_id}" if slice_id else args.topic
    if args.fallback:
        dest = os.path.join(config.WAREHOUSE, "fallback")
        os.makedirs(dest, exist_ok=True)
        db = os.path.join(dest, f"{nama}.duckdb")
    else:
        db = config.db_path(args.topic, slice_id)

    con = duckdb.connect(db)
    print(f"[load] {ctx['cfg']['label']}" + (f" · slice {slice_id} ({ctx['label']})" if slice_id else "")
          )
    print(f"[load] sql={os.path.relpath(path, config.ROOT)} · strategi={args.strategy} · db={os.path.relpath(db, config.ROOT)}")

    t0 = time.time()
    run_once(con, stmts, args.strategy, sudah_ada=False)
    c1 = counts(con)
    print(f"[load] run-1 {time.time() - t0:.2f}s → " + " · ".join(f"{k}={v:,}" for k, v in c1.items()))

    c2, beda = None, {}
    if args.twice:
        t1 = time.time()
        run_once(con, stmts, args.strategy, sudah_ada=True)
        c2 = counts(con)
        beda = {k: (c1[k], c2.get(k)) for k in c1 if c1[k] != c2.get(k)}
        print(f"[load] run-2 {time.time() - t1:.2f}s → " + " · ".join(f"{k}={v:,}" for k, v in c2.items()))
        if beda:
            print("[load] ✗ TIDAK IDEMPOTEN — " + " · ".join(f"{k}: {a:,} → {b:,}" for k, (a, b) in beda.items()))
            print("[load]   penyebab paling umum: INSERT tanpa klausa kunci, atau grain fact yang tidak unik")
        else:
            print("[load] ✓ IDEMPOTEN — row count run-1 == run-2")
    con.close()

    # Bukti yang bisa diperiksa mesin (checkpoint Sesi 12–15 membaca berkas ini).
    catat = {"topic": args.topic, "slice": slice_id, "sql": os.path.relpath(path, config.ROOT),
             "db": os.path.relpath(db, config.ROOT), "strategy": args.strategy,
             "run1": c1, "run2": c2, "idempoten": (not beda) if c2 is not None else None,
             "dijalankan_pada": dt.datetime.now().isoformat(timespec="seconds")}
    with open(db[: -len(".duckdb")] + ".load.json", "w", encoding="utf-8") as fh:
        json.dump(catat, fh, indent=2, ensure_ascii=False)
    if c2 is None:
        print("[load] catatan: jalankan dengan --twice supaya bukti idempotensi tersimpan")


if __name__ == "__main__":
    main()
