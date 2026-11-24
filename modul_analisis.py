from modul_crud import format_rupiah, Warna


def ambil_himpunan_ruangan(daftar_perangkat):
    set_ruangan = set()
    for p in daftar_perangkat:
        set_ruangan.add(p["ruangan"])
    return set_ruangan


def deteksi_bentrok_jam_perangkat(perangkat_a, perangkat_b):
    set_jam_a = set(perangkat_a.get("rentang_jam", []))
    set_jam_b = set(perangkat_b.get("rentang_jam", []))
    irisan_jam = set_jam_a.intersection(set_jam_b)
    return sorted(list(irisan_jam))


def deteksi_perangkat_boros(daftar_perangkat, ambang_aktif=200, ambang_standby=15):
    set_semua_id = {p["id"] for p in daftar_perangkat}
    set_hemat_id = {
        p["id"] for p in daftar_perangkat
        if p["watt_aktif"] <= ambang_aktif and p["watt_standby"] <= ambang_standby
    }
    set_boros_id = set_semua_id.difference(set_hemat_id)
    return [p for p in daftar_perangkat if p["id"] in set_boros_id]


def gabungkan_jam_aktif_ruangan(daftar_perangkat, ruang_a, ruang_b=None):
    set_jam_a = set()
    set_jam_b = set()

    for p in daftar_perangkat:
        if p["ruangan"].lower() == ruang_a.strip().lower():
            set_jam_a = set_jam_a.union(set(p.get("rentang_jam", [])))
        elif ruang_b and p["ruangan"].lower() == ruang_b.strip().lower():
            set_jam_b = set_jam_b.union(set(p.get("rentang_jam", [])))

    if ruang_b:
        gabungan = set_jam_a.union(set_jam_b)
        return sorted(list(gabungan)), sorted(list(set_jam_a)), sorted(list(set_jam_b))
    return sorted(list(set_jam_a)), sorted(list(set_jam_a)), []


def binary_search_rekursif(data_terurut, target_id, low, high, langkah=1):
    if low > high:
        return None, langkah - 1

    mid = (low + high) // 2
    id_mid = data_terurut[mid]["id"].upper()

    if id_mid == target_id:
        return data_terurut[mid], langkah
    if target_id < id_mid:
        return binary_search_rekursif(data_terurut, target_id, low, mid - 1, langkah + 1)
    return binary_search_rekursif(data_terurut, target_id, mid + 1, high, langkah + 1)


def cari_perangkat_id_binary(daftar_perangkat, target_id):
    if not daftar_perangkat:
        return None, 0
    # Data harus terurut berdasarkan ID sebelum binary search
    data_terurut = sorted(daftar_perangkat, key=lambda x: x["id"].upper())
    target_clean = target_id.strip().upper()
    return binary_search_rekursif(data_terurut, target_clean, 0, len(data_terurut) - 1, 1)


def cari_perangkat_nama(daftar_perangkat, keyword):
    keyword_clean = keyword.strip().lower()
    return [p for p in daftar_perangkat if keyword_clean in p["nama"].lower()]


def cari_perangkat_ruangan(daftar_perangkat, nama_ruangan):
    ruangan_clean = nama_ruangan.strip().lower()
    return [p for p in daftar_perangkat if ruangan_clean == p["ruangan"].lower()]


def cari_perangkat_daya_tinggi(daftar_perangkat, min_watt):
    return [p for p in daftar_perangkat if p["watt_aktif"] >= min_watt]


def urutkan_perangkat_biaya(daftar_perangkat, tarif_per_kwh=1444.70, descending=True):
    data = list(daftar_perangkat)
    n = len(data)

    def hitung_biaya(p):
        kwh = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
        return kwh * tarif_per_kwh

    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            biaya_j = hitung_biaya(data[j])
            biaya_next = hitung_biaya(data[j + 1])
            kondisi = (biaya_j < biaya_next) if descending else (biaya_j > biaya_next)
            if kondisi:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        if not swapped:
            break
    return data


