# ==============================================================================
# MODUL ANALISIS, SIMULASI & OPTIMASI (modul_analisis.py)
# Bagian Tanggung Jawab:
# - Anggota 2: Searching, Sorting Manual, Operasi Set (Himpunan)
# - Anggota 3: Simulasi Matriks Beban 24 Jam (Nested Loop), Detektor Vampire Power,
#              Audit Ruangan & Export Laporan ke laporan_audit.txt
# ==============================================================================

from modul_crud import format_rupiah

# ==============================================================================
# [BAGIAN ANGGOTA 2: OPERASI SET (HIMPUNAN)]
# ==============================================================================

# [MATERI: SET - MENYIMPAN NILAI UNIK]
def ambil_himpunan_ruangan(daftar_perangkat):
    """
    Mengambil daftar seluruh ruangan unik dari inventaris perangkat.
    Menggunakan tipe data Set untuk menjamin tidak ada duplikasi.
    """
    set_ruangan = set()
    for p in daftar_perangkat:
        set_ruangan.add(p["ruangan"])
    return set_ruangan

# [MATERI: SET - OPERASI INTERSECTION (&)]
def deteksi_bentrok_jam_perangkat(perangkat_a, perangkat_b):
    """
    Mendeteksi jam berapa saja dua perangkat menyala secara bersamaan.
    Menggunakan operasi irisan himpunan (Set Intersection).
    """
    set_jam_a = set(perangkat_a.get("rentang_jam", []))
    set_jam_b = set(perangkat_b.get("rentang_jam", []))
    # [MATERI: SET INTERSECTION]
    irisan_jam = set_jam_a.intersection(set_jam_b)
    return sorted(list(irisan_jam))

# [MATERI: SET - OPERASI DIFFERENCE (-)]
def deteksi_perangkat_boros(daftar_perangkat, ambang_aktif=200, ambang_standby=15):
    """
    Memisahkan perangkat hemat energi vs perangkat boros menggunakan Set Difference.
    Perangkat hemat: watt_aktif <= ambang_aktif DAN watt_standby <= ambang_standby.
    """
    set_semua_id = {p["id"] for p in daftar_perangkat}
    set_hemat_id = {
        p["id"] for p in daftar_perangkat
        if p["watt_aktif"] <= ambang_aktif and p["watt_standby"] <= ambang_standby
    }
    # [MATERI: SET DIFFERENCE]
    set_boros_id = set_semua_id.difference(set_hemat_id)

    list_boros = [p for p in daftar_perangkat if p["id"] in set_boros_id]
    return list_boros

# ==============================================================================
# [BAGIAN ANGGOTA 2: SEARCHING (PENCARIAN MANUAL)]
# ==============================================================================

# [MATERI: SEARCHING - LINEAR SEARCH BERDASARKAN KATA KUNCI NAMA]
def cari_perangkat_nama(daftar_perangkat, keyword):
    """
    Mencari perangkat dengan algoritma Linear Search berdasarkan kata kunci nama.
    Case-insensitive dan mencocokkan substring.
    """
    hasil = []
    keyword_clean = keyword.strip().lower()
    for p in daftar_perangkat:
        if keyword_clean in p["nama"].lower():
            hasil.append(p)
    return hasil

# [MATERI: SEARCHING - LINEAR SEARCH BERDASARKAN RUANGAN]
def cari_perangkat_ruangan(daftar_perangkat, nama_ruangan):
    """Mencari seluruh perangkat yang berada di ruangan tertentu."""
    hasil = []
    ruangan_clean = nama_ruangan.strip().lower()
    for p in daftar_perangkat:
        if ruangan_clean == p["ruangan"].lower():
            hasil.append(p)
    return hasil

# [MATERI: SEARCHING - FILTER BERDASARKAN MINIMAL DAYA WATT]
def cari_perangkat_daya_tinggi(daftar_perangkat, min_watt):
    """Mencari perangkat yang memiliki daya aktif >= min_watt."""
    hasil = []
    for p in daftar_perangkat:
        if p["watt_aktif"] >= min_watt:
            hasil.append(p)
    return hasil

# ==============================================================================
# [BAGIAN ANGGOTA 2: SORTING (PENGURUTAN MANUAL - BUBBLE SORT)]
# ==============================================================================

