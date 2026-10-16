"""D1 + UTS item 3 — profil sumber SEBELUM transformasi.

Enam query, tanpa kecerdikan: null, duplikat, rentang tidak wajar, nilai di luar domain,
kardinalitas, dan format tanggal/timestamp. Angka yang keluar di sini adalah angka yang dipakai
untuk menulis test ("expected: 4.712 baris duplikat").

Pakai:
    python -m pipeline.profile --topic t3 --slice k1
    python -m pipeline.profile --topic t2 --slice k8 --json > docs/profil.json
"""

from __future__ import annotations

import argparse
import json
import os
import textwrap

import duckdb

from pipeline import config

# {D} = folder seed slice ini. Kolom diambil apa adanya (semua VARCHAR) — tujuannya melihat
# kenyataan sumber, bukan kenyataan yang rapi.
QUERIES: dict[str, list[tuple[str, str]]] = {
    "t1": [
        ("mahasiswa", "SELECT count(*) AS baris, count(DISTINCT nim) AS nim_unik FROM read_csv_auto('{D}/mahasiswa.csv', all_varchar=true)"),
        ("mahasiswa", "SELECT count(*) AS nim_duplikat FROM (SELECT nim FROM read_csv_auto('{D}/mahasiswa.csv', all_varchar=true) GROUP BY 1 HAVING count(*) > 1)"),
        ("mahasiswa", "SELECT count(*) FILTER (WHERE angkatan IS NULL OR angkatan='') AS angkatan_kosong, count(DISTINCT status) AS varian_status FROM read_csv_auto('{D}/mahasiswa.csv', all_varchar=true)"),
        ("presensi", "SELECT count(*) AS baris, count(*) FILTER (WHERE nim IS NULL) AS nim_null FROM read_csv_auto('{D}/presensi.csv', all_varchar=true)"),
        ("presensi", "SELECT count(*) AS duplikat_grain FROM (SELECT nim, kode_mk, tanggal FROM read_csv_auto('{D}/presensi.csv', all_varchar=true) GROUP BY 1,2,3 HAVING count(*) > 1)"),
        ("presensi", "SELECT count(*) FILTER (WHERE tanggal LIKE '__/__/____') AS tanggal_format_lain, count(DISTINCT status) AS varian_status FROM read_csv_auto('{D}/presensi.csv', all_varchar=true)"),
        ("nilai", "SELECT count(*) FILTER (WHERE TRY_CAST(nilai_angka AS INT) > 100 OR TRY_CAST(nilai_angka AS INT) < 0) AS nilai_luar_rentang FROM read_csv_auto('{D}/nilai.csv', all_varchar=true)"),
    ],
    "t2": [
        ("transactions", "SELECT count(*) AS baris, count(DISTINCT transaction_id) AS id_unik FROM read_csv_auto('{D}/transactions.csv', all_varchar=true)"),
        ("transactions", "SELECT count(*) AS id_duplikat FROM (SELECT transaction_id FROM read_csv_auto('{D}/transactions.csv', all_varchar=true) GROUP BY 1 HAVING count(*) > 1)"),
        ("transactions", "SELECT count(*) FILTER (WHERE tanggal_waktu LIKE '%Z') AS timestamp_utc, count(DISTINCT status) AS varian_status FROM read_csv_auto('{D}/transactions.csv', all_varchar=true)"),
        ("transactions", "SELECT count(*) AS tanpa_item FROM read_csv_auto('{D}/transactions.csv', all_varchar=true) t WHERE NOT EXISTS (SELECT 1 FROM read_csv_auto('{D}/transaction_items.csv', all_varchar=true) i WHERE i.transaction_id = t.transaction_id)"),
        ("transaction_items", "SELECT count(*) FILTER (WHERE TRY_CAST(qty AS INT) < 0) AS qty_negatif, count(*) AS baris FROM read_csv_auto('{D}/transaction_items.csv', all_varchar=true)"),
        ("transaction_items", "SELECT count(*) AS fk_orphan FROM read_csv_auto('{D}/transaction_items.csv', all_varchar=true) i WHERE NOT EXISTS (SELECT 1 FROM read_csv_auto('{D}/products.csv', all_varchar=true) p WHERE p.product_id = i.product_id)"),
        ("products", "SELECT count(DISTINCT harga_satuan) AS varian_harga, count(*) AS produk FROM read_csv_auto('{D}/products.csv', all_varchar=true)"),
    ],
    "t3": [
        ("prakiraan_cuaca", "SELECT count(*) AS baris, count(DISTINCT adm4) AS desa FROM read_csv_auto('{D}/prakiraan_cuaca.csv', all_varchar=true)"),
        ("prakiraan_cuaca", "SELECT count(*) FILTER (WHERE vs IS NULL OR vs = '') AS vs_kosong FROM read_csv_auto('{D}/prakiraan_cuaca.csv', all_varchar=true)"),
        ("prakiraan_cuaca", "SELECT count(*) FILTER (WHERE TRY_CAST(tp AS DOUBLE) = 0) AS tp_nol, count(*) AS baris FROM read_csv_auto('{D}/prakiraan_cuaca.csv', all_varchar=true)"),
        ("prakiraan_cuaca", "SELECT weather AS kode, weather_desc AS deskripsi, count(*) AS baris FROM read_csv_auto('{D}/prakiraan_cuaca.csv', all_varchar=true) GROUP BY 1,2 ORDER BY 3 DESC"),
        ("prakiraan_cuaca", "SELECT min(TRY_CAST(time_index AS VARCHAR)) AS time_index_contoh, count(DISTINCT analysis_date) AS analysis_date_unik FROM read_csv_auto('{D}/prakiraan_cuaca.csv', all_varchar=true)"),
        ("prakiraan_cuaca", "SELECT count(*) FILTER (WHERE epoch(strptime(local_datetime, '%Y-%m-%d %H:%M:%S')) - epoch(strptime(utc_datetime, '%Y-%m-%d %H:%M:%S')) = 25200) AS baris_selisih_7jam, count(*) AS baris FROM read_csv_auto('{D}/prakiraan_cuaca.csv', all_varchar=true)"),
        ("desa", "SELECT count(*) AS desa, count(DISTINCT kecamatan) AS kecamatan FROM read_csv_auto('{D}/desa.csv', all_varchar=true)"),
    ],
    # T4 (Sesi 12–15) — delapan berkas, satu dataset penuh. Lima temuan wajib malam itu ada di sini:
    # waktu (UTC vs WIB), identitas (email dipakai dua customer_id), duplikat, yatim, dan qty negatif.
    "t4": [
        ("orders", "SELECT count(*) AS baris, count(DISTINCT order_id) AS id_unik FROM read_csv_auto('{D}/orders.csv', all_varchar=true)"),
        ("orders", "SELECT count(*) AS id_duplikat FROM (SELECT order_id FROM read_csv_auto('{D}/orders.csv', all_varchar=true) GROUP BY 1 HAVING count(*) > 1)"),
        ("orders", "SELECT count(*) FILTER (WHERE order_ts LIKE '%Z') AS timestamp_utc, count(*) FILTER (WHERE order_ts NOT LIKE '%Z') AS timestamp_wib, count(DISTINCT status) AS varian_status FROM read_csv_auto('{D}/orders.csv', all_varchar=true)"),
        ("orders", "SELECT store_id, substr(order_ts, 1, 10) AS tanggal, count(*) AS baris, count(DISTINCT order_id) AS order_unik, count(*) - count(DISTINCT order_id) AS kelebihan FROM read_csv_auto('{D}/orders.csv', all_varchar=true) WHERE store_id <> '' GROUP BY 1, 2 HAVING count(*) > count(DISTINCT order_id) ORDER BY kelebihan DESC, baris DESC LIMIT 5"),
        ("order_items", "SELECT count(*) FILTER (WHERE TRY_CAST(qty AS INTEGER) < 0) AS qty_negatif, count(*) AS baris FROM read_csv_auto('{D}/order_items.csv', all_varchar=true)"),
        ("order_items", "SELECT count(*) AS fk_yatim FROM read_csv_auto('{D}/order_items.csv', all_varchar=true) i WHERE NOT EXISTS (SELECT 1 FROM read_csv_auto('{D}/orders.csv', all_varchar=true) o WHERE o.order_id = i.order_id)"),
        ("customers", "SELECT count(*) AS email_dipakai_dua_id FROM (SELECT email FROM read_csv_auto('{D}/customers.csv', all_varchar=true) WHERE email <> '' GROUP BY 1 HAVING count(DISTINCT customer_id) > 1)"),
        ("customers", "SELECT count(*) FILTER (WHERE handle IS NULL OR handle = '') AS handle_kosong, count(DISTINCT wilayah) AS varian_wilayah FROM read_csv_auto('{D}/customers.csv', all_varchar=true)"),
        ("targets", "SELECT count(*) FILTER (WHERE target_revenue IS NULL OR target_revenue = '') AS target_kosong, count(*) AS baris FROM read_csv_auto('{D}/targets.csv', all_varchar=true)"),
        ("stores", "SELECT count(*) FILTER (WHERE upper(aktif) <> 'YA') AS toko_tutup, count(DISTINCT wilayah) AS varian_wilayah FROM read_csv_auto('{D}/stores.csv', all_varchar=true)"),
        ("products", "SELECT count(*) AS baris, count(DISTINCT product_id) AS produk_unik, count(*) - count(DISTINCT product_id) AS versi_harga_ekstra FROM read_csv_auto('{D}/products.csv', all_varchar=true)"),
        ("returns", "SELECT count(*) AS baris, count(DISTINCT reason) AS varian_alasan, count(DISTINCT return_channel) AS varian_channel FROM read_csv_auto('{D}/returns.csv', all_varchar=true)"),
    ],
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True, choices=sorted(config.TOPICS))
    ap.add_argument("--slice", default=None,
                    help="wajib untuk T1–T3; T4 tidak punya slice (satu dataset untuk semua tim)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    # T1–T3: kalau --slice tidak disebut, pakai slice pertama seperti checkpoint.py.
    slice_id = args.slice or (config.slice_ids(args.topic) or [None])[0]
    ctx = config.resolve(args.topic, slice_id)
    suffix = f"_{slice_id}" if slice_id else ""
    con = duckdb.connect()
    out = []
    for tabel, sql in QUERIES[args.topic]:
        rows = con.execute(sql.format(D=ctx["dir"])).fetchall()
        cols = [d[0] for d in con.description]
        out.append({"tabel": tabel, "query": sql, "kolom": cols, "hasil": [list(map(str, r)) for r in rows]})

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    judul = f"# Profil {ctx['cfg']['label']} — slice {slice_id} ({ctx['label']})\n" if slice_id \
        else f"# Profil {ctx['cfg']['label']} — dataset penuh\n"
    print(judul)
    for blok in out:
        print(f"## {blok['tabel']}")
        print("   " + textwrap.shorten(blok["query"], 160, placeholder=" …"))
        for r in blok["hasil"]:
            print("   " + " | ".join(f"{c}={v}" for c, v in zip(blok["kolom"], r)))
        print()
    os.makedirs(config.DOCS, exist_ok=True)
    dest = os.path.join(config.DOCS, f"profile_{args.topic}{suffix}.md")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(f"# Profil sumber — {ctx['cfg']['label']}" + (f" / {slice_id}\n\n" if slice_id else "\n\n"))
        for blok in out:
            fh.write(f"## {blok['tabel']}\n\n`{blok['query']}`\n\n")
            fh.write("| " + " | ".join(blok["kolom"]) + " |\n")
            fh.write("|" + "---|" * len(blok["kolom"]) + "\n")
            for r in blok["hasil"]:
                fh.write("| " + " | ".join(r) + " |\n")
            fh.write("\n")
    print(f"[profile] ditulis: {dest}")


if __name__ == "__main__":
    main()
