# ⚡ WattWise Home — Simulator Audit Listrik, Anti-Jeglek & Detektor Vampire Power

**Proyek Akhir Praktikum Dasar Pemrograman (Python)**  
Target Capaian: **Nilai UAS = 100**  
Tim Pengembang: 3 Orang  
Model: 100% CLI Terminal (Pure Python Standard Library — Zero-Dependency)

---

## 📌 1. Deskripsi Singkat & Solusi Masalah
**WattWise Home** adalah aplikasi audit kelistrikan rumah tangga berbasis teks (CLI) yang dirancang untuk mengatasi 3 permasalahan nyata:
1. **Listrik Sering "Jeglek" (MCB Trip):** Menghitung beban kumulatif per jam (24 jam) dan mendeteksi bentrok jam menyala alat berdaya besar.
2. **Kebocoran Vampire Power:** Menghitung energi dan uang yang terbuang sia-sia akibat alat yang dimatikan tetapi kabelnya tetap dicolok ke stopkontak.
3. **Prediksi Kehabisan Token Listrik & Diet Anggaran:** Mengestimasi sisa hari sebelum token kWh habis serta memberikan rekomendasi otomatis (*Greedy Diet*) pemangkasan jam pakai agar tagihan sesuai target anggaran.

---

## 🚀 2. Panduan Instalasi & Menjalankan Program (Tinggal Copy-Paste)

Program ini dibuat murni menggunakan **Python Standard Library (Zero-Dependency)** sehingga **tidak memerlukan `pip install` apa pun**. 100% aman dijalankan di sistem operasi Linux, macOS, maupun Windows tanpa risiko masalah *dependency*.

### 📋 Cara Cepat (One-Line Copy & Paste di Terminal)
Cukup salin dan tempel blok perintah berikut langsung ke Terminal / Command Prompt Anda:

```bash
git clone https://github.com/bravenaufala/wattwise.git && cd wattwise && python3 main.py
```

---

### 💻 Langkah Manual Bertahap:
```bash
# 1. Clone repositori dari GitHub ke laptop Anda
git clone https://github.com/bravenaufala/wattwise.git

# 2. Masuk ke direktori proyek
cd wattwise

# 3. Jalankan program aplikasi
python3 main.py    # Pada Windows: python main.py
```

---

## 🗂️ 3. Struktur File Proyek
```text
wattwise_project/
│
├── main.py            # Entry point & navigasi menu interaktif CLI
├── modul_crud.py      # Core data, File Handling, Tuple tarif PLN & CRUD lengkap
├── modul_analisis.py  # Searching, Sorting manual (Bubble Sort), Operasi Set & Simulasi 24 Jam
├── modul_prediksi.py  # Prediksi habisnya token (DateTime) & Greedy Budget Optimizer
│
├── data_profil.txt    # Konfigurasi daya PLN rumah & sisa token kWh
├── data_perangkat.txt # Database inventaris alat elektronik (delimiter '|')
├── riwayat_token.txt  # Histori pembelian dan pengisian token listrik
├── laporan_audit.txt  # File hasil export laporan resmi audit listrik
└── README.md          # Dokumentasi teknis & panduan tanya-jawab presentasi
```

---

## 🛠️ 4. Pemetaan Materi Praktikum ke dalam Kode (Wajib Tahu Saat Demo)

| No | Topik Praktikum | Penerapan Nyata di Kode | Lokasi File & Fungsi |
|---|---|---|---|
| **1** | **Tuple & Sequence Unpacking** | Konstanta tarif PLN `(Kode, VA, Batas_W, Tarif)` yang di-unpack saat pemilihan golongan | `modul_crud.py` (`GOLONGAN_PLN`) & `main.py` (`menu_profil_daya`) |
| **2** | **Dictionary & List** | Setiap perangkat direpresentasikan sebagai `dict` dan dihimpun ke dalam list inventaris | `modul_crud.py` (`muat_perangkat`, `tambah_perangkat`) |
| **3** | **Set Operations** | `set()` untuk ruangan unik, `.intersection()` untuk bentrok jam, dan `.difference()` untuk mendeteksi alat boros | `modul_analisis.py` (`ambil_himpunan_ruangan`, `deteksi_perangkat_boros`) |
| **4** | **Nested Loop (Perulangan Bersarang)** | Outer loop 24 jam & inner loop daftar perangkat untuk grafik ASCII simulasi beban; Outer loop ruangan & inner loop perangkat untuk audit ruangan | `modul_analisis.py` (`simulasi_beban_24jam`, `audit_per_ruangan`) |
| **5** | **Searching & Sorting Manual** | Linear Search (cari nama/ruangan/daya) dan Bubble Sort manual (urutkan biaya & vampire power) tanpa bergantung pada fungsi bawaan | `modul_analisis.py` (`cari_perangkat_nama`, `urutkan_perangkat_biaya`) |
| **6** | **Manipulasi String & File I/O** | Operasi `.split('\|')`, `.join('\|')`, `.strip()`, `.title()`, format rupiah kustom, serta `open(..., 'r'/'w')` | `modul_crud.py` & `modul_analisis.py` (`export_laporan_audit`) |