# [MATERI: SORTING - MANUAL BUBBLE SORT BERDASARKAN ESTIMASI BIAYA]
def urutkan_perangkat_biaya(daftar_perangkat, tarif_per_kwh=1444.70, descending=True):
    """
    Mengurutkan perangkat berdasarkan biaya bulanan menggunakan Bubble Sort manual.
    descending=True untuk mengurutkan dari yang paling boros ke paling hemat.
    """
    # Salin list agar tidak mengubah data asli secara langsung
    data = list(daftar_perangkat)
    n = len(data)

    def hitung_biaya(p):
        kwh = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
        return kwh * tarif_per_kwh

    # [MATERI: NESTED LOOP PADA BUBBLE SORT]
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            biaya_j = hitung_biaya(data[j])
            biaya_next = hitung_biaya(data[j + 1])
            kondisi = (biaya_j < biaya_next) if descending else (biaya_j > biaya_next)
            if kondisi:
                # Swap elemen
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

# [MATERI: SORTING - MANUAL BUBBLE SORT BERDASARKAN VAMPIRE POWER]
def urutkan_perangkat_vampire(daftar_perangkat, descending=True):
    """
    Mengurutkan perangkat berdasarkan daya standby (Vampire Power) terbesar.
    """
    data = list(daftar_perangkat)
    n = len(data)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            val_a = data[j]["watt_standby"]
            val_b = data[j + 1]["watt_standby"]
            kondisi = (val_a < val_b) if descending else (val_a > val_b)
            if kondisi:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data

# [MATERI: SORTING - MANUAL SELECTION SORT BERDASARKAN PRIORITAS]
def urutkan_perangkat_prioritas(daftar_perangkat):
    """
    Mengurutkan perangkat berdasarkan tingkat kepentingan:
    Primer (1) -> Sekunder (2) -> Tersier (3)
    Menggunakan Selection Sort manual.
    """
    bobot = {"Primer": 1, "Sekunder": 2, "Tersier": 3}
    data = list(daftar_perangkat)
    n = len(data)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            bobot_j = bobot.get(data[j]["prioritas"], 99)
            bobot_min = bobot.get(data[min_idx]["prioritas"], 99)
            if bobot_j < bobot_min:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    return data


# ==============================================================================
# [BAGIAN ANGGOTA 3: PERULANGAN BERSARANG (NESTED LOOP) & AUDIT LISTRIK]
# ==============================================================================

# [MATERI: NESTED LOOP - SIMULASI BEBAN 24 JAM & ANTI-JEGLEK]
def simulasi_beban_24jam(daftar_perangkat, batas_watt_aman=1100, va_maks=1300):
    """
    Mensimulasikan beban listrik rumah tangga selama 24 jam penuh (00:00 s/d 23:00).
    Outer Loop mengiterasi 24 jam.
    Inner Loop mengiterasi setiap perangkat yang aktif pada jam tersebut.
    """
    print("\n" + "="*85)
    print("        SIMULASI MATRIKS BEBAN LISTRIK 24 JAM (DETEKTOR ANTI-JEGLEK)")
    print(f"        Batas Daya Aman: {batas_watt_aman} Watt | Kapasitas Terpasang: {va_maks} VA")
    print("="*85)
    print(f"{'Jam':<7} | {'Beban (Watt)':<12} | {'Visualisasi Beban (ASCII Bar)':<35} | {'Status'}")
    print("-"*85)

    jam_overload = []
    rincian_per_jam = {}

    # [MATERI: NESTED LOOP - OUTER LOOP: ITERASI JAM 0-23]
    for jam in range(24):
        total_watt_jam = 0
        alat_menyala = []

        # [MATERI: NESTED LOOP - INNER LOOP: ITERASI SELURUH PERANGKAT]
        for p in daftar_perangkat:
            # Jika rentang_jam kosong atau jam termasuk rentang aktif
            if jam in p.get("rentang_jam", []):
                total_watt_jam += p["watt_aktif"]
                alat_menyala.append(p["nama"])
            else:
                # Saat mati tapi kabel tertancap, menyerap daya standby
                total_watt_jam += p.get("watt_standby", 0)

        rincian_per_jam[jam] = (total_watt_jam, alat_menyala)

        # Gambar Grafik Bar ASCII
        # Skala: 30 karakter maksimal
        persen = min(total_watt_jam / batas_watt_aman, 1.5)
        bar_len = int(persen * 20)
        bar_str = "█" * min(bar_len, 20) + "░" * max(0, 20 - bar_len)

        if total_watt_jam > batas_watt_aman:
            status = " [!] OVERLOAD (RISIKO JEGLEK)"
            jam_overload.append((jam, total_watt_jam, alat_menyala))
        elif total_watt_jam > (batas_watt_aman * 0.8):
            status = " [*] WASPADA (>80%)"
        else:
            status = " [v] AMAN"

        print(f"{jam:02d}:00   | {total_watt_jam:>5} Watt    | [{bar_str:<20}] {int(persen*100):>3}% |{status}")

    print("="*85)

    # Analisis dan Rekomendasi jika ada jam yang Jeglek
    if jam_overload:
        print("\n" + "!"*85)
        print(" PERINGATAN POTENSI MCB TRIP (LISTRIK JEGLEK) DITEMUKAN!")
        print("!"*85)
        for jam, watt, alat in jam_overload:
            print(f"-> Jam {jam:02d}:00 : Total Beban {watt} W melebihi kapasitas aman {batas_watt_aman} W.")
            print(f"   Alat yang menyala bersamaan: {', '.join(alat)}")
            print("   Saran Tindakan: Hindari menyalakan alat daya besar (seperti Setrika/Rice Cooker/AC) secara bersamaan.")
            print("                   Geser waktu pemakaian alat fleksibel ke jam dengan beban rendah.")
    else:
        print("\n[v] KONDISI AMAN: Tidak ditemukan jam dengan potensi listrik jeglek.")

    return rincian_per_jam

