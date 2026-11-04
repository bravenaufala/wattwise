# ==============================================================================
# MODUL CRUD & FILE HANDLING (modul_crud.py)
# Bagian Tanggung Jawab:
# - Anggota 1: Core Data, File Handling, Create (Tambah), Read (Tampil)
# - Anggota 2: Update (Ubah), Delete (Hapus) & Validasi ID
# ==============================================================================

import os

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
        baris = f"{golongan}|{va}|{batas_watt}|{tarif}|{sisa_token_kwh}\n"
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

# [FITUR CRUD: 1. CREATE - Dikerjakan oleh Anggota 1]
# [TODO: Refine Anggota 1 - Validasi tambahan untuk input jam di luar rentang 0-23]
def tambah_perangkat(daftar_perangkat):
    """Fungsi untuk menambahkan perangkat elektronik baru ke dalam sistem."""
    print("\n" + "="*50)
    print("       TAMBAH PERANGKAT ELEKTRONIK BARU")
    print("="*50)

    # [MATERI: STRING MANIPULATION - STRIP & TITLE]
    nama = input("Masukkan Nama Alat (cth: TV LED 43 Inch): ").strip()
    if not nama:
        print("[!] Nama perangkat tidak boleh kosong!")
        return

    ruangan = input("Masukkan Ruangan (cth: Dapur / Kamar Tidur): ").strip().title()
    if not ruangan:
        ruangan = "Umum"

    try:
        watt_aktif = int(input("Daya Aktif saat Menyala (Watt): "))
        watt_standby = int(input("Daya Standby saat Dimatikan tapi dicolok (Watt, default 0): ") or "0")
        jam_pakai = int(input("Durasi Penggunaan per Hari (Jam, cth: 4): "))
        if jam_pakai < 0 or jam_pakai > 24:
            print("[!] Durasi jam pakai harus antara 0 sampai 24 jam!")
            return
    except ValueError:
        print("[!] Input daya atau jam harus berupa angka bulat valid!")
        return

    print("Masukkan jam-jam menyala dalam sehari (0 s/d 23, pisahkan dengan koma).")
    print("Contoh: jika menyala jam 6 pagi dan jam 7 malam, ketik: 6, 19")
    rentang_input = input("Rentang Jam Menyala: ").strip()

    rentang_jam = []
    if rentang_input:
        for bagian in rentang_input.split(","):
            bagian = bagian.strip()
            if bagian.isdigit():
                jam_val = int(bagian)
                if 0 <= jam_val <= 23:
                    if jam_val not in rentang_jam:
                        rentang_jam.append(jam_val)
                else:
                    print(f"[!] Abaikan jam di luar rentang (0-23): {jam_val}")

    # Sinkronisasi jam_pakai dengan jumlah rentang jam jika belum sesuai
    if len(rentang_jam) > 0 and len(rentang_jam) != jam_pakai:
        print(f"[*] Durasi pemakaian disesuaikan otomatis menjadi {len(rentang_jam)} jam.")
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

    print(f"\n[OK] Perangkat '{nama}' berhasil ditambahkan dengan ID {id_baru}!")

