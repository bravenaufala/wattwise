# ==============================================================================
# MODUL CRUD & FILE HANDLING (modul_crud.py)
# Bagian Tanggung Jawab:
# - Anggota 1: Core Data, File Handling, Create (Tambah), Read (Tampil)
# - Anggota 2: Update (Ubah), Delete (Hapus) & Validasi ID
# ==============================================================================

import os
from datetime import datetime

# [MATERI: KELAS & KONSTANTA - ANSI ESCAPE COLORS UNTUK CLI]
class Warna:
    """Kode warna ANSI standar untuk mempercantik antarmuka terminal (Zero-dependency)."""
    MERAH = "\033[91m"
    HIJAU = "\033[92m"
    KUNING = "\033[93m"
    BIRU = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    PUTIH = "\033[97m"
    TEBAL = "\033[1m"
    RESET = "\033[0m"

# [MATERI: TUPLE]
# Konstanta Golongan Tarif Listrik PLN (Ordered & Immutable)
# Format tiap tuple: (Kode_Golongan, Daya_VA, Batas_Watt_Aman, Tarif_Per_kWh)
GOLONGAN_PLN = (
    ("R1-450", 450, 360, 415.0),
    ("R1-900", 900, 790, 1352.0),
    ("R1-1300", 1300, 1100, 1444.70),
    ("R1-2200", 2200, 1870, 1444.70),
    ("R2-3500", 3500, 2975, 1699.53)
)

FILE_PROFIL = "data_profil.txt"
FILE_PERANGKAT = "data_perangkat.txt"
FILE_LOG = "log_aktivitas.txt"

# [MATERI: STRING MANIPULATION - SANITASI INPUT FILE]
def sanitasi_string(teks):
    """
    Menghilangkan karakter delimiter pipe '|' agar struktur file teks tidak rusak,
    serta membersihkan spasi berlebih di awal dan akhir string.
    """
    if not teks:
        return ""
    return teks.replace("|", "/").strip()

def cari_perangkat_duplikat(daftar_perangkat, nama, ruangan, id_dikecualikan=None):
    """Mencari perangkat dengan kombinasi nama & ruangan yang sama
    (tidak membedakan huruf besar/kecil maupun spasi berlebih)."""
    def normalisasi(teks):
        return " ".join(sanitasi_string(teks).split()).casefold()

    nama_normal = normalisasi(nama)
    ruang_normal = normalisasi(ruangan)

    for perangkat in daftar_perangkat:
        if id_dikecualikan and perangkat["id"] == id_dikecualikan:
            continue
        if (normalisasi(perangkat["nama"]) == nama_normal
                and normalisasi(perangkat["ruangan"]) == ruang_normal):
            return perangkat

    return None

# [MATERI: STRING MANIPULATION - PARSING RENTANG JAM FLEKSIBEL]
def parse_rentang_jam(input_str):
    """
    Mengurai string input rentang jam yang fleksibel.
    Mendukung format koma: '6, 18, 19'
    Mendukung format rentang: '8-12' (menghasilkan jam 8, 9, 10, 11, 12)
    Mendukung format lewat tengah malam: '22-2' (jam 22, 23, 0, 1, 2)
    """
    jam_set = set()
    if not input_str:
        return []

    bagian_list = input_str.split(",")
    for bagian in bagian_list:
        bagian = bagian.strip()
        if "-" in bagian:
            sub = bagian.split("-")
            if len(sub) == 2 and sub[0].strip().isdigit() and sub[1].strip().isdigit():
                awal = int(sub[0].strip())
                akhir = int(sub[1].strip())
                if 0 <= awal <= 23 and 0 <= akhir <= 23:
                    if awal <= akhir:
                        for j in range(awal, akhir + 1):
                            jam_set.add(j)
                    else:
                        for j in range(awal, 24):
                            jam_set.add(j)
                        for j in range(0, akhir + 1):
                            jam_set.add(j)
        elif bagian.isdigit():
            j = int(bagian)
            if 0 <= j <= 23:
                jam_set.add(j)

    return sorted(list(jam_set))

# [MATERI: STRING MANIPULATION - FORMAT CURRENCY]
def format_rupiah(angka):
    """Mengubah bilangan bulat/float menjadi string format mata uang Rupiah."""
    return f"Rp {angka:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

