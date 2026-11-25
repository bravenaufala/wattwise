import os
import random
from datetime import datetime, timedelta
from modul_crud import format_rupiah, Warna, simpan_profil, simpan_semua_perangkat, cetak_header, cetak_garis

FILE_RIWAYAT_TOKEN = "riwayat_token.txt"


def muat_riwayat_token():
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
    riwayat = muat_riwayat_token()
    if not riwayat:
        print("\n[!] Belum ada riwayat pengisian token.")
        return

    data_grafik = []
    for transaksi in riwayat[-3:]:
        sisa_token = transaksi["sisa_sebelum"] + transaksi["kwh_didapat"]
        data_grafik.append({
            "tanggal": transaksi["tanggal"],
            "nominal": transaksi["nominal"],
            "sisa": sisa_token
        })

    nilai_maksimal = max(item["sisa"] for item in data_grafik)

    cetak_header("GRAFIK SISA TOKEN LISTRIK", "3 Transaksi Top-Up Terakhir", lebar=74)

    for item in data_grafik:
        panjang_bar = int((item["sisa"] / nilai_maksimal) * 30) if nilai_maksimal > 0 else 0
        bar_filled = "█" * panjang_bar
        bar_empty = "░" * (30 - panjang_bar)

        print(f"  {Warna.REDUP}{item['tanggal']:<16}{Warna.RESET} │ {format_rupiah(item['nominal']):>14} │ {Warna.HIJAU}{item['sisa']:>6.2f} kWh{Warna.RESET}")
        print(f"  {Warna.CYAN}{bar_filled}{Warna.REDUP}{bar_empty}{Warna.RESET}\n")

    cetak_garis(74)


def beli_token_listrik(profil_rumah, nominal_rp):
    tarif = profil_rumah["tarif"]
    sisa_awal = profil_rumah["sisa_token_kwh"]

    # Potongan Pajak Penerangan Jalan (PPJ) 3%
    potongan_ppj = nominal_rp * 0.03
    dana_bersih = nominal_rp - potongan_ppj
    kwh_didapat = dana_bersih / tarif
    sisa_baru = sisa_awal + kwh_didapat

    profil_rumah["sisa_token_kwh"] = sisa_baru
    simpan_profil(
        profil_rumah["golongan"],
        profil_rumah["va"],
        profil_rumah["batas_watt"],
        profil_rumah["tarif"],
        profil_rumah["sisa_token_kwh"]
    )

    digit_token = "".join(str(random.randint(0, 9)) for _ in range(20))
    kode_token = f"{digit_token[0:4]}-{digit_token[4:8]}-{digit_token[8:12]}-{digit_token[12:16]}-{digit_token[16:20]}"

    tgl_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(FILE_RIWAYAT_TOKEN, "a", encoding="utf-8") as f:
        f.write(f"{tgl_sekarang}|{int(nominal_rp)}|{kwh_didapat:.1f}|{sisa_awal:.1f}\n")

    return {
        "nominal": nominal_rp,
        "ppj": potongan_ppj,
        "dana_bersih": dana_bersih,
        "kwh_didapat": kwh_didapat,
        "sisa_awal": sisa_awal,
        "sisa_baru": sisa_baru,
        "kode_token": kode_token,
        "tanggal": tgl_sekarang
    }


