# WattWise Home

Aplikasi terminal (CLI) berbahasa Python untuk mencatat perangkat elektronik rumah tangga, menyimulasikan beban listrik 24 jam, menghitung pemborosan daya standby, dan memperkirakan pengeluaran serta sisa token PLN.

Dibuat sebagai proyek akhir Praktikum Dasar Pemrograman menggunakan Python Standard Library tanpa library eksternal.

## Fitur Utama

1. Manajemen perangkat elektronik (CRUD) dengan deteksi duplikat, filter ruangan, ringkasan perubahan sebelum simpan, dan pencatatan log aktivitas ke `log_aktivitas.txt`.
2. Pencarian dan pengurutan data secara manual: linear search, recursive binary search berdasarkan ID, bubble sort, insertion sort, selection sort, serta operasi himpunan (intersection, union, difference).
3. Simulasi beban listrik 24 jam dalam bentuk grafik batang ASCII, lengkap dengan deteksi jam overload dan rekomendasi pemindahan jam pakai (load shifting).
4. Audit konsumsi per ruangan dan perhitungan vampire power (daya standby yang tetap terpakai saat alat tidak aktif).
5. Prediksi habisnya token listrik berdasarkan pemakaian harian serta grafik ASCII sisa token dari 3 transaksi terakhir.
6. Pengaturan golongan daya PLN, simulasi pembelian token prabayar dengan potongan PPJ 3%, dan pembuatan kode token 20 digit.
7. Ekspor laporan audit lengkap ke `laporan_audit.txt`, mencakup rincian perangkat, estimasi emisi CO2, kebutuhan pohon ekuivalen, dan tabel simulasi beban 24 jam.
8. Smart Budget Optimizer berbasis algoritma greedy dengan daftar ID perangkat yang dikecualikan agar tidak dikurangi jam pakainya.

## Cara Menjalankan

Pastikan Python 3 sudah terpasang. Tidak perlu menginstal paket tambahan.

```bash
git clone https://github.com/bravenaufala/wattwise.git
cd wattwise
python main.py
```

Di Linux atau macOS, gunakan `python3 main.py`.

## Struktur Proyek

```text
wattwise/
├── main.py             Entry point dan navigasi menu CLI
├── modul_crud.py       Manajemen profil PLN, CRUD perangkat, validasi, dan log aktivitas
├── modul_analisis.py   Search, sort, operasi set, simulasi 24 jam, emisi CO2, budget optimizer, dan ekspor laporan
├── modul_prediksi.py   Transaksi token PLN, prediksi habis token, dan grafik sisa token
├── data_profil.txt     Konfigurasi golongan daya PLN dan sisa token (kWh)
├── data_perangkat.txt  Data inventaris perangkat (dipisahkan karakter '|')
├── log_aktivitas.txt   Catatan riwayat tambah, ubah, dan hapus perangkat
├── riwayat_token.txt   Riwayat pembelian token listrik
├── laporan_audit.txt   Hasil ekspor laporan audit kelistrikan
└── README.md
```

## Penerapan Materi Praktikum

| Topik | Implementasi di Kode | Lokasi |
| :--- | :--- | :--- |
| Tuple & unpacking | Daftar golongan tarif PLN `(kode, va, batas_watt, tarif)` | `modul_crud.py` (`GOLONGAN_PLN`), `main.py` (`menu_profil_daya`) |
| List & dictionary | Representasi setiap perangkat sebagai `dict` di dalam `list` | `modul_crud.py` (`muat_perangkat`, `tambah_perangkat`) |
| Set | Ruangan unik, irisan jam bentrok, selisih alat boros, gabungan jam ruangan | `modul_analisis.py` (`ambil_himpunan_ruangan`, `deteksi_bentrok_jam_perangkat`, `deteksi_perangkat_boros`, `gabungkan_jam_aktif_ruangan`) |
| Fungsi rekursif | Binary search ID perangkat secara rekursif | `modul_analisis.py` (`binary_search_rekursif`, `cari_perangkat_id_binary`) |
| Searching & sorting | Linear search, binary search, bubble sort, insertion sort, selection sort | `modul_analisis.py` |
| Nested loop | Matriks simulasi beban 24 jam dan audit konsumsi per ruangan | `modul_analisis.py` (`simulasi_beban_24jam`, `audit_per_ruangan`) |
| String & file handling | Parsing delimiter `\|`, sanitasi input, parsing rentang jam (`8-12`, `22-2`), baca/tulis/append `.txt` | `modul_crud.py`, `modul_analisis.py`, `modul_prediksi.py` |