def urutkan_perangkat_vampire(daftar_perangkat, descending=True):
    data = list(daftar_perangkat)
    n = len(data)

    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            val_a = data[j]["watt_standby"]
            val_b = data[j + 1]["watt_standby"]
            kondisi = (val_a < val_b) if descending else (val_a > val_b)
            if kondisi:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        if not swapped:
            break
    return data


def urutkan_perangkat_watt_insertion(daftar_perangkat, descending=True):
    data = list(daftar_perangkat)
    n = len(data)

    for i in range(1, n):
        key_item = data[i]
        key_watt = key_item["watt_aktif"]
        j = i - 1

        while j >= 0:
            kondisi = (data[j]["watt_aktif"] < key_watt) if descending else (data[j]["watt_aktif"] > key_watt)
            if kondisi:
                data[j + 1] = data[j]
                j -= 1
            else:
                break
        data[j + 1] = key_item

    return data


def urutkan_perangkat_prioritas(daftar_perangkat):
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


def rekomendasi_anti_jeglek(daftar_perangkat, batas_watt_aman, jam_overload, rincian_per_jam):
    if not jam_overload:
        return

    print("\n" + "=" * 85)
    print(f"      {Warna.CYAN}{Warna.TEBAL}REKOMENDASI CERDAS ANTI-JEGLEK (SMART LOAD SHIFTING){Warna.RESET}")
    print("=" * 85)
    print("Sistem menganalisis pergeseran jam pakai untuk mencegah MCB trip:")

    for jam, watt, alat_id_list in jam_overload:
        kelebihan = watt - batas_watt_aman
        print(f"\n[!] Kasus Jam {jam:02d}:00 (Beban {watt} W | Melebihi batas aman sebesar +{kelebihan} W):")

        kandidat_geser = [
            p for p in daftar_perangkat
            if p["id"] in alat_id_list
            and p["prioritas"] in ["Sekunder", "Tersier"]
            and p["watt_aktif"] >= 200
        ]
        kandidat_geser.sort(key=lambda x: x["watt_aktif"], reverse=True)

        if not kandidat_geser:
            print("   -> Tidak ada perangkat fleksibel yang dapat digeser (semua berprioritas Primer).")
            print("   -> Saran: Pertimbangkan upgrade daya meteran PLN ke golongan di atasnya.")
            continue

        alat_terpilih = kandidat_geser[0]
        jam_tujuan_terbaik = None
        beban_terendah = 99999

        # Cari jam pengganti di rentang 08:00-21:00 agar total beban tetap <= 85% batas aman
        for j_target in range(8, 22):
            if j_target != jam:
                beban_j, _ = rincian_per_jam.get(j_target, (0, []))
                if (beban_j + alat_terpilih["watt_aktif"]) <= (batas_watt_aman * 0.85):
                    if beban_j < beban_terendah:
                        beban_terendah = beban_j
                        jam_tujuan_terbaik = j_target

        if jam_tujuan_terbaik is not None:
            beban_baru_asal = watt - alat_terpilih["watt_aktif"]
            beban_baru_tujuan = beban_terendah + alat_terpilih["watt_aktif"]
            print(f"   {Warna.HIJAU}[*] SOLUSI REKOMENDASI SISTEM:{Warna.RESET}")
            print(f"   1. Geser pemakaian '{alat_terpilih['nama']}' ({alat_terpilih['watt_aktif']} W) dari Pk {jam:02d}:00 ke Pk {jam_tujuan_terbaik:02d}:00.")
            print(f"   2. Hasil Simulasi Pk {jam:02d}:00: Beban turun dari {watt} W -> {Warna.HIJAU}{beban_baru_asal} W{Warna.RESET} (Bebas dari Jeglek!).")
            print(f"   3. Kondisi Pk {jam_tujuan_terbaik:02d}:00: Beban naik menjadi {beban_baru_tujuan} W (Masih sangat aman di bawah {batas_watt_aman} W).")
        else:
            print(f"   [*] Saran: Hindari menyalakan '{alat_terpilih['nama']}' bersamaan dengan alat pemanas lainnya.")

    print("=" * 85)


