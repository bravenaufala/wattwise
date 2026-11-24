# ==============================================================================
# MODUL PREDIKSI & SMART BUDGET OPTIMIZER (modul_prediksi.py)
# Bagian Tanggung Jawab:
# - Anggota 1: Transaksi Beli Token Baru, Cetak Struk 20-Digit & Integrasi Simpan Data
# - Anggota 3: Prediksi Habisnya Token Listrik & Smart Diet Listrik (Greedy Optimizer)
# ==============================================================================

import os
import random
from datetime import datetime, timedelta
from modul_crud import format_rupiah, Warna, simpan_profil, simpan_semua_perangkat

FILE_RIWAYAT_TOKEN = "riwayat_token.txt"

# [MATERI: FILE HANDLING - MEMBACA RIWAYAT TOKEN]
def muat_riwayat_token():
    """Membaca histori pengisian token dari riwayat_token.txt."""
    riwayat = []
    if not os.path.exists(FILE_RIWAYAT_TOKEN):
        return riwayat

    with open(FILE_RIWAYAT_TOKEN, "r", encoding="utf-8") as f:
        baris_semua = f.readlines()

    for baris in baris_semua[1:]:
        baris = baris.strip()
        if not baris:
            continue
        parts = baris.split("|")
        if len(parts) >= 4:
            try:
                riwayat.append({
                    "tanggal": parts[0].strip(),
                    "nominal": int(parts[1].strip()),
                    "kwh_didapat": float(parts[2].strip()),
                    "sisa_sebelum": float(parts[3].strip())
                })
            except ValueError:
                continue
    return riwayat

def tampilkan_grafik_sisa_token():
    """
    Menampilkan grafik ASCII sisa token dari 3 transaksi terakhir
    """
    riwayat = muat_riwayat_token()

    if not riwayat:
        print("\n[!]Belum ada riwayat pengisian token.")
        return

    tiga_transaksi = riwayat[-3:]

    # Hitung sisa token setelah setiap pengisian
    data_grafik = []
    for transaksi in tiga_transaksi:
        sisa_token = (
            transaksi["sisa_sebelum"] + transaksi["kwh_didapat"]
        )

        data_grafik.append({
            "tanggal": transaksi["tanggal"],
            "nominal": transaksi["nominal"],
            "sisa": sisa_token
        })

    nilai_maksimal = max(item["sisa"] for item in data_grafik)

    print("\n" + "=" * 65)
    print("     GRAFIK SISA TOKEN LISTRIK - 3 UP TERAKHIR")
    print("="*65)

    for item in data_grafik:
        if nilai_maksimal > 0:
            panjang_bar = int(
                (item["sisa"] / nilai_maksimal)*30
            )
        else:
            panjang_bar = 0 

        grafik = "#" * panjang_bar

        print(f"\nTanggal   : {item['tanggal']}")
        print(f"Top up      : Rp{item['nominal']:,}")
        print(f"sisa        : {item['sisa']:.2f} kwh")
        print(f"[{grafik}]")

    print("\n" + "=" * 65)

# [FITUR BARU ANGGOTA 1: TRANSAKSI & PENCATATAN FILE RIWAYAT TOKEN]
def beli_token_listrik(profil_rumah, nominal_rp):
    """
    Mensimulasikan pembelian token listrik PLN (Prabayar):
    1. Memotong Pajak Penerangan Jalan (PPJ) 3% (regulasi resmi PLN).
    2. Menghitung jumlah kWh yang didapat berdasarkan tarif per kWh golongan aktif.
    3. Menghasilkan kode stroom token 20 digit unik (format XXXX-XXXX-XXXX-XXXX-XXXX).
    4. Mengupdate sisa token di profil dan menyimpannya ke data_profil.txt.
    5. Menulis transaksi ke riwayat_token.txt (File Handling Append).
    """
    tarif = profil_rumah["tarif"]
    sisa_awal = profil_rumah["sisa_token_kwh"]

    # Regulasi PLN: Pajak Penerangan Jalan (PPJ) rata-rata 3%
    ppj_persen = 0.03
    potongan_ppj = nominal_rp * ppj_persen
    dana_bersih = nominal_rp - potongan_ppj

    # Hitung kWh didapat
    kwh_didapat = dana_bersih / tarif
    sisa_baru = sisa_awal + kwh_didapat

    # Update profil rumah & simpan ke file
    profil_rumah["sisa_token_kwh"] = sisa_baru
    simpan_profil(
        profil_rumah["golongan"],
        profil_rumah["va"],
        profil_rumah["batas_watt"],
        profil_rumah["tarif"],
        profil_rumah["sisa_token_kwh"]
    )

    # Generate nomor token 20 digit acak
    digit_token = "".join([str(random.randint(0, 9)) for _ in range(20)])
    kode_token = f"{digit_token[0:4]}-{digit_token[4:8]}-{digit_token[8:12]}-{digit_token[12:16]}-{digit_token[16:20]}"

    # Simpan ke file riwayat_token.txt (Append mode)
    tgl_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(FILE_RIWAYAT_TOKEN, "a", encoding="utf-8") as f:
        f.write(f"{tgl_sekarang}|{int(nominal_rp)}|{kwh_didapat:.1f}|{sisa_awal:.1f}\n")

    struk = {
        "nominal": nominal_rp,
        "ppj": potongan_ppj,
        "dana_bersih": dana_bersih,
        "kwh_didapat": kwh_didapat,
        "sisa_awal": sisa_awal,
        "sisa_baru": sisa_baru,
        "kode_token": kode_token,
        "tanggal": tgl_sekarang
    }
    return struk

