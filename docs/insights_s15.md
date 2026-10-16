# Insight dan rekomendasi — langkah 4 (Sesi 15)

## Temuan

Channel yang membuat target kuartal ini meleset adalah **WEB**: capaiannya sekitar 88% dari target,
sementara tiga channel lain berada di 99–104%. Melesetnya bukan efek satu bulan, tapi melebar sejak
kuartal ketiga, tepat setelah kanal web berhenti beberapa hari di Agustus.

## Bukti

Tile "target vs aktual" di atas `v_kpi_monthly`: baris WEB kuartal ketiga menunjukkan capaian 88,0%,
turun dari 102% di kuartal pertama. Tile tren di view yang sama menunjukkan volume pesanan WEB
menurun sementara APP naik. Verdict anomali ada di `pred_anomaly_daily`: 12–14 Agustus ditandai
penuh. Penyebabnya dari `v_revenue_bridge`: efek volume mendominasi, harga rata-rata nyaris tidak
bergerak.

## Rekomendasi

Hentikan promosi berbayar di channel WEB untuk sementara dan pindahkan anggarannya ke APP, sambil
memasang pemantauan ketersediaan pembayaran yang menyala kalau volume kanal turun di bawah separuh
rata-rata 28 hari. Satu tindakan, bukan daftar keinginan.

## Pemilik tindakan

Head of Omnichannel Retail memutuskan perpindahan anggaran, dan Retail Planning Lead merevisi target
WEB kuartal berikutnya paling lambat dua minggu setelah keputusan itu. Pemantauannya dipasang Head of
Digital Operations sebelum promosi berikutnya dimulai.
