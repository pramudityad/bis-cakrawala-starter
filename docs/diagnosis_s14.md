# Diagnosis Sesi 14 — satu kalimat per hari yang ditandai

> Setiap tanggal yang penandanya menyala di `pred_anomaly_daily` harus punya satu kalimat.
> Kalimatnya menjawab satu hal: hari itu **jenis apa**.
>
>   - **anomali data** — pencatatannya yang salah (mis. satu toko mengirim batch POS dua kali)
>   - **anomali bisnis** — kejadiannya nyata (mis. kanal web berhenti sekitar tiga hari)
>   - **kampanye** — memang direncanakan; cek `marketing_spend.csv` dan kalender kampanye
>
> Penanda yang menyala di tanggal kampanye tidak salah. Yang salah adalah menghapusnya tanpa
> penjelasan. Tanggal yang tidak bisa kamu jelaskan adalah temuan paling jujur malam itu — tulis
> apa adanya, jangan dipaksakan.

| Tanggal | Channel | Jenis | Kalimat diagnosis | Bukti (SQL/kolom) |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## Faktor di balik selisih

Tulis satu paragraf: dari `v_revenue_bridge`, selisih bulan mana yang paling besar, dan efek mana
(volume, harga, mix) yang menjelaskannya.