def simulasi_beban_24jam(daftar_perangkat, batas_watt_aman=1100, va_maks=1300):
    print("\n" + "=" * 85)
    print(f"        {Warna.CYAN}{Warna.TEBAL}SIMULASI MATRIKS BEBAN LISTRIK 24 JAM (DETEKTOR ANTI-JEGLEK){Warna.RESET}")
    print(f"        Batas Daya Aman: {batas_watt_aman} Watt | Kapasitas Terpasang: {va_maks} VA")
    print("=" * 85)
    print(f"{'Jam':<7} | {'Beban (Watt)':<12} | {'Visualisasi Beban (ASCII Bar)':<35} | {'Status'}")
    print("-" * 85)

    jam_overload = []
    rincian_per_jam = {}

    for jam in range(24):
        total_watt_jam = 0
        alat_id_list = []
        alat_nama_list = []

        for p in daftar_perangkat:
            if jam in p.get("rentang_jam", []):
                total_watt_jam += p["watt_aktif"]
                alat_id_list.append(p["id"])
                alat_nama_list.append(p["nama"])
            else:
                total_watt_jam += p.get("watt_standby", 0)

        rincian_per_jam[jam] = (total_watt_jam, alat_nama_list)

        if total_watt_jam > batas_watt_aman:
            jam_overload.append((jam, total_watt_jam, alat_id_list))

        persen = min(total_watt_jam / batas_watt_aman, 1.5)
        bar_len = int(persen * 20)
        bar_str = "█" * min(bar_len, 20) + "░" * max(0, 20 - bar_len)

        if total_watt_jam > batas_watt_aman:
            status = f" {Warna.MERAH}{Warna.TEBAL}[!] OVERLOAD (RISIKO JEGLEK){Warna.RESET}"
        elif total_watt_jam > (batas_watt_aman * 0.8):
            status = f" {Warna.KUNING}[*] WASPADA (>80%){Warna.RESET}"
        else:
            status = f" {Warna.HIJAU}[v] AMAN{Warna.RESET}"

        print(f"{jam:02d}:00   | {total_watt_jam:>5} Watt    | [{bar_str:<20}] {int(persen*100):>3}% |{status}")

    print("=" * 85)

    if jam_overload:
        print("\n" + "!" * 85)
        print(f" {Warna.MERAH}{Warna.TEBAL}PERINGATAN POTENSI MCB TRIP (LISTRIK JEGLEK) DITEMUKAN!{Warna.RESET}")
        print("!" * 85)
        for jam, watt, alat_id_list in jam_overload:
            print(f"-> Jam {jam:02d}:00 : Total Beban {Warna.MERAH}{watt} W{Warna.RESET} melebihi kapasitas aman {batas_watt_aman} W.")
            nama_alat_list = [p["nama"] for p in daftar_perangkat if p["id"] in alat_id_list]
            print(f"   Alat yang menyala bersamaan: {', '.join(nama_alat_list)}")

        rekomendasi_anti_jeglek(daftar_perangkat, batas_watt_aman, jam_overload, rincian_per_jam)
    else:
        print(f"\n{Warna.HIJAU}[v] KONDISI AMAN: Tidak ditemukan jam dengan potensi listrik jeglek.{Warna.RESET}")

    return rincian_per_jam