# [MATERI: FUNGSI & FILE HANDLING - PROFIL RUMAH]
def muat_profil():
    """
    Membaca data konfigurasi daya rumah dari data_profil.txt.
    Mengembalikan dictionary profil rumah.
    """
    # Auto-seed jika file profil belum ada
    if not os.path.exists(FILE_PROFIL):
        simpan_profil("R1-1300", 1300, 1100, 1444.70, 40.0)

    try:
        with open(FILE_PROFIL, "r", encoding="utf-8") as f:
            baris = f.readline().strip()
            # [MATERI: MANIPULASI STRING - SPLIT]
            parts = baris.split("|")
            if len(parts) >= 5:
                return {
                    "golongan": parts[0],
                    "va": int(parts[1]),
                    "batas_watt": int(parts[2]),
                    "tarif": float(parts[3]),
                    "sisa_token_kwh": float(parts[4])
                }
    except Exception as e:
        print(f"[!] Terjadi kesalahan saat membaca file profil: {e}")

    # Fallback default
    return {
        "golongan": "R1-1300",
        "va": 1300,
        "batas_watt": 1100,
        "tarif": 1444.70,
        "sisa_token_kwh": 40.0
    }

def simpan_profil(golongan, va, batas_watt, tarif, sisa_token_kwh):
    """Menyimpan data profil ke dalam data_profil.txt."""
    with open(FILE_PROFIL, "w", encoding="utf-8") as f:
        # [MATERI: MANIPULASI STRING - JOIN / CONCATENATION]
        baris = f"{golongan}|{va}|{batas_watt}|{tarif}|{float(sisa_token_kwh):.2f}\n"
        f.write(baris)

# [MATERI: FILE HANDLING & DICTIONARY - MEMBACA DAFTAR PERANGKAT]
def muat_perangkat():
    """
    Membaca seluruh data perangkat dari data_perangkat.txt.
    Mengembalikan list of dictionaries.
    """
    daftar_perangkat = []
    if not os.path.exists(FILE_PERANGKAT):
        return daftar_perangkat

    with open(FILE_PERANGKAT, "r", encoding="utf-8") as f:
        baris_semua = f.readlines()

    # Lewati baris header pertama
    for baris in baris_semua[1:]:
        baris = baris.strip()
        if not baris:
            continue
        parts = baris.split("|")
        if len(parts) >= 8:
            # Parsing jam aktif menjadi list of int
            jam_str = parts[6].split(",") if parts[6] else []
            jam_list = []
            for j in jam_str:
                j = j.strip()
                if j.isdigit():
                    jam_list.append(int(j))

            perangkat = {
                "id": parts[0].strip(),
                "nama": parts[1].strip(),
                "ruangan": parts[2].strip(),
                "watt_aktif": int(parts[3]),
                "watt_standby": int(parts[4]),
                "jam_pakai": int(parts[5]),
                "rentang_jam": jam_list,
                "prioritas": parts[7].strip()
            }
            daftar_perangkat.append(perangkat)

    return daftar_perangkat

# [MATERI: FILE HANDLING - MENULIS DATA PERANGKAT]
def simpan_semua_perangkat(daftar_perangkat):
    """Menyimpan seluruh list of dictionaries perangkat ke data_perangkat.txt."""
    header = "ID|Nama Alat|Ruangan|Watt Aktif|Watt Standby|Jam Pakai|Rentang Jam|Prioritas\n"
    with open(FILE_PERANGKAT, "w", encoding="utf-8") as f:
        f.write(header)
        for p in daftar_perangkat:
            rentang_jam_str = ",".join(str(j) for j in sorted(p["rentang_jam"]))
            baris = f"{p['id']}|{p['nama']}|{p['ruangan']}|{p['watt_aktif']}|{p['watt_standby']}|{p['jam_pakai']}|{rentang_jam_str}|{p['prioritas']}\n"
            f.write(baris)

# [MATERI: FILE HANDLING - APPEND MODE 'a' UNTUK AUDIT TRAIL]
def catat_log_aktivitas(aktivitas, detail):
    """
    Mencatat riwayat aktivitas perubahan data (TAMBAH / UBAH / HAPUS) ke log_aktivitas.txt
    menggunakan File Handling mode append ('a') disertai timestamp tanggal dan waktu.
    """
    file_ada = os.path.exists(FILE_LOG)
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(FILE_LOG, "a", encoding="utf-8") as f:
            if not file_ada:
                f.write("Timestamp|Aktivitas|Detail\n")
            f.write(f"{waktu_sekarang}|{aktivitas}|{sanitasi_string(detail)}\n")
    except Exception as e:
        print(f"{Warna.MERAH}[!] Gagal mencatat log aktivitas: {e}{Warna.RESET}")

