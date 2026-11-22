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
| **3** | **Set Operations Lengkap** | `set()` untuk ruangan unik, `.intersection()` untuk irisan bentrok jam 2 alat, `.difference()` untuk deteksi alat boros, dan `.union()` untuk gabungan jam aktif ruangan | `modul_analisis.py` (`ambil_himpunan_ruangan`, `deteksi_bentrok_jam_perangkat`, `deteksi_perangkat_boros`, `gabungkan_jam_aktif_ruangan`) |
| **4** | **Fungsi Rekursif (Recursion)** | Pencarian ID perangkat dengan Binary Search secara rekursif murni (Base case & Recursive step) dengan kompleksitas $O(\log n)$ | `modul_analisis.py` (`binary_search_rekursif`, `cari_perangkat_id_binary`) |
| **5** | **Searching & Sorting Lengkap** | • **Searching:** Linear Search (nama & ruangan) dan Binary Search Rekursif (ID).<br>• **Sorting:** Optimized Bubble Sort (`swapped` flag), Insertion Sort (Watt aktif), dan Selection Sort (Prioritas). | `modul_analisis.py` (`cari_perangkat_nama`, `cari_perangkat_id_binary`, `urutkan_perangkat_biaya`, `urutkan_perangkat_watt_insertion`, `urutkan_perangkat_prioritas`) |
| **6** | **Nested Loop (Perulangan Bersarang)** | Outer loop 24 jam & inner loop daftar perangkat untuk matriks simulasi beban ASCII; Outer loop ruangan & inner loop perangkat untuk audit per ruangan | `modul_analisis.py` (`simulasi_beban_24jam`, `audit_per_ruangan`) |
| **7** | **Manipulasi String & File Handling** | Operasi `.split('|')`, `.join('|')`, `.strip()`, `.title()`, sanitasi string delimiter pipe, parsing rentang jam fleksibel (`8-12`), struk token 20 digit, dan file I/O multi-entitas (`.txt`) | `modul_crud.py`, `modul_analisis.py`, & `modul_prediksi.py` |

---

## 👥 5. Pembagian Jobdesk Anggota Tim (3 Orang)

### 👤 Anggota 1 (Lead Developer / System Architect & Algorithm Specialist)
- **Tanggung Jawab:**
  - Merancang arsitektur sistem, struktur data `Tuple` regulasi PLN, dan integrasi antar-modul di `main.py`.
  - Mengimplementasikan **Fungsi Rekursif & Binary Search** (`binary_search_rekursif`) untuk pencarian ID perangkat $O(\log n)$.
  - Mengimplementasikan **Insertion Sort** manual untuk menyortir beban Watt aktif dan optimasi `swapped` flag pada Bubble Sort.
  - Mengimplementasikan **Set Union** (`gabungkan_jam_aktif_ruangan`) serta algoritma **Smart Load Shifting (Anti-Jeglek Otomatis)**.
  - Membangun subsistem transaksi **Beli Token Listrik PLN** (perhitungan PPJ 3%, penambahan kWh, generate kode token 20 digit, dan struk digital).
  - Merancang sistem pewarnaan antarmuka terminal (ANSI Escape Colors — Zero Dependency).
- **File Kerja:** `main.py`, `modul_analisis.py` (Search/Sort/Rekursi/Union/Anti-Jeglek), `modul_prediksi.py` (Beli Token), dan `modul_crud.py` (ANSI/Tuple).

---

### 👤 Anggota 2 (CRUD, Data Integrity & Form Validation Specialist)
- **Tanggung Jawab:**
  - Membangun operasi **CRUD Lengkap** pada inventaris perangkat (Tambah, Lihat, Ubah, Hapus).
  - Membangun mekanisme sanitasi string (`sanitasi_string`) untuk mencegah kerusakan file `.txt` akibat karakter delimiter pipe (`|`).
  - Membangun parser input rentang jam fleksibel (`parse_rentang_jam`) yang mendukung format koma maupun rentang strip (`8-12` / `22-2`).
  - Membangun fitur **Linear Search** (pencarian nama & ruangan) dan **Selection Sort** (pengurutan prioritas: Primer $\rightarrow$ Sekunder $\rightarrow$ Tersier).
  - Mengimplementasikan operasi himpunan **Set Difference** (`deteksi_perangkat_boros`) dan **Set Intersection** (`deteksi_bentrok_jam_perangkat`).
- **File Kerja:** `modul_crud.py` (CRUD & Validasi) dan `modul_analisis.py` (Linear Search, Selection Sort, Set Difference & Intersection).

---