def smart_budget_optimizer(daftar_perangkat, anggaran_maksimal, tarif_per_kwh):
    """Optimasi biaya bulanan dengan metode greedy dan daftar ID pengecualian."""
    print("\n" + "=" * 75)
    print(f"            {Warna.CYAN}{Warna.TEBAL}SMART BUDGET OPTIMIZER - GREEDY ALGORITHM{Warna.RESET}")
    print("=" * 75)

    perangkat_hasil = [p.copy() for p in daftar_perangkat]
    input_id = input("Masukkan ID perangkat yang dikecualikan (pisahkan dengan koma): ")
    daftar_id_dikecualikan = [item.strip().upper() for item in input_id.split(",") if item.strip()]

    print(f"\nID yang dikecualikan: {daftar_id_dikecualikan}")

    def hitung_total_biaya():
        total = 0.0
        for p in perangkat_hasil:
            kwh = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
            total += kwh * tarif_per_kwh
        return total

    biaya_awal = hitung_total_biaya()
    biaya_sekarang = biaya_awal

    print(f"\nBiaya awal        : {format_rupiah(biaya_awal)}")
    print(f"Target anggaran   : {format_rupiah(anggaran_maksimal)}")

    while biaya_sekarang > anggaran_maksimal:
        kandidat = []
        for p in perangkat_hasil:
            if str(p["id"]).upper() in daftar_id_dikecualikan or p["jam_pakai"] <= 0:
                continue
            hemat = (p["watt_aktif"] - p["watt_standby"]) * 30 / 1000.0 * tarif_per_kwh
            if hemat > 0:
                kandidat.append((hemat, p))

        if not kandidat:
            break

        kandidat.sort(key=lambda x: x[0], reverse=True)
        _, alat = kandidat[0]
        alat["jam_pakai"] -= 1
        biaya_sekarang = hitung_total_biaya()

        print(f"-> ID {alat['id']} ({alat['nama']}) jam pakai dikurangi menjadi {alat['jam_pakai']} jam")

    print("\n" + "=" * 75)
    print(f"Biaya sebelum optimasi : {format_rupiah(biaya_awal)}")
    print(f"Biaya setelah optimasi : {format_rupiah(biaya_sekarang)}")
    print(f"Total penghematan      : {format_rupiah(biaya_awal - biaya_sekarang)}")

    if biaya_sekarang <= anggaran_maksimal:
        print(f"{Warna.HIJAU}[BERHASIL] Anggaran berhasil dicapai!{Warna.RESET}")
    else:
        print(f"{Warna.KUNING}[PERINGATAN] Anggaran belum tercapai.{Warna.RESET}")
        print("Perangkat yang tersisa tidak dapat dikurangi lagi atau dikecualikan.")

    print("=" * 75)
    return perangkat_hasil


def audit_per_ruangan(daftar_perangkat, tarif_per_kwh=1444.70):
    set_ruangan = ambil_himpunan_ruangan(daftar_perangkat)
    if not set_ruangan:
        print("\n[i] Tidak ada data perangkat untuk diaudit.")
        return

    print("\n" + "=" * 80)
    print(f"                    {Warna.CYAN}{Warna.TEBAL}AUDIT KONSUMSI LISTRIK PER RUANGAN{Warna.RESET}")
    print("=" * 80)

    for ruangan in sorted(set_ruangan):
        print(f"\n Ruangan: [{ruangan.upper()}]")
        print(f" {'ID':<6} | {'Nama Alat':<25} | {'Aktif':<8} | {'Jam':<5} | {'Biaya/Bulan'}")
        print(" " + "-" * 65)

        subtotal_watt = 0
        subtotal_biaya = 0.0

        for p in daftar_perangkat:
            if p["ruangan"] == ruangan:
                kwh_bulan = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
                biaya = kwh_bulan * tarif_per_kwh
                subtotal_watt += p["watt_aktif"]
                subtotal_biaya += biaya
                print(f" {p['id']:<6} | {p['nama']:<25} | {p['watt_aktif']:<5} W | {p['jam_pakai']:<2} j  | {format_rupiah(biaya)}")

        print(" " + "-" * 65)
        print(f" Subtotal Ruang {ruangan}: Total Daya Aktif = {subtotal_watt} W | Biaya = {format_rupiah(subtotal_biaya)}/Bulan")

    print("=" * 80)