## Pembagian Tugas Tim

### Brave (`bravenaufala`)
- Merancang struktur awal aplikasi, skema penyimpanan file `.txt`, dan menu utama di `main.py`.
- Mengimplementasikan binary search rekursif, bubble sort, insertion sort, selection sort, dan operasi set.
- Membangun simulasi beban 24 jam, rekomendasi pemindahan jam pakai (`rekomendasi_anti_jeglek`), detektor vampire power, transaksi token PLN (`beli_token_listrik`, `tampilkan_struk_token`), serta prediksi habisnya token.
- Menggabungkan branch tim, memperbaiki bug pasca-merge, dan merapikan format kode.

### Faisal (`Pesalll`)
- Menambahkan deteksi perangkat duplikat berdasarkan nama dan ruangan (`cari_perangkat_duplikat`) pada proses tambah dan ubah data.
- Membangun ringkasan perbandingan sebelum dan sesudah perubahan (before vs after diff) dengan konfirmasi simpan di `ubah_perangkat`.
- Menambahkan pencatatan log aktivitas (`catat_log_aktivitas`, `lihat_log_aktivitas`) ke `log_aktivitas.txt` serta menu riwayat log di submenu CRUD.
- Menambahkan opsi filter ruangan pada tampilan inventaris perangkat dan memperbaiki pencocokan perangkat pada simulasi agar berbasis ID, bukan nama.

### Kaka (`sabiru11`)
- Membangun fitur Smart Budget Optimizer di `modul_analisis.py` dengan algoritma greedy dan dukungan daftar ID pengecualian (Menu 8).
- Menambahkan grafik ASCII sisa token dari 3 transaksi terakhir (`tampilkan_grafik_sisa_token`) di `modul_prediksi.py` dan mengintegrasikannya ke Menu 5.
- Menambahkan kalkulator estimasi emisi CO2 dan kebutuhan pohon ekuivalen (`hitung_emisi_karbon`).
- Memperluas hasil ekspor `laporan_audit.txt` agar memuat data emisi karbon, tabel simulasi beban 24 jam, dan catatan peringatan overload.

## Alur Singkat Demo

1. Jalankan `python main.py` untuk menampilkan menu utama beserta informasi daya dan sisa token.
2. Buka Menu 1 untuk mendemokan tambah/ubah perangkat (termasuk cek duplikat, before vs after diff), filter per ruangan, dan riwayat log aktivitas.
3. Buka Menu 2 untuk mencoba pencarian ID dengan binary search rekursif, pengurutan biaya/daya, serta cek bentrok jam 2 perangkat.
4. Buka Menu 3 untuk menampilkan simulasi beban 24 jam, status overload, dan saran pergeseran jam pakai.
5. Buka Menu 4 untuk melihat audit per ruangan dan perhitungan vampire power.
6. Buka Menu 5 dan Menu 6 untuk mengecek prediksi habis token, grafik 3 top-up terakhir, serta simulasi pembelian token.
7. Buka Menu 8 untuk menguji Smart Budget Optimizer dengan mengecualikan ID perangkat tertentu.
8. Buka Menu 7 lalu periksa `laporan_audit.txt` untuk melihat hasil ekspor laporan lengkap.
