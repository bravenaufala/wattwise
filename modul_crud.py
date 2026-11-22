# ==============================================================================
# MODUL CRUD & FILE HANDLING (modul_crud.py)
# Bagian Tanggung Jawab:
# - Anggota 1: Core Data, File Handling, Create (Tambah), Read (Tampil)
# - Anggota 2: Update (Ubah), Delete (Hapus) & Validasi ID
# ==============================================================================

import os

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

# [MATERI: STRING MANIPULATION - SANITASI INPUT FILE]
def sanitasi_string(teks):
    """
    Menghilangkan karakter delimiter pipe '|' agar struktur file teks tidak rusak,
    serta membersihkan spasi berlebih di awal dan akhir string.
    """
    if not teks:
        return ""
    return teks.replace("|", "/").strip()

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

    print(f"\n{Warna.HIJAU}[OK] Perangkat '{nama}' berhasil ditambahkan dengan ID {id_baru}!{Warna.RESET}")

# [FITUR CRUD: 2. READ - Dikerjakan oleh Anggota 1]
def tampilkan_tabel_perangkat(daftar_perangkat, tarif_per_kwh=1444.70):
    """Menampilkan tabel inventaris perangkat elektronik beserta perhitungan biaya bulanan & kontribusi beban."""
    if not daftar_perangkat:
        print(f"\n{Warna.KUNING}[i] Belum ada data perangkat. Silakan tambahkan perangkat terlebih dahulu.{Warna.RESET}")
        return

    print("\n" + "="*115)
    print(f"                             {Warna.CYAN}{Warna.TEBAL}DAFTAR INVENTARIS PERANGKAT ELEKTRONIK{Warna.RESET}")
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
    """Mengubah data perangkat yang sudah ada berdasarkan ID, termasuk rentang jam operasional."""
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

    p = daftar_perangkat[target_idx]
    rentang_lama_str = ",".join(str(j) for j in sorted(p.get("rentang_jam", [])))
    print(f"\nData Saat Ini:")
    print(f"Nama        : {p['nama']}")
    print(f"Ruangan     : {p['ruangan']}")
    print(f"Watt Aktif  : {p['watt_aktif']} W")
    print(f"Watt Stdby  : {p['watt_standby']} W")
    print(f"Jam Pakai   : {p['jam_pakai']} Jam/Hari")
    print(f"Rentang Jam : {rentang_lama_str or '(kosong)'}")
    print(f"Prioritas   : {p['prioritas']}")
    print("-" * 50)
    print("Tekan ENTER langsung jika tidak ingin mengubah field tertentu.")

    nama_baru = sanitasi_string(input(f"Nama Baru [{p['nama']}]: "))
    if nama_baru:
        p["nama"] = nama_baru

    ruang_baru = sanitasi_string(input(f"Ruangan Baru [{p['ruangan']}]: ")).title()
    if ruang_baru:
        p["ruangan"] = ruang_baru

    watt_input = input(f"Watt Aktif Baru [{p['watt_aktif']}]: ").strip()
    if watt_input.isdigit() and int(watt_input) > 0:
        p["watt_aktif"] = int(watt_input)

    standby_input = input(f"Watt Standby Baru [{p['watt_standby']}]: ").strip()
    if standby_input.isdigit() and int(standby_input) >= 0:
        p["watt_standby"] = int(standby_input)

    rentang_input = input(f"Rentang Jam Baru (cth: 6,18,19 atau 8-12) [{rentang_lama_str}]: ").strip()
    if rentang_input:
        jam_baru_list = parse_rentang_jam(rentang_input)
        p["rentang_jam"] = jam_baru_list
        p["jam_pakai"] = len(jam_baru_list)
        print(f"[*] Rentang jam dan durasi pemakaian diperbarui ({len(jam_baru_list)} jam).")
    else:
        jam_input = input(f"Durasi Jam Pakai Baru [{p['jam_pakai']}]: ").strip()
        if jam_input.isdigit():
            jam_val = int(jam_input)
            if 0 <= jam_val <= 24:
                p["jam_pakai"] = jam_val

    prio_input = input(f"Prioritas Baru (Primer/Sekunder/Tersier) [{p['prioritas']}]: ").strip().title()
    if prio_input in ["Primer", "Sekunder", "Tersier"]:
        p["prioritas"] = prio_input

    simpan_semua_perangkat(daftar_perangkat)
    print(f"\n{Warna.HIJAU}[OK] Perangkat ID '{p['id']}' berhasil diperbarui!{Warna.RESET}")

# [FITUR CRUD: 4. DELETE - Dikerjakan oleh Anggota 2]
# [TODO: Refine Anggota 2 - Tambahkan konfirmasi penghapusan (Y/N) dengan rincian nama alat]
def hapus_perangkat(daftar_perangkat):
    """Menghapus perangkat dari daftar dan memperbarui file data_perangkat.txt."""
    if not daftar_perangkat:
        print("\n[i] Data perangkat masih kosong.")
        return

    print("\n" + "="*50)
    print("            HAPUS DATA PERANGKAT")
    print("="*50)
    id_target = input("Masukkan ID Perangkat yang akan dihapus (cth: EL01): ").strip().upper()

    target_idx = -1
    for i, p in enumerate(daftar_perangkat):
        if p["id"].upper() == id_target:
            target_idx = i
            break

    if target_idx == -1:
        print(f"[!] Perangkat dengan ID '{id_target}' tidak ditemukan!")
        return

    perangkat_dihapus = daftar_perangkat[target_idx]
    konfirmasi = input(f"Apakah Anda yakin ingin menghapus '{perangkat_dihapus['nama']}' ({perangkat_dihapus['id']})? (y/n): ").strip().lower()

    if konfirmasi == "y":
        # [MATERI: LIST - POP / REMOVE]
        daftar_perangkat.pop(target_idx)
        simpan_semua_perangkat(daftar_perangkat)
        print(f"\n[OK] Perangkat '{perangkat_dihapus['nama']}' berhasil dihapus!")
    else:
        print("[*] Penghapusan dibatalkan.")