# [FITUR CRUD: 2. READ - Dikerjakan oleh Anggota 1]
# [TODO: Refine Anggota 1 - Menambahkan opsi paging atau filter per ruangan langsung di tabel]
def tampilkan_tabel_perangkat(daftar_perangkat, tarif_per_kwh=1444.70):
    """Menampilkan tabel inventaris perangkat elektronik beserta perhitungan biaya bulanan."""
    if not daftar_perangkat:
        print("\n[i] Belum ada data perangkat. Silakan tambahkan perangkat terlebih dahulu.")
        return

    print("\n" + "="*105)
    print("                              DAFTAR INVENTARIS PERANGKAT ELEKTRONIK")
    print("="*105)
    print(f"{'ID':<6} | {'Nama Alat':<20} | {'Ruangan':<14} | {'Watt':<6} | {'Jam':<4} | {'kWh/Bulan':<10} | {'Biaya/Bulan':<16} | {'Prioritas':<9}")
    print("-"*105)

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
        nama_pendek = (p["nama"][:18] + "..") if len(p["nama"]) > 20 else p["nama"]
        ruang_pendek = (p["ruangan"][:12] + "..") if len(p["ruangan"]) > 14 else p["ruangan"]
        print(f"{p['id']:<6} | {nama_pendek:<20} | {ruang_pendek:<14} | {p['watt_aktif']:<6} | {p['jam_pakai']:<4} | {kwh_bulan:<10.2f} | {format_rupiah(biaya):<16} | {p['prioritas']:<9}")

    print("-"*105)
    print(f" TOTAL ESTIMASI KONSUMSI : {total_kwh_bulanan:.2f} kWh/Bulan")
    print(f" TOTAL ESTIMASI BIAYA    : {format_rupiah(total_biaya_bulanan)} /Bulan (Tarif: {format_rupiah(tarif_per_kwh)}/kWh)")
    print("="*105)

# [FITUR CRUD: 3. UPDATE - Dikerjakan oleh Anggota 2]
# [TODO: Refine Anggota 2 - Tambahkan fitur ubah jam menyala spesifik (rentang jam)]
def ubah_perangkat(daftar_perangkat):
    """Mengubah data perangkat yang sudah ada berdasarkan ID."""
    if not daftar_perangkat:
        print("\n[i] Data perangkat masih kosong.")
        return

    print("\n" + "="*50)
    print("            UBAH DATA PERANGKAT")
    print("="*50)
    id_target = input("Masukkan ID Perangkat yang ingin diubah (cth: EL01): ").strip().upper()

    # Cari index perangkat
    target_idx = -1
    for i, p in enumerate(daftar_perangkat):
        if p["id"].upper() == id_target:
            target_idx = i
            break

    if target_idx == -1:
        print(f"[!] Perangkat dengan ID '{id_target}' tidak ditemukan!")
        return

    p = daftar_perangkat[target_idx]
    print(f"\nData Saat Ini:")
    print(f"Nama       : {p['nama']}")
    print(f"Ruangan    : {p['ruangan']}")
    print(f"Watt Aktif : {p['watt_aktif']} W")
    print(f"Watt Stdby : {p['watt_standby']} W")
    print(f"Jam Pakai  : {p['jam_pakai']} Jam/Hari")
    print(f"Prioritas  : {p['prioritas']}")
    print("-" * 50)
    print("Tekan ENTER langsung jika tidak ingin mengubah field tertentu.")

    nama_baru = input(f"Nama Baru [{p['nama']}]: ").strip()
    if nama_baru:
        p["nama"] = nama_baru

    ruang_baru = input(f"Ruangan Baru [{p['ruangan']}]: ").strip().title()
    if ruang_baru:
        p["ruangan"] = ruang_baru

    watt_input = input(f"Watt Aktif Baru [{p['watt_aktif']}]: ").strip()
    if watt_input.isdigit():
        p["watt_aktif"] = int(watt_input)

    standby_input = input(f"Watt Standby Baru [{p['watt_standby']}]: ").strip()
    if standby_input.isdigit():
        p["watt_standby"] = int(standby_input)

    jam_input = input(f"Durasi Jam Pakai Baru [{p['jam_pakai']}]: ").strip()
    if jam_input.isdigit():
        jam_baru = int(jam_input)
        if 0 <= jam_baru <= 24:
            p["jam_pakai"] = jam_baru

    prio_input = input(f"Prioritas Baru (Primer/Sekunder/Tersier) [{p['prioritas']}]: ").strip().title()
    if prio_input in ["Primer", "Sekunder", "Tersier"]:
        p["prioritas"] = prio_input

    simpan_semua_perangkat(daftar_perangkat)
    print(f"\n[OK] Perangkat ID '{p['id']}' berhasil diperbarui!")

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