def tampilkan_struk_token(struk, profil_rumah):
    """Menampilkan struk digital resmi pembelian token listrik PLN."""
    print("\n" + "="*55)
    print(f"       {Warna.CYAN}{Warna.TEBAL}STRUK PEMBELIAN LISTRIK PRABAYAR (PLN){Warna.RESET}")
    print("="*55)
    print(f" Waktu Transaksi   : {struk['tanggal']}")
    print(f" ID Pelanggan / ID : 5382-9102-4412 (Simulasi)")
    print(f" Golongan / Daya   : {profil_rumah['golongan']} / {profil_rumah['va']} VA")
    print(f" Tarif Dasar Listrik: {format_rupiah(profil_rumah['tarif'])} /kWh")
    print("-" * 55)
    print(f" Pembelian Token   : {format_rupiah(struk['nominal'])}")
    print(f" Potongan PPJ (3%) : {format_rupiah(struk['ppj'])}")
    print(f" Nilai Listrik Net : {format_rupiah(struk['dana_bersih'])}")
    print(f" {Warna.HIJAU}{Warna.TEBAL}Energi Didapat    : +{struk['kwh_didapat']:.2f} kWh{Warna.RESET}")
    print(f" Sisa Token Baru   : {struk['sisa_baru']:.2f} kWh")
    print("="*55)
    print(f" {Warna.KUNING}{Warna.TEBAL}KODE TOKEN 20 DIGIT ANDA:{Warna.RESET}")
    print(f" >> {Warna.HIJAU}{Warna.TEBAL}{struk['kode_token']}{Warna.RESET} <<")
    print("="*55)
    print(" [i] Masukkan kode 20 digit di atas ke meteran listrik rumah.")
    print(" [i] Data sisa token dan histori berhasil disimpan otomatis.")
    print("="*55)

