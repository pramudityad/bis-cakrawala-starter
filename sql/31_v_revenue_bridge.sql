-- ============================================================
-- 31_v_revenue_bridge.sql — Sesi 14, langkah 3b. Bagianmu.
--
-- Mengeser "targetnya meleset" jadi "kenapa meleset". Selisih omzet dipecah jadi tiga sebab:
--
--     volume_effect : jumlah unit berubah, harga tetap
--     price_effect  : harga berubah, jumlah unit tetap
--     mix_effect    : komposisi produk berubah (yang mahal laku lebih sedikit daripada yang murah)
--
-- Ketiganya harus berjumlah tepat sama dengan selisih omzet yang dijelaskan. Kalau tidak jumlahnya
-- pas, bukan berarti "hampir benar" — artinya salah satu efeknya salah hitung.
--
-- Kolomnya sudah ditetapkan dan tidak boleh ditambah:
--     v_revenue_bridge(bulan, channel, volume_effect, price_effect, mix_effect)
-- Grain: satu baris = satu bulan, satu channel (wilayah dijumlahkan).
--
-- SATU KEPUTUSAN YANG HARUS DIAMBIL SEBELUM MENULIS (dan ini pertanyaan dosen di kelas):
--   pembandingnya bulan sebelumnya atau bulan yang sama tahun lalu? Untuk dataset ini yang
--   tersedia hanya Jan–Des 2025, jadi bulan sebelumnya untuk Feb–Des, dan baris Januari tidak punya
--   pembanding. Buat keputusanmu, tulis di bawah, dan pakai konsisten.
--
-- TODO: tulis view-nya, tulis keputusan pembandingmu, lalu HAPUS kata TODO ini.
--       Pembanding: ______________________________________________________
SELECT
    CAST(NULL AS VARCHAR) AS bulan, CAST(NULL AS VARCHAR) AS channel,
    CAST(NULL AS DOUBLE) AS volume_effect, CAST(NULL AS DOUBLE) AS price_effect,
    CAST(NULL AS DOUBLE) AS mix_effect
WHERE FALSE;

-- Bukti yang harus hijau di Cek 3b: jumlah tiga efek = selisih omzet bulan itu vs pembandingnya.