### 👤 Anggota 3 (Nested Loop, Simulation & Analytics Specialist)
- **Tanggung Jawab:**
  - Membangun algoritma **Perulangan Bersarang (Nested Loop)** untuk Simulasi Matriks Beban 24 Jam dengan visualisasi ASCII load bar chart dan detektor alarm overload.
  - Membangun audit beban bersarang per ruangan (Outer loop: Ruangan unik, Inner loop: Perangkat).
  - Menghitung kebocoran energi dan kerugian finansial akibat **Vampire Power (Daya Standby)** per bulan dan per tahun.
  - Membangun fitur **Prediksi Waktu Habisnya Token** menggunakan modul `datetime` & `timedelta`.
  - Mengimplementasikan optimasi anggaran **Smart Budget Optimizer** dengan pendekatan algoritma Greedy berjenjang beserta integrasi penyimpanan jadwal baru ke database.
  - Mengimplementasikan fitur **Export Laporan Resmi Audit Listrik** ke file teks format `.txt`.
- **File Kerja:** `modul_analisis.py` (Simulasi 24 Jam, Audit Ruangan, Vampire Power, Export) dan `modul_prediksi.py` (Prediksi Token & Budget Optimizer).

---

## 🎭 6. Skenario Demonstrasi saat Presentasi (Alur Demo Juara Tanpa Slide)

1. **Langkah 1 (Anggota 1):**
   - Buka terminal, tunjukkan instalasi yang sangat bersih (zero-dependency, cukup `python main.py`).
   - Tunjukkan menu utama berwana ANSI. Buka Menu 6 -> Opsi 2 (Beli Token Listrik PLN). Masukkan nominal Rp 50.000, tunjukkan kalkulasi potongan PPJ 3%, penambahan kWh, pencatatan otomatis ke `riwayat_token.txt`, dan cetak struk kode stroom 20 digit.
   - Buka Menu 2 -> Opsi 3 (Binary Search Rekursif). Cari ID `EL04` dan jelaskan proses pemanggilan fungsi rekursif $O(\log n)$.
2. **Langkah 2 (Anggota 2):**
   - Buka Menu 1 (Manajemen CRUD Perangkat). Tunjukkan tabel inventaris dengan kolom persentase beban biaya.
   - Demokan penambahan alat baru (Create) dengan rentang jam fleksibel `8-12` dan perlihatkan sanitasi input.
   - Buka Menu 2 -> Opsi 9 (Set Intersection) untuk membuktikan deteksi bentrok jam antara Rice Cooker dan Setrika pada Pk 18:00-19:00.
3. **Langkah 3 (Anggota 3):**
   - Buka Menu 3 (Simulasi Beban 24 Jam). Tunjukkan matriks 24 baris dengan ASCII bar berwarna merah di Pk 19:00 (1308 W > 1100 W Overload).
   - Tunjukkan fitur **Smart Load Shifting**: sistem secara cerdas menyarankan pemindahan jam Setrika ke Pk 08:00 sehingga beban Pk 19:00 langsung turun menjadi 958 W (Aman).
   - Buka Menu 5 (Prediksi Token & Budget Optimizer). Masukkan anggaran Rp 200.000, perlihatkan algoritma Greedy memangkas jam alat Tersier, lalu terapkan jadwal hemat ke database.
   - Buka Menu 7 (Export Laporan) dan buka file `laporan_audit.txt` untuk membuktikan hasil audit telah tersimpan permanen.

---

## 🎯 7. Cheat Sheet Tanya Jawab Perorangan (Bocoran Pertanyaan Dosen & Jawaban)

### ❓ Pertanyaan untuk Anggota 1 (Lead / Algorithm & Architecture):
* **Dosen:** *"Di mana letak implementasi Fungsi Rekursif pada program kalian dan bagaimana cara kerjanya?"*
  * **Jawaban Mantap:** *"Kami mengimplementasikannya pada fungsi `binary_search_rekursif` di `modul_analisis.py`. Fungsi ini memiliki dua base case: pertama, jika `low > high`, artinya data tidak ada; kedua, jika elemen tengah `mid` sama dengan target ID, data ditemukan. Jika target lebih kecil atau lebih besar, fungsi memanggil dirinya sendiri secara rekursif pada paruh subarray kiri atau kanan dengan membagi ruang pencarian menjadi setengahnya ($O(\log n)$)."*
* **Dosen:** *"Bagaimana cara kerja algoritma Insertion Sort pada pengurutan daya Watt?"*
  * **Jawaban Mantap:** *"Insertion sort bekerja dengan mengasumsikan elemen pertama sudah terurut. Lalu pada perulangan dari elemen ke-1 hingga n-1, sistem mengambil elemen `key` dan membandingkannya mundur ke belakang melalui `while j >= 0`. Jika elemen sebelumnya lebih kecil dari `key` (untuk descending), elemen digeser ke kanan `data[j+1] = data[j]`. Ketika posisi yang tepat ditemukan, `key` disisipkan ke posisi tersebut."*
