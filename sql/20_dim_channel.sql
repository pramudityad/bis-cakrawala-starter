-- ============================================================
-- 20_dim_channel.sql — Sesi 12, langkah 1c. DIBERIKAN (1 dari 5 dimensi).
--
-- Empat channel dataset T4, plus satu anggota Unknown. Dimensi sekecil ini tetap dibuat karena
-- `channel` muncul di semua pertanyaan proyek: "channel mana yang membuat target meleset?".
-- Grain: satu baris = satu channel.
-- ============================================================

CREATE OR REPLACE TABLE dim_channel AS
SELECT * FROM (VALUES
    (1, 'STORE',       'Toko fisik'),
    (2, 'WEB',         'Situs web'),
    (3, 'APP',         'Aplikasi mobile'),
    (4, 'MARKETPLACE', 'Marketplace pihak ketiga')
) AS t(channel_sk, channel, label)
UNION ALL
SELECT -1, 'TIDAK DIKETAHUI', 'TIDAK DIKETAHUI';
