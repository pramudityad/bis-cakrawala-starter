# Profil T4 — lima temuan (D11, langkah 1a)

Hasil `python -m pipeline.profile --topic t4`, lalu dibaca dan diberi arti. Aturan malam itu:
temuan tanpa angka hanyalah pendapat.

| # | Temuan | Angka | Tabel | Kenapa penting |
|---|---|---|---|---|
| 1 | Waktu bercampur: sebagian baris bertanda UTC, sisanya WIB | 9,903 baris bertanda `Z` dari 65,756 | `orders` | satu hari bergeser 7 jam; total harian dan penanda anomali ikut salah |
| 2 | Satu ide status ditulis lima cara (plus tiga status lain) | 8 nilai berbeda | `orders` | KPI per status pecah, angka gabungan menipu |
| 3 | `order_id` kembar | 317 baris kelebihan | `orders` | omzet channel itu dihitung dua kali |
| 4 | Satu toko mengirim batch POS-nya dua kali | STR-14 2025-05-27: 34 baris untuk 17 pesanan | `orders` | anomali **data**, bukan bisnis — kejadiannya sekali, tercatat dua kali |
| 5 | Item tanpa order induk | 200 baris | `order_items` | join ke fact menggagalkan baris itu tanpa pesan error; omzet hilang diam-diam |
| 6 | Identitas ganda lintas channel: satu email dipakai dua `customer_id` | 20 email, 0 pelanggan tanpa handle | `customers` | satu orang terpecah dua; resolusi identitas jadi syarat |

## Bintang satu temuan

**Yang dibintangi: temuan nomor 4** (batch POS dua kali).

**Alasannya:** inilah yang paling dulu dirasakan Head of Omnichannel Retail. Temuan 1–3 dan 5–6
menggeser angka sedikit di banyak tempat; temuan 4 menggandakan omzet satu gerai pada satu hari
sekaligus, dan kalau tidak dibereskan channel STORE terlihat lebih baik daripada kenyataannya.