# [FITUR TAMBAHAN: PREDIKSI HABISNYA TOKEN LISTRIK]
# [TODO: Refine Anggota 3 - Tambahkan grafik tren sisa token berdasarkan tanggal]
def prediksi_habis_token(daftar_perangkat, profil_rumah):
    """
    Memprediksi berapa hari lagi sisa token meteran akan habis
    dan memperkirakan tanggal pengguna wajib membeli token baru.
    """
    print("\n" + "="*75)
    print("           PREDIKSI HABISNYA TOKEN LISTRIK (PULSA PLN)")
    print("="*75)

    sisa_kwh = profil_rumah.get("sisa_token_kwh", 0.0)
    tarif = profil_rumah.get("tarif", 1444.70)

    # 1. Hitung konsumsi harian saat ini dari semua perangkat
    total_kwh_harian = 0.0
    for p in daftar_perangkat:
        aktif = (p["watt_aktif"] * p["jam_pakai"]) / 1000.0
        standby = (p["watt_standby"] * (24 - p["jam_pakai"])) / 1000.0
        total_kwh_harian += (aktif + standby)

    print(f" Sisa Token Saat Ini di Meteran : {sisa_kwh:.2f} kWh")
    print(f" Rata-rata Pemakaian Harian     : {total_kwh_harian:.2f} kWh / Hari")
    print(f" Estimasi Biaya Pemakaian Harian : {format_rupiah(total_kwh_harian * tarif)} / Hari")
    print("-" * 75)

    if total_kwh_harian <= 0:
        print("[i] Tidak ada konsumsi listrik harian yang terdeteksi.")
        print("="*75)
        return

    # [MATERI: STATISTIKA DASAR & ESTIMASI]
    sisa_hari = sisa_kwh / total_kwh_harian
    hari_bulat = int(sisa_hari)
    jam_sisa = int((sisa_hari - hari_bulat) * 24)

    # [MATERI: PENGGUNAAN MODUL DATETIME BAWAAN PYTHON]
    hari_ini = datetime.now()
    tanggal_habis = hari_ini + timedelta(days=sisa_hari)

    print(f"\n>>> HASIL PREDIKSI SISTEM:")
    print(f" Token Anda diperkirakan akan HABIS dalam:")
    print(f" ==> {hari_bulat} Hari {jam_sisa} Jam lagi")
    print(f" ==> Perkiraan Tanggal Habis : {tanggal_habis.strftime('%A, %d %B %Y jam %H:%M')}")

    if sisa_hari <= 2:
        print("\n[!] PERINGATAN DARURAT: Token Anda tinggal sedikit! Segera beli token baru")
        print("    agar listrik tidak padam tiba-tiba di malam hari.")
    elif sisa_hari <= 5:
        print("\n[*] PERHATIAN: Sisa token kurang dari 5 hari. Disarankan menyiapkan dana isi ulang.")
    else:
        print("\n[v] STATUS AMAN: Sisa kuota token masih mencukupi untuk beberapa hari ke depan.")

    # Tampilkan Histori Pengisian Token
    riwayat = muat_riwayat_token()
    if riwayat:
        print("\n" + "-"*75)
        print(" Catatan Riwayat Pengisian Token Terakhir:")
        for r in riwayat[-3:]:
            print(f" - Tanggal {r['tanggal']}: Beli {format_rupiah(r['nominal'])} -> Dapat {r['kwh_didapat']:.1f} kWh (Sisa awal: {r['sisa_sebelum']:.1f} kWh)")
    print("="*75)