---

## 👥 5. Pembagian Jobdesk Anggota Tim (3 Orang)

### 👤 Anggota 1: Core Data, File Handling & CRUD (Create & Read)
- **Tanggung Jawab:**
  - Merancang struktur data `Tuple` golongan tarif PLN dan `Dictionary` perangkat.
  - Membangun mekanisme file handling baca/tulis (`.txt`) dengan delimiter `|`.
  - Mengimplementasikan fitur **Tambah Perangkat (Create)** dengan validasi input string & angka.
  - Mengimplementasikan fitur **Lihat Inventaris (Read)** dengan tabel ASCII dan kalkulasi kWh/biaya bulanan.
- **File Kerja:** `modul_crud.py` (bagian atas & Create/Read) dan `main.py` (menu awal).

---

### 👤 Anggota 2: CRUD (Update & Delete), Searching, Sorting & Operasi Set
- **Tanggung Jawab:**
  - Mengimplementasikan fitur **Ubah Data Perangkat (Update)** dan **Hapus Perangkat (Delete)**.
  - Membangun algoritma **Searching (Linear Search)** berdasarkan nama alat dan ruangan.
  - Membangun algoritma **Sorting manual (Bubble Sort & Selection Sort)** untuk menyortir perangkat terboros dan standby tertinggi.
  - Menerapkan tipe data **Set** untuk daftar ruangan unik serta operasi `.difference()` & `.intersection()`.
- **File Kerja:** `modul_crud.py` (Update/Delete) dan `modul_analisis.py` (Set, Search, Sort).

---

### 👤 Anggota 3: Nested Loop (Simulasi 24 Jam), Vampire Power, Prediksi & Export
- **Tanggung Jawab:**
  - Membangun algoritma **Perulangan Bersarang (Nested Loop)** untuk Simulasi Matriks Beban 24 Jam dengan ASCII bar chart dan detektor Anti-Jeglek.
  - Menghitung kerugian kebocoran daya standby (**Vampire Power**) per bulan dan per tahun.
  - Membangun fitur tambahan **Prediksi Habisnya Token** menggunakan modul `datetime` dan **Smart Budget Optimizer** dengan pendekatan algoritma Greedy.
  - Mengimplementasikan fitur **Export Laporan Audit** ke file `laporan_audit.txt`.
- **File Kerja:** `modul_analisis.py` (Simulasi 24 Jam, Audit Ruangan, Export) dan `modul_prediksi.py`.

---

## 🎭 6. Skenario Demonstrasi saat Presentasi (Alur Demo Juara)
1. **Langkah 1 (Anggota 1):** Buka terminal, jelaskan bahwa program zero-dependency. Pilih Menu 1 -> Sub-menu 2 (Lihat Data). Tunjukkan bagaimana data dibaca dari file `data_perangkat.txt`. Tambah 1 perangkat baru (Sub-menu 1) untuk demo Create.
2. **Langkah 2 (Anggota 2):** Pilih Menu 2 (Pencarian & Pengurutan). Demokan pencarian nama "AC" atau ruangan "Dapur". Lalu klik urutkan biaya terboros (Bubble sort berjalan). Jelaskan cara kerja pertukaran (*swap*) elemen di Bubble Sort.
3. **Langkah 3 (Anggota 3):** Pilih Menu 3 (Simulasi Beban 24 Jam). Tunjukkan visualisasi bar ASCII Jam 19:00 yang melonjak hingga **1308 W (>1100 W)** dan memicu alarm **OVERLOAD / MCB TRIP**. Jelaskan outer loop (jam) dan inner loop (perangkat).
4. **Langkah 4 (Anggota 3):** Pilih Menu 4 (Vampire Power) untuk menunjukkan uang yang terbuang sia-sia per tahun. Lalu buka Menu 5 untuk demo Prediksi Token & Budget Optimizer (masukkan budget Rp 200.000). Terakhir pilih Menu 7 untuk export laporan ke file `.txt`.