def analisis_vampire_power(daftar_perangkat, tarif_per_kwh=1444.70):
    print("\n" + "=" * 85)
    print(f"        {Warna.CYAN}{Warna.TEBAL}DETEKTOR VAMPIRE POWER (KEBOCORAN DAYA STANDBY LISTRIK){Warna.RESET}")
    print("=" * 85)
    print(f"{'ID':<6} | {'Nama Alat':<22} | {'Stdby (W)':<10} | {'Jam Idle':<9} | {'kWh/Bulan':<10} | {'Rupiah Terbuang/Thn'}")
    print("-" * 85)

    total_kwh_vampire_bulan = 0.0
    total_rugi_tahunan = 0.0

    for p in daftar_perangkat:
        standby_w = p.get("watt_standby", 0)
        jam_idle = 24 - p["jam_pakai"]
        if standby_w > 0 and jam_idle > 0:
            kwh_bulan = (standby_w * jam_idle * 30) / 1000.0
            rugi_tahun = kwh_bulan * tarif_per_kwh * 12

            total_kwh_vampire_bulan += kwh_bulan
            total_rugi_tahunan += rugi_tahun

            print(f"{p['id']:<6} | {p['nama']:<22} | {standby_w:>6} W   | {jam_idle:>4} jam  | {kwh_bulan:>8.2f}   | {format_rupiah(rugi_tahun)}")

    print("-" * 85)
    print(f" TOTAL KEBOCORAN DAYA STANDBY : {total_kwh_vampire_bulan:.2f} kWh/Bulan")
    print(f" TOTAL UANG TERBUANG SIA-SIA   : {format_rupiah(total_kwh_vampire_bulan * tarif_per_kwh)}/Bulan")
    print(f"                                 atau {format_rupiah(total_rugi_tahunan)}/Tahun!")
    print("\n[TIPS HEMAT] Cabut colokan TV, microwave, charger, dan dispenser saat tidak dipakai,")
    print("             atau gunakan stopkontak switch on/off agar tidak ada arus standby.")
    print("=" * 85)


def hitung_emisi_karbon(total_kwh_bulan):
    # Faktor emisi listrik ~0.85 kg CO2/kWh; serapan pohon dewasa ~22 kg CO2/tahun
    emisi_co2 = total_kwh_bulan * 0.85
    emisi_tahunan = emisi_co2 * 12
    jumlah_pohon = int(emisi_tahunan / 22) + (1 if emisi_tahunan % 22 > 0 else 0)
    return emisi_co2, jumlah_pohon