# [FITUR TAMBAHAN: SMART BUDGET OPTIMIZER (GREEDY HEURISTIC)]
# [TODO: Refine Anggota 3 - Tambahkan opsi pemilihan perangkat spesifik yang dikecualikan dari diet]
def smart_budget_optimizer(daftar_perangkat, tarif_per_kwh=1444.70):
    """
    Rekomendasi diet listrik otomatis menggunakan algoritma Greedy.
    Mengurangi jam operasional perangkat dari prioritas terendah (Tersier -> Sekunder)
    hingga estimasi pengeluaran bulanan masuk ke dalam batas target budget pengguna.
    """
    print("\n" + "="*75)
    print("       SMART BUDGET OPTIMIZER (REKOMENDASI DIET LISTRIK GREEDY)")
    print("="*75)

    if not daftar_perangkat:
        print("[i] Belum ada data perangkat untuk dianalisis.")
        return

    # Hitung total biaya bulanan saat ini
    total_biaya_saat_ini = 0.0
    for p in daftar_perangkat:
        kwh = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
        total_biaya_saat_ini += (kwh * tarif_per_kwh)

    print(f" Estimasi Biaya Listrik Saat Ini : {format_rupiah(total_biaya_saat_ini)} / Bulan")
    print("-" * 75)

    try:
        target_budget_str = input("Masukkan Target Anggaran Maksimal Anda per Bulan (Rp): ").strip().replace(".", "")
        target_budget = float(target_budget_str)
    except ValueError:
        print("[!] Input budget harus berupa angka valid!")
        return

    if target_budget >= total_biaya_saat_ini:
        selisih = target_budget - total_biaya_saat_ini
        print(f"\n[v] Pengeluaran Anda saat ini ({format_rupiah(total_biaya_saat_ini)}) sudah BERADA DI BAWAH target budget!")
        print(f"    Anda masih memiliki surplus anggaran sebesar {format_rupiah(selisih)} / Bulan.")
        print("="*75)
        return

    selisih_harus_hemat = total_biaya_saat_ini - target_budget
    print(f"\n[*] Anda perlu menghemat pengeluaran sebesar minimal {format_rupiah(selisih_harus_hemat)} / Bulan.")
    print("    Sistem sedang menyusun strategi pemangkasan jam pakai paling ideal...")

    # [MATERI: ALGORITMA GREEDY - PENGELOMPOKAN PRIORITAS]
    # Salin data perangkat agar simulasi tidak mengubah data asli secara permanen
    simulasi = [dict(p) for p in daftar_perangkat]

    rekomendasi_diet = []
    biaya_berjalan = total_biaya_saat_ini

    # Fase 1: Pangkas perangkat Tersier terlebih dahulu
    # Fase 2: Jika masih kurang, pangkas perangkat Sekunder
    for prioritas_target in ["Tersier", "Sekunder"]:
        for p in simulasi:
            if biaya_berjalan <= target_budget:
                break
            if p["prioritas"] == prioritas_target and p["jam_pakai"] > 1:
                # Coba kurangi jam pakai secara bertahap
                jam_awal = p["jam_pakai"]
                while p["jam_pakai"] > 1 and biaya_berjalan > target_budget:
                    # Kurangi 1 jam
                    p["jam_pakai"] -= 1
                    # Selisih kWh hemat per hari = (watt_aktif - watt_standby) / 1000
                    hemat_kwh_hari = (p["watt_aktif"] - p["watt_standby"]) / 1000.0
                    hemat_rp_bulan = hemat_kwh_hari * 30 * tarif_per_kwh
                    biaya_berjalan -= hemat_rp_bulan

                if p["jam_pakai"] < jam_awal:
                    jam_dipangkas = jam_awal - p["jam_pakai"]
                    rupiah_hemat = (jam_dipangkas * (p["watt_aktif"] - p["watt_standby"]) / 1000.0) * 30 * tarif_per_kwh
                    rekomendasi_diet.append({
                        "id": p["id"],
                        "nama": p["nama"],
                        "prioritas": p["prioritas"],
                        "jam_awal": jam_awal,
                        "jam_baru": p["jam_pakai"],
                        "hemat_rp": rupiah_hemat
                    })

    print("\n" + "="*75)
    print(f"{'Nama Alat':<25} | {'Prioritas':<10} | {'Jam Lama':<8} -> {'Jam Baru':<8} | {'Hemat/Bulan'}")
    print("-"*75)

    total_dihemat = 0.0
    for r in rekomendasi_diet:
        total_dihemat += r["hemat_rp"]
        print(f"{r['nama']:<25} | {r['prioritas']:<10} | {r['jam_awal']:<2} jam/hr  -> {r['jam_baru']:<2} jam/hr  | {format_rupiah(r['hemat_rp'])}")

    print("-"*75)
    print(f" TOTAL BIAYA SETELAH DIET : {format_rupiah(biaya_berjalan)} / Bulan")
    print(f" TOTAL PENGHEMATAN DIDAPAT: {format_rupiah(total_dihemat)} / Bulan")

    if biaya_berjalan <= target_budget:
        print(f"\n{Warna.HIJAU}[v] TARGET TERCAPAI! Dengan mengikuti rekomendasi di atas, tagihan listrik Anda{Warna.RESET}")
        print("    dipastikan tidak akan melebihi batas anggaran yang Anda tentukan.")
    else:
        print(f"\n{Warna.KUNING}[!] TARGET HAMPIR TERCAPAI: Seluruh perangkat hiburan & sekunder telah diminimalkan.{Warna.RESET}")
        print("    Untuk menghemat lebih jauh, pertimbangkan mengganti perangkat utama dengan teknologi inverter/hemat energi.")
    print("="*75)

    if rekomendasi_diet:
        print("\n" + "-"*75)
        konfirmasi = input("Apakah Anda ingin langsung menerapkan jadwal rekomendasi hemat ini ke data perangkat? (y/n): ").strip().lower()
        if konfirmasi == "y":
            for r in rekomendasi_diet:
                for p in daftar_perangkat:
                    if p["id"] == r["id"]:
                        p["jam_pakai"] = r["jam_baru"]
                        if len(p.get("rentang_jam", [])) > r["jam_baru"]:
                            p["rentang_jam"] = p["rentang_jam"][:r["jam_baru"]]
            simpan_semua_perangkat(daftar_perangkat)
            print(f"\n{Warna.HIJAU}[OK] Jadwal operasional baru berhasil diterapkan ke inventaris perangkat!{Warna.RESET}")