# [MATERI: FILE HANDLING - READ MODE 'r' UNTUK AUDIT TRAIL]
def lihat_log_aktivitas():
    """Membaca dan menampilkan log audit trail dari log_aktivitas.txt ke terminal."""
    if not os.path.exists(FILE_LOG):
        print(f"\n{Warna.KUNING}[i] Belum ada riwayat aktivitas yang tercatat di {FILE_LOG}.{Warna.RESET}")
        return

    print("\n" + "="*85)
    print(f"             {Warna.CYAN}{Warna.TEBAL}RIWAYAT LOG AKTIVITAS (AUDIT TRAIL - log_aktivitas.txt){Warna.RESET}")
    print("="*85)
    try:
        with open(FILE_LOG, "r", encoding="utf-8") as f:
            baris_list = f.readlines()
    except Exception as e:
        print(f"{Warna.MERAH}[!] Gagal membaca file log: {e}{Warna.RESET}")
        return

    if len(baris_list) <= 1:
        print(f"{Warna.KUNING}[i] File log aktivitas masih kosong.{Warna.RESET}")
        print("="*85)
        return

    print(f"{'No':<4} | {'Timestamp':<19} | {'Aktivitas':<10} | {'Detail':<45}")
    print("-" * 85)
    count = 0
    for b in baris_list[1:]:
        b = b.strip()
        if not b:
            continue
        parts = b.split("|")
        if len(parts) >= 3:
            count += 1
            ts = parts[0]
            aksi = parts[1]
            detail = "|".join(parts[2:])
            warna_aksi = Warna.HIJAU if aksi == "TAMBAH" else (Warna.MERAH if aksi == "HAPUS" else Warna.KUNING)
            print(f"{count:<4} | {ts:<19} | {warna_aksi}{aksi:<10}{Warna.RESET} | {detail}")
    print("="*85)

# [MATERI: FUNGSI BANTU GENERATE ID]
def generate_id_baru(daftar_perangkat):
    """Menghasilkan ID unik berurutan seperti EL01, EL02, dst."""
    if not daftar_perangkat:
        return "EL01"
    max_num = 0
    for p in daftar_perangkat:
        id_str = p.get("id", "")
        if id_str.startswith("EL") and id_str[2:].isdigit():
            num = int(id_str[2:])
            if num > max_num:
                max_num = num
    return f"EL{max_num + 1:02d}"

# ==============================================================================
# FITUR CRUD (CREATE, READ, UPDATE, DELETE)
# ==============================================================================