---

## 🎯 7. Cheat Sheet Tanya Jawab Perorangan (Bocoran Pertanyaan Dosen & Jawaban)

### ❓ Pertanyaan untuk Anggota 1:
* **Dosen:** *"Mengapa Golongan PLN disimpan dalam bentuk Tuple, bukan List?"*
  * **Jawaban Mantap:** *"Karena tarif dasar listrik PLN merupakan konstanta regulasi yang sifatnya immutable (tidak boleh diubah sembarangan saat runtime). Tuple melindungi data ini dari perubahan tidak sengaja dan mendukung sequence unpacking secara cepat saat membaca `kode, va, batas_w, tarif = GOLONGAN_PLN[i]`."*
* **Dosen:** *"Bagaimana cara program menangani data yang dibaca dari file teks agar bisa diolah sebagai angka?"*
  * **Jawaban Mantap:** *"Saat membaca baris dari file `.txt`, kami menggunakan metode `.strip()` untuk menghilangkan enter/spasi, lalu memecahnya dengan `.split('\|')`. Kolom angka seperti watt dan jam kemudian kami konversi eksplisit dengan tipe data `int()` atau `float()` sebelum dimasukkan ke dalam Dictionary."*

---

### ❓ Pertanyaan untuk Anggota 2:
* **Dosen:** *"Coba jelaskan bagaimana algoritma Bubble Sort pada fungsi `urutkan_perangkat_biaya` bekerja!"*
  * **Jawaban Mantap:** *"Bubble Sort bekerja dengan membandingkan dua elemen yang bersebelahan secara berulang melalui nested loop. Pada inner loop, jika elemen saat ini memiliki biaya lebih kecil daripada elemen berikutnya (untuk pengurutan menurun/descending), posisinya ditukar menggunakan mekanisme swap Python `data[j], data[j+1] = data[j+1], data[j]`. Proses ini diulang sebanyak n-1 kali hingga elemen terbesar mengapung ke posisi atas."*
* **Dosen:** *"Di mana letak penerapan operasi himpunan (Set) dan apa fungsinya?"*
  * **Jawaban Mantap:** *"Kami menerapkan Set di fungsi `ambil_himpunan_ruangan` untuk mengeliminasi duplikasi nama ruangan. Selain itu, kami menggunakan `.difference()` pada `deteksi_perangkat_boros` untuk mencari selisih antara seluruh perangkat dan perangkat hemat energi, serta `.intersection()` untuk mendeteksi irisan jam nyala yang bentrok."*

---

### ❓ Pertanyaan untuk Anggota 3:
* **Dosen:** *"Bagaimana perulangan bersarang (Nested Loop) bekerja pada fitur Simulasi 24 Jam?"*
  * **Jawaban Mantap:** *"Outer loop mengiterasi indeks jam dari 0 hingga 23 (24 jam). Pada setiap jam tersebut, Inner loop mengiterasi seluruh daftar perangkat dalam rumah. Jika jam saat itu ada di dalam `rentang_jam` perangkat, maka daya aktifnya dijumlahkan; jika tidak, daya standby-nya yang dijumlahkan. Hasil penjumlahan inilah yang divisualisasikan menjadi ASCII load bar."*
* **Dosen:** *"Bagaimana logika algoritma Greedy pada Smart Budget Optimizer?"*
  * **Jawaban Mantap:** *"Algoritma Greedy mengambil keputusan lokal terbaik secara bertahap. Sistem menyortir perangkat dari prioritas terendah yaitu Tersier terlebih dahulu. Selama total estimasi biaya masih melebihi budget target pengguna, sistem memangkas jam operasional perangkat Tersier 1 jam demi 1 jam. Jika perangkat Tersier sudah minimal dan budget belum tercapai, sistem beralih memangkas perangkat Sekunder, sehingga perangkat Primer (seperti kulkas/pompa) tetap terlindungi."*
