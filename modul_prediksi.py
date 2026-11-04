# ==============================================================================
# MODUL PREDIKSI & SMART BUDGET OPTIMIZER (modul_prediksi.py)
# Bagian Tanggung Jawab:
# - Anggota 3: Prediksi Habisnya Token Listrik & Smart Diet Listrik (Greedy Optimizer)
# ==============================================================================

import os
from datetime import datetime, timedelta
from modul_crud import format_rupiah

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
        print("\n[v] TARGET TERCAPAI! Dengan mengikuti rekomendasi di atas, tagihan listrik Anda")
        print("    dipastikan tidak akan melebihi batas anggaran yang Anda tentukan.")
    else:
        print("\n[!] TARGET HAMPIR TERCAPAI: Seluruh perangkat hiburan & sekunder telah diminimalkan.")
        print("    Untuk menghemat lebih jauh, pertimbangkan mengganti perangkat utama dengan teknologi inverter/hemat energi.")
    print("="*75)