# [FITUR CRUD: 1. CREATE - Dikerjakan oleh Anggota 1 & Anggota 2]
def tambah_perangkat(daftar_perangkat):
    """Fungsi untuk menambahkan perangkat elektronik baru ke dalam sistem."""
    print("\n" + "="*50)
    print(f"       {Warna.CYAN}{Warna.TEBAL}TAMBAH PERANGKAT ELEKTRONIK BARU{Warna.RESET}")
    print("="*50)

    # [MATERI: STRING MANIPULATION - STRIP & SANITASI]
    nama_raw = input("Masukkan Nama Alat (cth: TV LED 43 Inch): ")
    nama = sanitasi_string(nama_raw)
    if not nama:
        print(f"{Warna.MERAH}[!] Nama perangkat tidak boleh kosong!{Warna.RESET}")
        return

    ruang_raw = input("Masukkan Ruangan (cth: Dapur / Kamar Tidur): ")
    ruangan = sanitasi_string(ruang_raw).title()
    if not ruangan:
        ruangan = "Umum"

    # Periksa duplikat berdasarkan kombinasi nama & ruangan
    duplikat = cari_perangkat_duplikat(daftar_perangkat, nama, ruangan)
    if duplikat:
        konfirmasi = input(
            f"{Warna.KUNING}[!] Perangkat dengan nama tersebut sudah ada di "
            f"{duplikat['ruangan']}. Tetap tambahkan? (y/n): {Warna.RESET}"
        ).strip().lower()
        if konfirmasi != "y":
            print(f"{Warna.KUNING}[*] Penambahan perangkat dibatalkan.{Warna.RESET}")
            return

    try:
        watt_aktif = int(input("Daya Aktif saat Menyala (Watt): "))
        if watt_aktif <= 0:
            print(f"{Warna.MERAH}[!] Daya aktif harus lebih besar dari 0 Watt!{Warna.RESET}")
            return

        watt_standby_input = input("Daya Standby saat Dimatikan tapi dicolok (Watt, default 0): ").strip()
        watt_standby = int(watt_standby_input) if watt_standby_input else 0
        if watt_standby < 0:
            print(f"{Warna.MERAH}[!] Daya standby tidak boleh negatif!{Warna.RESET}")
            return

        jam_pakai = int(input("Durasi Penggunaan per Hari (Jam, cth: 4): "))
        if jam_pakai < 0 or jam_pakai > 24:
            print(f"{Warna.MERAH}[!] Durasi jam pakai harus antara 0 sampai 24 jam!{Warna.RESET}")
            return
    except ValueError:
        print(f"{Warna.MERAH}[!] Input daya atau jam harus berupa angka bulat valid!{Warna.RESET}")
        return

    print("Masukkan jam-jam menyala dalam sehari (0 s/d 23).")
    print(f"{Warna.KUNING}Format didukung: koma ('6, 18, 19') atau rentang ('8-12' / '22-4'){Warna.RESET}")
    rentang_input = input("Rentang Jam Menyala: ").strip()

    # [MATERI: STRING PARSING MENGGUNAKAN FUNGSI BANTU]
    rentang_jam = parse_rentang_jam(rentang_input)

    # Sinkronisasi jam_pakai dengan jumlah rentang jam jika rentang jam diisi
    if len(rentang_jam) > 0 and len(rentang_jam) != jam_pakai:
        print(f"[*] Durasi pemakaian disesuaikan otomatis menjadi {len(rentang_jam)} jam sesuai rentang jam aktif.")
        jam_pakai = len(rentang_jam)

    print("\nPilih Tingkat Prioritas Perangkat:")
    print("1. Primer   (Wajib nyala terus, cth: Kulkas, Pompa Air)")
    print("2. Sekunder (Penting harian, cth: AC, Setrika, Rice Cooker)")
    print("3. Tersier  (Hiburan/Pelengkap, cth: TV, Game Console, Dispenser)")
    pilihan_prio = input("Pilihan (1/2/3, default 2): ").strip()
    if pilihan_prio == "1":
        prioritas = "Primer"
    elif pilihan_prio == "3":
        prioritas = "Tersier"
    else:
        prioritas = "Sekunder"

    id_baru = generate_id_baru(daftar_perangkat)

    # [MATERI: DICTIONARY]
    perangkat_baru = {
        "id": id_baru,
        "nama": nama,
        "ruangan": ruangan,
        "watt_aktif": watt_aktif,
        "watt_standby": watt_standby,
        "jam_pakai": jam_pakai,
        "rentang_jam": sorted(rentang_jam),
        "prioritas": prioritas
    }

    # [MATERI: LIST - APPEND]
    daftar_perangkat.append(perangkat_baru)
    simpan_semua_perangkat(daftar_perangkat)

    # [MATERI: FILE HANDLING - PENCATATAN AUDIT TRAIL]
    catat_log_aktivitas(
        "TAMBAH",
        f"ID: {id_baru}, Nama: {nama}, Ruangan: {ruangan}, Watt: {watt_aktif}W, Jam: {jam_pakai}h, Prio: {prioritas}"
    )

    print(f"\n{Warna.HIJAU}[OK] Perangkat '{nama}' berhasil ditambahkan dengan ID {id_baru}!{Warna.RESET}")