# [MATERI: NESTED LOOP - AUDIT PER RUANGAN X PERANGKAT]
def audit_per_ruangan(daftar_perangkat, tarif_per_kwh=1444.70):
    """
    Menampilkan rincian perangkat per ruangan beserta subtotal konsumsi daya dan biaya.
    Outer Loop: Setiap ruangan unik.
    Inner Loop: Setiap perangkat di dalam ruangan tersebut.
    """
    set_ruangan = ambil_himpunan_ruangan(daftar_perangkat)
    if not set_ruangan:
        print("\n[i] Tidak ada data perangkat untuk diaudit.")
        return

    print("\n" + "="*80)
    print("                    AUDIT KONSUMSI LISTRIK PER RUANGAN")
    print("="*80)

    # [MATERI: NESTED LOOP - OUTER LOOP: ITERASI RUANGAN]
    for ruangan in sorted(set_ruangan):
        print(f"\n Ruangan: [{ruangan.upper()}]")
        print(f" {'ID':<6} | {'Nama Alat':<25} | {'Aktif':<8} | {'Jam':<5} | {'Biaya/Bulan'}")
        print(" " + "-"*65)

        subtotal_watt = 0
        subtotal_biaya = 0.0

        # [MATERI: NESTED LOOP - INNER LOOP: ITERASI PERANGKAT DI RUANGAN ITU]
        for p in daftar_perangkat:
            if p["ruangan"] == ruangan:
                kwh_bulan = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
                biaya = kwh_bulan * tarif_per_kwh
                subtotal_watt += p["watt_aktif"]
                subtotal_biaya += biaya
                print(f" {p['id']:<6} | {p['nama']:<25} | {p['watt_aktif']:<5} W | {p['jam_pakai']:<2} j  | {format_rupiah(biaya)}")

        print(" " + "-"*65)
        print(f" Subtotal Ruang {ruangan}: Total Daya Aktif = {subtotal_watt} W | Biaya = {format_rupiah(subtotal_biaya)}/Bulan")

    print("="*80)

