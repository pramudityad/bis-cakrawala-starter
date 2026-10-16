# data/raw/ — seed (jangan diubah)

Diisi dosen, dibaca saja. Salin dari folder seed kelas:

```bash
cp -R <seed-kelas>/t1_kampus  data/raw/
cp -R <seed-kelas>/t2_umkm    data/raw/
cp -R <seed-kelas>/t3_publik  data/raw/
cp -R <seed-kelas>/t4_omni    data/raw/      # Sesi 12–15
```

T3 hanya butuh foldernya sendiri (tiap slice ada di dalam `t3_publik/<kode-tim>/`), dan setiap
folder T3 menyertakan `SOURCE.md` — sumber, tanggal snapshot, jumlah baris. Itu syarat data publik:
tanpa SOURCE.md, angkanya tidak bisa diperiksa siapa pun.

## T4 — Ritel Omnichannel (Sesi 12–15)

Delapan berkas, satu dataset untuk seluruh kelas (tidak ada slice): `stores`, `products`,
`customers`, `orders`, `order_items`, `returns`, `targets`, `marketing_spend`.

Datanya **sengaja kotor** dan sudah disuntik beberapa kejadian. Baca soal itu di Sesi 12; yang
perlu kamu ingat sebelum menyentuhnya: profil dulu, jangan percaya satu angka pun yang belum
kamu lihat sendiri. Kunci penyuntikannya milik dosen dan tidak ada di repo ini.