# [FITUR CRUD: 2. READ - Dikerjakan oleh Anggota 1]
def tampilkan_tabel_perangkat(daftar_perangkat, tarif_per_kwh=1444.70, judul_filter=None):
    """Menampilkan tabel inventaris perangkat elektronik beserta perhitungan biaya bulanan & kontribusi beban."""
    if not daftar_perangkat:
        print(f"\n{Warna.KUNING}[i] Belum ada data perangkat. Silakan tambahkan perangkat terlebih dahulu.{Warna.RESET}")
        return

    judul = "DAFTAR INVENTARIS PERANGKAT ELEKTRONIK"
    if judul_filter:
        judul += f" (RUANGAN: {judul_filter.upper()})"

    print("\n" + "="*115)
    print(f"{Warna.CYAN}{Warna.TEBAL}{judul:^115}{Warna.RESET}")
    print("="*115)
    print(f"{'ID':<6} | {'Nama Alat':<20} | {'Ruangan':<14} | {'Watt':<6} | {'Jam':<4} | {'kWh/Bulan':<10} | {'Biaya/Bulan':<16} | {'% Beban':<7} | {'Prioritas':<9}")
    print("-"*115)

    total_kwh_bulanan = 0.0
    total_biaya_bulanan = 0.0

    # Hitung total terlebih dahulu untuk persentase
    kalkulasi_list = []
    for p in daftar_perangkat:
        # kWh harian = (Watt_aktif * Jam + Watt_standby * (24 - Jam)) / 1000
        kwh_aktif_hari = (p["watt_aktif"] * p["jam_pakai"]) / 1000.0
        kwh_standby_hari = (p["watt_standby"] * (24 - p["jam_pakai"])) / 1000.0
        kwh_total_bulan = (kwh_aktif_hari + kwh_standby_hari) * 30.0
        biaya_bulan = kwh_total_bulan * tarif_per_kwh

        total_kwh_bulanan += kwh_total_bulan
        total_biaya_bulanan += biaya_bulan
        kalkulasi_list.append((p, kwh_total_bulan, biaya_bulan))

    for p, kwh_bulan, biaya in kalkulasi_list:
        persen = (biaya / total_biaya_bulanan * 100) if total_biaya_bulanan > 0 else 0.0
        nama_pendek = (p["nama"][:18] + "..") if len(p["nama"]) > 20 else p["nama"]
        ruang_pendek = (p["ruangan"][:12] + "..") if len(p["ruangan"]) > 14 else p["ruangan"]
        print(f"{p['id']:<6} | {nama_pendek:<20} | {ruang_pendek:<14} | {p['watt_aktif']:<6} | {p['jam_pakai']:<4} | {kwh_bulan:<10.2f} | {format_rupiah(biaya):<16} | {persen:>6.1f}% | {p['prioritas']:<9}")

    print("-"*115)
    print(f" TOTAL ESTIMASI KONSUMSI : {Warna.TEBAL}{total_kwh_bulanan:.2f} kWh/Bulan{Warna.RESET}")
    print(f" TOTAL ESTIMASI BIAYA    : {Warna.HIJAU}{Warna.TEBAL}{format_rupiah(total_biaya_bulanan)}{Warna.RESET} /Bulan (Tarif: {format_rupiah(tarif_per_kwh)}/kWh)")
    print("="*115)