# [MATERI: PERHITUNGAN VAMPIRE POWER / DAYA STANDBY]
def analisis_vampire_power(daftar_perangkat, tarif_per_kwh=1444.70):
    """
    Menghitung kebocoran energi akibat perangkat yang tetap menyedot listrik
    saat standby (colokan tidak dicabut).
    """
    print("\n" + "="*85)
    print("        DETEKTOR VAMPIRE POWER (KEBOCORAN DAYA STANDBY LISTRIK)")
    print("="*85)
    print(f"{'ID':<6} | {'Nama Alat':<22} | {'Stdby (W)':<10} | {'Jam Idle':<9} | {'kWh/Bulan':<10} | {'Rupiah Terbuang/Thn'}")
    print("-"*85)

    total_kwh_vampire_bulan = 0.0
    total_rugi_tahunan = 0.0

    for p in daftar_perangkat:
        standby_w = p.get("watt_standby", 0)
        jam_idle = 24 - p["jam_pakai"]
        if standby_w > 0 and jam_idle > 0:
            kwh_bulan = (standby_w * jam_idle * 30) / 1000.0
            rugi_bulan = kwh_bulan * tarif_per_kwh
            rugi_tahun = rugi_bulan * 12

            total_kwh_vampire_bulan += kwh_bulan
            total_rugi_tahunan += rugi_tahun

            print(f"{p['id']:<6} | {p['nama']:<22} | {standby_w:>6} W   | {jam_idle:>4} jam  | {kwh_bulan:>8.2f}   | {format_rupiah(rugi_tahun)}")

    print("-"*85)
    print(f" TOTAL KEBOCORAN DAYA STANDBY : {total_kwh_vampire_bulan:.2f} kWh/Bulan")
    print(f" TOTAL UANG TERBUANG SIA-SIA   : {format_rupiah(total_kwh_vampire_bulan * tarif_per_kwh)}/Bulan")
    print(f"                                 atau {format_rupiah(total_rugi_tahunan)}/Tahun!")
    print("\n[TIPS HEMAT] Cabut colokan TV, microwave, charger, dan dispenser saat tidak dipakai,")
    print("             atau gunakan stopkontak switch on/off agar tidak ada arus standby.")
    print("="*85)

# [MATERI: FILE HANDLING - EXPORT LAPORAN AUDIT KE FILE .TXT]
def export_laporan_audit(daftar_perangkat, profil_rumah, nama_file="laporan_audit.txt"):
    """
    Menyusun laporan audit listrik rumah tangga lengkap dan menyimpannya ke dalam file teks.
    """
    tarif = profil_rumah["tarif"]
    batas = profil_rumah["batas_watt"]

    total_kwh_bulan = 0.0
    total_biaya_bulan = 0.0
    total_vampire_rugi = 0.0

    lines = []
    lines.append("="*75 + "\n")
    lines.append("             LAPORAN RESMI AUDIT KELISTRIKAN RUMAH TANGGA\n")
    lines.append("                       APLIKASI WATTWISE HOME\n")
    lines.append("="*75 + "\n\n")

    lines.append(f"GOLONGAN LISTRIK PLN : {profil_rumah['golongan']} ({profil_rumah['va']} VA)\n")
    lines.append(f"BATAS AMAN BEBAN     : {batas} Watt\n")
    lines.append(f"TARIF PER KWH        : {format_rupiah(tarif)} /kWh\n")
    lines.append(f"SISA TOKEN SAAT INI  : {profil_rumah['sisa_token_kwh']:.2f} kWh\n")
    lines.append("-"*75 + "\n\n")

    lines.append("RINCIAN PERANGKAT ELEKTRONIK:\n")
    lines.append(f"{'ID':<6} | {'Nama Alat':<22} | {'Ruang':<12} | {'Watt':<6} | {'Jam':<4} | {'Biaya/Bulan'}\n")
    lines.append("-"*75 + "\n")

    for p in daftar_perangkat:
        kwh = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
        biaya = kwh * tarif
        total_kwh_bulan += kwh
        total_biaya_bulan += biaya

        jam_idle = 24 - p["jam_pakai"]
        if p["watt_standby"] > 0 and jam_idle > 0:
            total_vampire_rugi += (p["watt_standby"] * jam_idle * 30 / 1000.0) * tarif * 12

        lines.append(f"{p['id']:<6} | {p['nama']:<22} | {p['ruangan']:<12} | {p['watt_aktif']:<6} | {p['jam_pakai']:<4} | {format_rupiah(biaya)}\n")

    lines.append("-"*75 + "\n")
    lines.append(f"TOTAL ESTIMASI BIAYA LISTRIK : {format_rupiah(total_biaya_bulan)} / Bulan\n")
    lines.append(f"TOTAL KONSUMSI LISTRIK       : {total_kwh_bulan:.2f} kWh / Bulan\n")
    lines.append(f"POTENSI RUGI VAMPIRE POWER   : {format_rupiah(total_vampire_rugi)} / Tahun\n\n")
    lines.append("CATATAN AUDITOR:\n")
    lines.append("- Matikan alat elektronika saat jam beban puncak (18:00 - 21:00).\n")
    lines.append("- Cabut stopkontak perangkat yang memiliki daya standby tinggi.\n")
    lines.append("="*75 + "\n")

    try:
        with open(nama_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"\n[OK] Laporan audit berhasil diekspor ke file '{nama_file}'!")
    except Exception as e:
        print(f"[!] Gagal mengekspor laporan: {e}")
