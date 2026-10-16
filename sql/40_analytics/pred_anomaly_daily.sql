-- ============================================================
-- 40_analytics/pred_anomaly_daily.sql — Sesi 12, langkah 1d. Bagianmu.
--
-- Sebuah prediksi adalah DATA. Karena itu ia punya grain, versi, waktu penskoran, dan test —
-- sama seperti tabel lain di warehouse ini. Kolomnya sudah ditetapkan dan tidak boleh ditambah:
--     pred_anomaly_daily(tanggal, channel, revenue, zscore, anomaly_flag, model_version, scored_at)
--
-- Bagian yang sudah ditulis: omzet harian per channel (itu "apa yang terjadi").
-- Bagianmu: rerata bergulir 28 hari, simpangan, z-score, dan ambangnya.
--
-- SATU HAL YANG TIDAK BOLEH SALAH MALAM INI:
--   jendela 28 hari TIDAK memuat hari yang sedang dinilai.
--   Kalau hari yang dinilai ikut masuk, hari yang aneh ikut menarik rerata dan simpangannya,
--   sehingga z-nya mengecil — dan penandanya menyala setiap hari, atau tidak pernah menyala.
--   Pegang ini: rerata dan simpangan harus dihitung dari data SEBELUM hari itu.
--
-- Ambangnya kamu pilih sendiri dari grafikmu, dan tulis alasannya satu baris.
-- Ingat: kalender kampanye (11.11 dan 12.12) ada di `marketing_spend.csv`. Penanda yang menyala
-- di tanggal kampanye tidak salah — yang salah adalah menghapusnya tanpa penjelasan.
--
-- TODO: hitung rerata + simpangan bergulir 28 hari per channel, lalu zscore dan anomaly_flag.
--       Pilih ambang + tulis alasanmu, lalu HAPUS kata TODO ini supaya loader boleh jalan.
--       Alasan ambang: ______________________________________________________
CREATE OR REPLACE TABLE pred_anomaly_daily AS
WITH harian AS (
    SELECT
        CAST(f.order_ts AS DATE) AS tanggal,
        c.channel                AS channel,
        sum(f.neto)              AS revenue
    FROM fact_order_line f
    JOIN dim_channel c ON c.channel_sk = f.channel_sk
    GROUP BY 1, 2
)
SELECT
    tanggal,
    channel,
    revenue,
    CAST(NULL AS DOUBLE) AS zscore,
    FALSE                AS anomaly_flag,
    'z28-v1'             AS model_version,
    now()                AS scored_at
FROM harian;

-- Bukti yang harus hijau di Cek 1d:
--   SELECT count(*) FILTER (WHERE zscore IS NULL) FROM pred_anomaly_daily;   -- harus 0
--   SELECT channel, count(*) FROM pred_anomaly_daily GROUP BY 1;             -- 337 per channel
--   SELECT count(*) FILTER (WHERE anomaly_flag) FROM pred_anomaly_daily;     -- bukan 0, bukan semua
--   SELECT tanggal FROM pred_anomaly_daily WHERE anomaly_flag ORDER BY 1;    -- kamu harus bisa
--                                                                            -- menjelaskan tiap tanggal
--
-- Catatan soal 337: setahun ada 365 hari, dan 28 hari pertama tiap channel tidak punya riwayat
-- penuh untuk dijadikan pembanding. Hari seperti itu jangan diskor dengan jendela kosong — buang
-- (lalu baris pertama tabelmu 29 Januari), atau biarkan dan jelaskan. Kalau kamu biarkan dengan
-- jendela 1–2 hari, penandanya akan menyala di hari-hari awal Januari yang sebenarnya biasa saja.