def tampilkan_struk_token(struk, profil_rumah):
    cetak_header("STRUK PEMBELIAN LISTRIK PRABAYAR (PLN)", f"Waktu: {struk['tanggal']}", lebar=60)
    print("  ID Pelanggan       : 5382-9102-4412 (Simulasi)")
    print(f"  Golongan / Daya    : {profil_rumah['golongan']} ({profil_rumah['va']} VA)")
    print(f"  Tarif Dasar        : {format_rupiah(profil_rumah['tarif'])} /kWh")
    cetak_garis(60)
    print(f"  Pembelian Token    : {format_rupiah(struk['nominal'])}")
    print(f"  Potongan PPJ (3%)  : {format_rupiah(struk['ppj'])}")
    print(f"  Nilai Listrik Net  : {format_rupiah(struk['dana_bersih'])}")
    print(f"  Energi Didapat     : {Warna.HIJAU}{Warna.TEBAL}+{struk['kwh_didapat']:.2f} kWh{Warna.RESET}")
    print(f"  Sisa Token Baru    : {Warna.TEBAL}{struk['sisa_baru']:.2f} kWh{Warna.RESET}")
    cetak_garis(60)
    print(f"  {Warna.KUNING}{Warna.TEBAL}KODE TOKEN 20 DIGIT:{Warna.RESET}")
    print(f"  {Warna.HIJAU}{Warna.TEBAL}>> {struk['kode_token']} <<{Warna.RESET}")
    cetak_garis(60)
    print(f"  {Warna.REDUP}[i] Data sisa token dan histori berhasil disimpan otomatis.{Warna.RESET}")
    cetak_garis(60)


def prediksi_habis_token(daftar_perangkat, profil_rumah):
    cetak_header("PREDIKSI HABISNYA TOKEN LISTRIK", "Estimasi Pemakaian Harian PLN Prabayar", lebar=74)

    sisa_kwh = profil_rumah.get("sisa_token_kwh", 0.0)
    tarif = profil_rumah.get("tarif", 1444.70)

    total_kwh_harian = 0.0
    for p in daftar_perangkat:
        aktif = (p["watt_aktif"] * p["jam_pakai"]) / 1000.0
        standby = (p["watt_standby"] * (24 - p["jam_pakai"])) / 1000.0
        total_kwh_harian += aktif + standby

    print(f"  Sisa Token di Meteran    : {Warna.HIJAU}{Warna.TEBAL}{sisa_kwh:.2f} kWh{Warna.RESET}")
    print(f"  Rata-rata Pemakaian      : {total_kwh_harian:.2f} kWh / hari")
    print(f"  Estimasi Biaya Harian    : {format_rupiah(total_kwh_harian * tarif)} / hari")
    cetak_garis(74)

    if total_kwh_harian <= 0:
        print("  [i] Tidak ada konsumsi listrik harian yang terdeteksi.")
        cetak_garis(74)
        return

    sisa_hari = sisa_kwh / total_kwh_harian
    hari_bulat = int(sisa_hari)
    jam_sisa = int((sisa_hari - hari_bulat) * 24)
    tanggal_habis = datetime.now() + timedelta(days=sisa_hari)

    print(f"  Perkiraan Token Habis    : {Warna.TEBAL}{hari_bulat} Hari {jam_sisa} Jam lagi{Warna.RESET}")
    print(f"  Estimasi Tanggal Habis   : {Warna.CYAN}{tanggal_habis.strftime('%A, %d %B %Y jam %H:%M')}{Warna.RESET}")

    if sisa_hari <= 2:
        print(f"\n  {Warna.MERAH}{Warna.TEBAL}[!] DARURAT: Sisa token sangat sedikit, segera isi ulang.{Warna.RESET}")
    elif sisa_hari <= 5:
        print(f"\n  {Warna.KUNING}[*] PERHATIAN: Sisa token kurang dari 5 hari. Siapkan dana isi ulang.{Warna.RESET}")
    else:
        print(f"\n  {Warna.HIJAU}[v] STATUS AMAN: Kuota token masih mencukupi.{Warna.RESET}")

    riwayat = muat_riwayat_token()
    if riwayat:
        print()
        cetak_garis(74)
        print(f"  {Warna.TEBAL}Riwayat 3 Pengisian Token Terakhir:{Warna.RESET}")
        for r in riwayat[-3:]:
            print(
                f"  - {Warna.REDUP}{r['tanggal']:<16}{Warna.RESET} │ {format_rupiah(r['nominal']):>14} │ "
                f"+{r['kwh_didapat']:.1f} kWh {Warna.REDUP}(sisa awal {r['sisa_sebelum']:.1f} kWh){Warna.RESET}"
            )
    cetak_garis(74)