* **Dosen:** *"Bagaimana sistem menangani transaksi token listrik prabayar?"*
  * **Jawaban Mantap:** *"Pada fungsi `beli_token_listrik`, nominal input dipotong PPJ 3% sesuai regulasi PLN untuk mendapatkan nilai bersih. Nilai bersih dibagi tarif golongan saat ini untuk memperoleh kWh. Sisa kWh di profil diakumulasikan, disimpan ke `data_profil.txt`, dan baris histori baru di-append ke `riwayat_token.txt` lengkap dengan nomor token acak 20 digit berformat standar PLN."*

---

### ❓ Pertanyaan untuk Anggota 2 (CRUD & Data Validation):
* **Dosen:** *"Bagaimana program menjamin data di file teks tidak korup jika pengguna memasukkan karakter sembarangan?"*
  * **Jawaban Mantap:** *"Kami membuat fungsi sanitasi string `sanitasi_string` di `modul_crud.py`. Karena file database kami menggunakan delimiter pipe `|`, setiap input teks nama atau ruangan secara otomatis disanitasi dengan mengganti karakter pipe menjadi garis miring `/` dan membersihkan spasi awal/akhir dengan `.strip()`."*
* **Dosen:** *"Bagaimana kalian mengurai input rentang jam yang fleksibel seperti '8-12'?"*
  * **Jawaban Mantap:** *"Kami membuat fungsi parser `parse_rentang_jam`. Input di-split berdasarkan koma, lalu untuk tiap segmen yang mengandung karakter tanda hubung `-`, kami split batas awal dan akhirnya, lalu memasukkan bilangan integer dalam rentang tersebut ke dalam tipe data `set` guna menjamin jam aktif bernilai unik (0 s/d 23), termasuk penanganan jam lewat tengah malam seperti '22-2'."*
* **Dosen:** *"Bagaimana operasi Set Intersection dan Set Difference diterapkan pada data inventaris?"*
  * **Jawaban Mantap:** *"Set Intersection kami gunakan pada `deteksi_bentrok_jam_perangkat` dengan mengiriskan `set(jam_alat_A).intersection(set(jam_alat_B))` untuk mengetahui jam berapa kedua alat menyala bersamaan. Sedangkan Set Difference kami gunakan pada `deteksi_perangkat_boros` dengan mengurangkan himpunan seluruh ID perangkat dengan himpunan ID perangkat hemat energi menggunakan `.difference()`."*

---

### ❓ Pertanyaan untuk Anggota 3 (Nested Loop, Simulation & Analytics):
* **Dosen:** *"Bagaimana perulangan bersarang (Nested Loop) bekerja pada fitur Simulasi Beban 24 Jam?"*
  * **Jawaban Mantap:** *"Outer loop mengiterasi 24 jam dalam sehari dari jam 0 s/d 23. Di setiap jam, Inner loop mengiterasi seluruh daftar perangkat dalam rumah. Jika jam saat itu ada di dalam list `rentang_jam` perangkat, maka daya aktifnya dijumlahkan; jika tidak, daya standby-nya yang dijumlahkan. Akumulasi daya ini dibandingkan dengan batas aman daya PLN untuk menggambar ASCII bar chart dan status overload."*
* **Dosen:** *"Bagaimana logika algoritma Greedy pada Smart Budget Optimizer?"*
  * **Jawaban Mantap:** *"Algoritma Greedy mengambil keputusan lokal terbaik secara bertahap. Sistem menyortir perangkat dari prioritas terendah yaitu Tersier terlebih dahulu. Selama total estimasi biaya masih melebihi budget target pengguna, sistem memangkas jam operasional perangkat Tersier 1 jam demi 1 jam. Jika perangkat Tersier sudah minimal dan budget belum tercapai, sistem beralih memangkas perangkat Sekunder, sehingga perangkat Primer (seperti kulkas/pompa) tetap terlindungi."*
* **Dosen:** *"Bagaimana sistem menghasilkan rekomendasi otomatis Smart Load Shifting saat listrik jeglek?"*
  * **Jawaban Mantap:** *"Pada fungsi `rekomendasi_anti_jeglek`, sistem mendeteksi perangkat non-primer berdaya besar yang menyala pada jam overload tersebut (misal Setrika 350 W pada Pk 19:00). Sistem kemudian memindai jam-jam kosong di siang/sore hari yang beban kumulatifnya masih sangat rendah, lalu merekomendasikan pemindahan jadwal pemakaian ke jam tersebut agar beban jam 19:00 turun drastis di bawah batas kapasitas aman MCB."*
