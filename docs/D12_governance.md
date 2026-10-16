# D12 — Lampiran tata kelola (9 bagian)

> UAS. Setiap bagian minimal dua kalimat. Kalau satu bagian kosong, dashboard-nya belum boleh
> dipakai orang lain.
>
> Enam bagian pertama dipakai sejak UTS. Tiga bagian terakhir (7–9) lahir dari tabel target dan
> dari identitas lintas channel yang muncul di Sesi 12–13. Isi singkat tidak apa-apa; yang penting
> jawabannya bisa dipertahankan, bukan panjangnya.

1. **Pemilik data** — siapa yang bertanggung jawab atas isi dan kualitasnya (jabatan, bukan tim).
2. **Klasifikasi PII** — kolom mana yang PII, mana yang tidak, dan dasarnya (UU PDP No 27/2022).
3. **Hak akses** — siapa boleh melihat apa; sebutkan aturan row-level kalau ada (mis. per outlet).
4. **Lineage** — dari tabel sumber mana angka di dashboard berasal, sampai kolomnya.
5. **Retensi** — berapa lama disimpan dan apa yang dihapus lebih dulu.
   Ingat: dimensi pelangganmu menyimpan setiap versi (Type 2). Perintah DELETE hari ini tidak
   menghapus versi kemarin. Tulis bagaimana permintaan penghapusan benar-benar dijalankan.
6. **Penghentian** — kalau layanan ini dimatikan, apa yang terjadi pada datanya dan siapa yang diberi tahu.

7. **Pemilik target** — jabatan yang menetapkan target, periode berlakunya, dan siapa yang boleh merevisinya.
   Satu angka tanpa pemilik tidak bisa dipertanggungjawabkan. Jabatan bernama, bukan "tim data".

8. **Identitas lintas channel** — orang yang sama datang sebagai `loyalty_id` di toko, email di web/app,
   dan `handle` di marketplace. Tulis kolom PII mana yang kamu ingesti ke lapisan BI, mana yang tidak,
   dan bagaimana kamu menyatukannya tanpa menyimpan lebih banyak daripada yang dibutuhkan.
   **Tandai tegas minimal satu kolom dengan kalimat "tidak di-ingest"** — kolom yang datanya tidak
   dibutuhkan dashboard sama sekali, jadi lebih baik tidak pernah masuk.

9. **Matriks akses** — peran × channel × wilayah. Satu baris per peran; sel berisi baca atau tulis.
   Contoh bentuk (lengkapi barismu sendiri):

   | Peran | channel | wilayah | Akses |
   |---|---|---|---|
   | Analis wilayah | semua | satu wilayah saja | baca |
   | Retail Planning Lead | STORE, WEB, APP, MARKETPLACE | semua | baca |
   | (jabatan pilihanmu) |  |  |  |

## Khusus data publik (tim T3)
Satu paragraf: lisensi sumber, tanggal snapshot, dan apa yang boleh serta tidak boleh diklaim dari
data prakiraan. (Tim T4 boleh menulis "tidak berlaku — data sintetis buatan dosen".)