def export_laporan_audit(daftar_perangkat, profil_rumah, nama_file="laporan_audit.txt"):
    tarif = profil_rumah["tarif"]
    batas = profil_rumah["batas_watt"]

    total_kwh_bulan = 0.0
    total_biaya_bulan = 0.0
    total_vampire_rugi = 0.0

    lines = [
        "=" * 75 + "\n",
        "             LAPORAN RESMI AUDIT KELISTRIKAN RUMAH TANGGA\n",
        "                       APLIKASI WATTWISE HOME\n",
        "=" * 75 + "\n\n",
        f"GOLONGAN LISTRIK PLN : {profil_rumah['golongan']} ({profil_rumah['va']} VA)\n",
        f"BATAS AMAN BEBAN     : {batas} Watt\n",
        f"TARIF PER KWH        : {format_rupiah(tarif)} /kWh\n",
        f"SISA TOKEN SAAT INI  : {profil_rumah['sisa_token_kwh']:.2f} kWh\n",
        "-" * 75 + "\n\n",
        "RINCIAN PERANGKAT ELEKTRONIK:\n",
        f"{'ID':<6} | {'Nama Alat':<22} | {'Ruang':<12} | {'Watt':<6} | {'Jam':<4} | {'Biaya/Bulan'}\n",
        "-" * 75 + "\n",
    ]

    for p in daftar_perangkat:
        kwh = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
        biaya = kwh * tarif
        total_kwh_bulan += kwh
        total_biaya_bulan += biaya

        jam_idle = 24 - p["jam_pakai"]
        if p["watt_standby"] > 0 and jam_idle > 0:
            total_vampire_rugi += (p["watt_standby"] * jam_idle * 30 / 1000.0) * tarif * 12

        lines.append(f"{p['id']:<6} | {p['nama']:<22} | {p['ruangan']:<12} | {p['watt_aktif']:<6} | {p['jam_pakai']:<4} | {format_rupiah(biaya)}\n")

    emisi, pohon = hitung_emisi_karbon(total_kwh_bulan)
    lines.extend([
        "-" * 75 + "\n",
        f"TOTAL ESTIMASI BIAYA LISTRIK : {format_rupiah(total_biaya_bulan)} / Bulan\n",
        f"TOTAL KONSUMSI LISTRIK       : {total_kwh_bulan:.2f} kWh / Bulan\n",
        f"ESTIMASI EMISI CO2           : {emisi:.2f} kg / Bulan\n",
        f"ESTIMASI KEBUTUHAN POHON     : {pohon} pohon (ekuivalen tahunan)\n",
        f"POTENSI RUGI VAMPIRE POWER   : {format_rupiah(total_vampire_rugi)} / Tahun\n\n",
        "CATATAN AUDITOR:\n",
        "- Matikan alat elektronika saat jam beban puncak (18:00 - 21:00).\n",
        "- Cabut stopkontak perangkat yang memiliki daya standby tinggi.\n",
        "=" * 75 + "\n\n",
        "=" * 75 + "\n",
        "HASIL SIMULASI BEBAN LISTRIK 24 JAM\n",
        "=" * 75 + "\n",
    ])

    rincian_simulasi = simulasi_beban_24jam(
        daftar_perangkat,
        batas_watt_aman=batas,
        va_maks=profil_rumah["va"]
    )

    lines.append(f"{'JAM':<10} | {'BEBAN (WATT)':<15} | {'VISUALISASI':<25} | {'STATUS':<10}\n")
    lines.append("=" * 75 + "\n")

    jam_overload_laporan = []
    for jam in range(24):
        total_watt, alat_menyala = rincian_simulasi[jam]
        bar_len = min(int((total_watt / batas) * 10), 25)
        grafik = "#" * bar_len

        if total_watt > batas:
            status = "OVERLOAD"
            jam_overload_laporan.append((jam, total_watt, alat_menyala))
        elif total_watt > batas * 0.8:
            status = "WASPADA"
        else:
            status = "AMAN"

        lines.append(f"{f'{jam:02d}:00':<10} | {total_watt:<15} | {grafik:<25} | {status}\n")

    lines.append("-" * 75 + "\n\nCATATAN PERINGATAN ANTI JEGLEK\n")

    if jam_overload_laporan:
        lines.append("[!] PERINGATAN: DITEMUKAN JAM OVERLOAD!\n")
        for jam, watt, alat in jam_overload_laporan:
            lines.append(f"- Jam {jam:02d}:00: {watt} Watt\n")
            lines.append(f"  Perangkat menyala : {', '.join(alat)}\n")
        lines.append("REKOMENDASI: Kurangi atau geser penggunaan perangkat berdaya besar ke jam yang lebih aman.\n")
    else:
        lines.append("[OK] Tidak ditemukan beban listrik yang melebihi batas aman.\n")

    lines.append("=" * 75 + "\n")

    try:
        with open(nama_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"\n[OK] Laporan audit berhasil diekspor ke file '{nama_file}'!")
    except Exception as e:
        print(f"[!] Gagal mengekspor laporan: {e}")