# [FITUR CRUD: 3. UPDATE - Dikerjakan oleh Anggota 2 & Anggota 1]
def ubah_perangkat(daftar_perangkat):
    """Mengubah data perangkat yang sudah ada berdasarkan ID, termasuk konfirmasi Before vs After Diff."""
    if not daftar_perangkat:
        print(f"\n{Warna.KUNING}[i] Data perangkat masih kosong.{Warna.RESET}")
        return

    print("\n" + "="*50)
    print(f"            {Warna.CYAN}{Warna.TEBAL}UBAH DATA PERANGKAT{Warna.RESET}")
    print("="*50)
    id_target = input("Masukkan ID Perangkat yang ingin diubah (cth: EL01): ").strip().upper()

    # Cari index perangkat
    target_idx = -1
    for i, p in enumerate(daftar_perangkat):
        if p["id"].upper() == id_target:
            target_idx = i
            break

    if target_idx == -1:
        print(f"{Warna.MERAH}[!] Perangkat dengan ID '{id_target}' tidak ditemukan!{Warna.RESET}")
        return

    p_lama = daftar_perangkat[target_idx]
    # Siapkan salinan dictionary agar data lama tidak langsung termutasi
    p_baru = dict(p_lama)
    p_baru["rentang_jam"] = list(p_lama.get("rentang_jam", []))

    rentang_lama_str = ",".join(str(j) for j in sorted(p_lama.get("rentang_jam", [])))
    print(f"\nData Saat Ini:")
    print(f"Nama        : {p_lama['nama']}")
    print(f"Ruangan     : {p_lama['ruangan']}")
    print(f"Watt Aktif  : {p_lama['watt_aktif']} W")
    print(f"Watt Stdby  : {p_lama['watt_standby']} W")
    print(f"Jam Pakai   : {p_lama['jam_pakai']} Jam/Hari")
    print(f"Rentang Jam : {rentang_lama_str or '(kosong)'}")
    print(f"Prioritas   : {p_lama['prioritas']}")
    print("-" * 50)
    print("Tekan ENTER langsung jika tidak ingin mengubah field tertentu.")

    nama_baru = sanitasi_string(input(f"Nama Baru [{p_lama['nama']}]: "))
    ruang_baru = sanitasi_string(input(f"Ruangan Baru [{p_lama['ruangan']}]: ")).title()

    nama_final = nama_baru if nama_baru else p_lama["nama"]
    ruang_final = ruang_baru if ruang_baru else p_lama["ruangan"]

    if nama_baru or ruang_baru:
        duplikat = cari_perangkat_duplikat(
            daftar_perangkat, nama_final, ruang_final, id_dikecualikan=p_lama["id"]
        )
        if duplikat:
            konfirmasi_dup = input(
                f"{Warna.KUNING}[!] Perangkat dengan nama tersebut sudah ada di "
                f"{duplikat['ruangan']} (ID {duplikat['id']}). Tetap simpan? (y/n): {Warna.RESET}"
            ).strip().lower()
            if konfirmasi_dup != "y":
                print(f"{Warna.KUNING}[*] Perubahan dibatalkan.{Warna.RESET}")
                return

    p_baru["nama"] = nama_final
    p_baru["ruangan"] = ruang_final

    watt_input = input(f"Watt Aktif Baru [{p_lama['watt_aktif']}]: ").strip()
    if watt_input.isdigit() and int(watt_input) > 0:
        p_baru["watt_aktif"] = int(watt_input)

    standby_input = input(f"Watt Standby Baru [{p_lama['watt_standby']}]: ").strip()
    if standby_input.isdigit() and int(standby_input) >= 0:
        p_baru["watt_standby"] = int(standby_input)

    rentang_input = input(f"Rentang Jam Baru (cth: 6,18,19 atau 8-12) [{rentang_lama_str}]: ").strip()
    if rentang_input:
        jam_baru_list = parse_rentang_jam(rentang_input)
        p_baru["rentang_jam"] = jam_baru_list
        p_baru["jam_pakai"] = len(jam_baru_list)
        print(f"[*] Rentang jam dan durasi pemakaian disesuaikan ({len(jam_baru_list)} jam).")
    else:
        jam_input = input(f"Durasi Jam Pakai Baru [{p_lama['jam_pakai']}]: ").strip()
        if jam_input.isdigit():
            jam_val = int(jam_input)
            if 0 <= jam_val <= 24:
                p_baru["jam_pakai"] = jam_val

    prio_input = input(f"Prioritas Baru (Primer/Sekunder/Tersier) [{p_lama['prioritas']}]: ").strip().title()
    if prio_input in ["Primer", "Sekunder", "Tersier"]:
        p_baru["prioritas"] = prio_input

    # [FITUR: RINGKASAN PERUBAHAN SEBELUM VS SESUDAH (BEFORE VS AFTER DIFF)]
    rentang_lama_format = ",".join(str(j) for j in sorted(p_lama.get("rentang_jam", []))) or "(kosong)"
    rentang_baru_format = ",".join(str(j) for j in sorted(p_baru.get("rentang_jam", []))) or "(kosong)"

    print("\n" + "="*50)
    print(f"       {Warna.CYAN}{Warna.TEBAL}Ringkasan Perubahan:{Warna.RESET}")
    print("="*50)

    # Periksa dan tampilkan perbandingan tiap atribut
    if p_lama["nama"] != p_baru["nama"]:
        print(f"- Nama        : {p_lama['nama']} -> {p_baru['nama']} {Warna.KUNING}(Berubah){Warna.RESET}")
    else:
        print(f"- Nama        : {p_lama['nama']} (Tetap)")

    if p_lama["ruangan"] != p_baru["ruangan"]:
        print(f"- Ruangan     : {p_lama['ruangan']} -> {p_baru['ruangan']} {Warna.KUNING}(Berubah){Warna.RESET}")
    else:
        print(f"- Ruangan     : {p_lama['ruangan']} (Tetap)")

    if p_lama["watt_aktif"] != p_baru["watt_aktif"]:
        print(f"- Watt Aktif  : {p_lama['watt_aktif']} W -> {p_baru['watt_aktif']} W {Warna.KUNING}(Berubah){Warna.RESET}")
    else:
        print(f"- Watt Aktif  : {p_lama['watt_aktif']} W (Tetap)")

    if p_lama["watt_standby"] != p_baru["watt_standby"]:
        print(f"- Watt Standby: {p_lama['watt_standby']} W -> {p_baru['watt_standby']} W {Warna.KUNING}(Berubah){Warna.RESET}")
    else:
        print(f"- Watt Standby: {p_lama['watt_standby']} W (Tetap)")

    if p_lama["jam_pakai"] != p_baru["jam_pakai"]:
        print(f"- Jam Pakai   : {p_lama['jam_pakai']} Jam -> {p_baru['jam_pakai']} Jam {Warna.KUNING}(Berubah){Warna.RESET}")
    else:
        print(f"- Jam Pakai   : {p_lama['jam_pakai']} Jam (Tetap)")

    if sorted(p_lama.get("rentang_jam", [])) != sorted(p_baru.get("rentang_jam", [])):
        print(f"- Rentang Jam : {rentang_lama_format} -> {rentang_baru_format} {Warna.KUNING}(Berubah){Warna.RESET}")
    else:
        print(f"- Rentang Jam : {rentang_lama_format} (Tetap)")

    if p_lama["prioritas"] != p_baru["prioritas"]:
        print(f"- Prioritas   : {p_lama['prioritas']} -> {p_baru['prioritas']} {Warna.KUNING}(Berubah){Warna.RESET}")
    else:
        print(f"- Prioritas   : {p_lama['prioritas']} (Tetap)")

    print("="*50)
    konfirmasi = input(f"{Warna.TEBAL}Simpan perubahan ke file? (y/n): {Warna.RESET}").strip().lower()

    if konfirmasi == "y":
        daftar_perangkat[target_idx] = p_baru
        simpan_semua_perangkat(daftar_perangkat)
        catat_log_aktivitas(
            "UBAH",
            f"ID: {p_baru['id']}, Nama: {p_baru['nama']}, Ruangan: {p_baru['ruangan']}, Watt: {p_baru['watt_aktif']}W, Jam: {p_baru['jam_pakai']}h"
        )
        print(f"\n{Warna.HIJAU}[OK] Perangkat ID '{p_baru['id']}' berhasil diperbarui dan disimpan ke file!{Warna.RESET}")
    else:
        print(f"\n{Warna.KUNING}[*] Perubahan dibatalkan. Data lama tetap dipertahankan.{Warna.RESET}")