def smart_budget_optimizer(daftar_perangkat, tarif_per_kwh=1444.70):
    """Rekomendasi pemangkasan jam pakai berdasarkan prioritas (Tersier lalu Sekunder)."""
    print("\n" + "=" * 75)
    print(f"       {Warna.CYAN}{Warna.TEBAL}SMART BUDGET OPTIMIZER (REKOMENDASI DIET LISTRIK GREEDY){Warna.RESET}")
    print("=" * 75)

    if not daftar_perangkat:
        print("[i] Belum ada data perangkat untuk dianalisis.")
        return

    total_biaya_saat_ini = 0.0
    for p in daftar_perangkat:
        kwh = ((p["watt_aktif"] * p["jam_pakai"]) + (p["watt_standby"] * (24 - p["jam_pakai"]))) * 30 / 1000.0
        total_biaya_saat_ini += kwh * tarif_per_kwh

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
        print("=" * 75)
        return

    selisih_harus_hemat = total_biaya_saat_ini - target_budget
    print(f"\n[*] Anda perlu menghemat pengeluaran sebesar minimal {format_rupiah(selisih_harus_hemat)} / Bulan.")
    print("    Sistem sedang menyusun strategi pemangkasan jam pakai paling ideal...")

    simulasi = [dict(p) for p in daftar_perangkat]
    rekomendasi_diet = []
    biaya_berjalan = total_biaya_saat_ini

    for prioritas_target in ["Tersier", "Sekunder"]:
        for p in simulasi:
            if biaya_berjalan <= target_budget:
                break
            if p["prioritas"] == prioritas_target and p["jam_pakai"] > 1:
                jam_awal = p["jam_pakai"]
                while p["jam_pakai"] > 1 and biaya_berjalan > target_budget:
                    p["jam_pakai"] -= 1
                    hemat_kwh_hari = (p["watt_aktif"] - p["watt_standby"]) / 1000.0
                    biaya_berjalan -= hemat_kwh_hari * 30 * tarif_per_kwh

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

    print("\n" + "=" * 75)
    print(f"{'Nama Alat':<25} | {'Prioritas':<10} | {'Jam Lama':<8} -> {'Jam Baru':<8} | {'Hemat/Bulan'}")
    print("-" * 75)

    total_dihemat = 0.0
    for r in rekomendasi_diet:
        total_dihemat += r["hemat_rp"]
        print(f"{r['nama']:<25} | {r['prioritas']:<10} | {r['jam_awal']:<2} jam/hr  -> {r['jam_baru']:<2} jam/hr  | {format_rupiah(r['hemat_rp'])}")

    print("-" * 75)
    print(f" TOTAL BIAYA SETELAH DIET : {format_rupiah(biaya_berjalan)} / Bulan")
    print(f" TOTAL PENGHEMATAN DIDAPAT: {format_rupiah(total_dihemat)} / Bulan")

    if biaya_berjalan <= target_budget:
        print(f"\n{Warna.HIJAU}[v] TARGET TERCAPAI! Dengan mengikuti rekomendasi di atas, tagihan listrik Anda{Warna.RESET}")
        print("    dipastikan tidak akan melebihi batas anggaran yang Anda tentukan.")
    else:
        print(f"\n{Warna.KUNING}[!] TARGET HAMPIR TERCAPAI: Seluruh perangkat hiburan & sekunder telah diminimalkan.{Warna.RESET}")
        print("    Untuk menghemat lebih jauh, pertimbangkan mengganti perangkat utama dengan teknologi inverter/hemat energi.")
    print("=" * 75)

    if rekomendasi_diet:
        print("\n" + "-" * 75)
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