# [FITUR CRUD: 4. DELETE - Dikerjakan oleh Anggota 2]
def hapus_perangkat(daftar_perangkat):
    """Menghapus perangkat dari daftar dan memperbarui file data_perangkat.txt serta mencatat audit trail."""
    if not daftar_perangkat:
        print(f"\n{Warna.KUNING}[i] Data perangkat masih kosong.{Warna.RESET}")
        return

    print("\n" + "="*50)
    print(f"            {Warna.CYAN}{Warna.TEBAL}HAPUS DATA PERANGKAT{Warna.RESET}")
    print("="*50)
    id_target = input("Masukkan ID Perangkat yang akan dihapus (cth: EL01): ").strip().upper()

    target_idx = -1
    for i, p in enumerate(daftar_perangkat):
        if p["id"].upper() == id_target:
            target_idx = i
            break

    if target_idx == -1:
        print(f"{Warna.MERAH}[!] Perangkat dengan ID '{id_target}' tidak ditemukan!{Warna.RESET}")
        return

    perangkat_dihapus = daftar_perangkat[target_idx]
    konfirmasi = input(
        f"Apakah Anda yakin ingin menghapus '{perangkat_dihapus['nama']}' "
        f"({perangkat_dihapus['id']} - {perangkat_dihapus['ruangan']})? (y/n): "
    ).strip().lower()

    if konfirmasi == "y":
        # [MATERI: LIST - POP / REMOVE]
        dihapus = daftar_perangkat.pop(target_idx)
        simpan_semua_perangkat(daftar_perangkat)
        catat_log_aktivitas(
            "HAPUS",
            f"ID: {dihapus['id']}, Nama: {dihapus['nama']}, Ruangan: {dihapus['ruangan']}, Daya: {dihapus['watt_aktif']}W"
        )
        print(f"\n{Warna.HIJAU}[OK] Perangkat '{dihapus['nama']}' ({dihapus['id']}) berhasil dihapus dan dicatat di log aktivitas!{Warna.RESET}")
    else:
        print(f"\n{Warna.KUNING}[*] Penghapusan dibatalkan.{Warna.RESET}")
