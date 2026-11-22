# ==============================================================================
# WATTWISE HOME — SIMULATOR AUDIT LISTRIK, ANTI-JEGLEK & DETEKTOR VAMPIRE POWER
# File Utama: main.py
# Mata Kuliah: Praktikum Dasar Pemrograman (Python)
# Tim Pengembang:
# - Anggota 1: System Architect, Binary Search Rekursif, Insertion Sort, Set Union & Transaksi Token
# - Anggota 2: CRUD Lengkap (Create, Read, Update, Delete) & Validasi ID
# - Anggota 3: Nested Loop (Simulasi 24 Jam), Detektor Vampire Power, Prediksi & Export
# ==============================================================================

import sys
import os

# Inisialisasi terminal untuk mendukung ANSI Escape Colors di semua OS
os.system('')

# Import fungsi-fungsi modular dari berkas terpisah
from modul_crud import (
    GOLONGAN_PLN,
    Warna,
    muat_profil,
    simpan_profil,
    muat_perangkat,
    tambah_perangkat,
    tampilkan_tabel_perangkat,
    ubah_perangkat,
    hapus_perangkat,
    format_rupiah
)

from modul_analisis import (
    simulasi_beban_24jam,
    analisis_vampire_power,
    audit_per_ruangan,
    cari_perangkat_nama,
    cari_perangkat_ruangan,
    cari_perangkat_daya_tinggi,
    cari_perangkat_id_binary,
    urutkan_perangkat_biaya,
    urutkan_perangkat_vampire,
    urutkan_perangkat_watt_insertion,
    urutkan_perangkat_prioritas,
    deteksi_bentrok_jam_perangkat,
    gabungkan_jam_aktif_ruangan,
    deteksi_perangkat_boros,
    export_laporan_audit
)

from modul_prediksi import (
    prediksi_habis_token,
    smart_budget_optimizer,
    beli_token_listrik,
    tampilkan_struk_token
)

def jeda_layar():
    """Memberikan jeda agar pengguna dapat membaca output sebelum kembali ke menu."""
    input("\n[ Tekan ENTER untuk kembali ke menu... ]")

def menu_kelola_perangkat(daftar_perangkat, profil_rumah):
    """Sub-menu untuk operasi CRUD perangkat elektronik."""
    while True:
        print("\n" + "="*50)
        print("          MANAJEMEN DATA PERANGKAT (CRUD)")
        print("="*50)
        print("1. Tambah Perangkat Baru       (Create)")
        print("2. Lihat Seluruh Inventaris    (Read)")
        print("3. Ubah Data Perangkat         (Update)")
        print("4. Hapus Perangkat             (Delete)")
        print("0. Kembali ke Menu Utama")
        print("="*50)
        pilihan = input("Pilih Menu [0-4]: ").strip()

        if pilihan == "1":
            tambah_perangkat(daftar_perangkat)
            jeda_layar()
        elif pilihan == "2":
            tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "3":
            tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            ubah_perangkat(daftar_perangkat)
            jeda_layar()
        elif pilihan == "4":
            tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            hapus_perangkat(daftar_perangkat)
            jeda_layar()
        elif pilihan == "0":
            break
        else:
            print("[!] Pilihan tidak valid!")

def menu_pencarian_pengurutan(daftar_perangkat, profil_rumah):
    """Sub-menu untuk fitur Searching & Sorting manual."""
    while True:
        print("\n" + "="*60)
        print(f"       {Warna.CYAN}{Warna.TEBAL}FITUR PENCARIAN & PENGURUTAN (SEARCH & SORT){Warna.RESET}")
        print("="*60)
        print("1. Cari Perangkat Berdasarkan Nama       (Linear Search)")
        print("2. Cari Perangkat Berdasarkan Ruangan    (Linear Search)")
        print("3. Cari Perangkat Berdasarkan ID         (Binary Search Rekursif O(log n))")
        print("4. Filter Perangkat Daya Tinggi (Watt)")
        print("5. Urutkan dari yang Paling Boros        (Optimized Bubble Sort)")
        print("6. Urutkan berdasarkan Vampire Power     (Bubble Sort)")
        print("7. Urutkan berdasarkan Daya Aktif Watt   (Insertion Sort)")
        print("8. Urutkan berdasarkan Tingkat Prioritas (Selection Sort)")
        print("9. Cek Bentrok Jam 2 Perangkat Spesifik  (Set Intersection)")
        print("10. Gabungkan Jam Operasional Ruangan    (Set Union)")
        print("11. Deteksi Perangkat Non-Hemat Energi   (Set Difference)")
        print("0. Kembali ke Menu Utama")
        print("="*60)
        pilihan = input("Pilih Opsi [0-11]: ").strip()

        if pilihan == "1":
            keyword = input("Masukkan kata kunci nama: ")
            hasil = cari_perangkat_nama(daftar_perangkat, keyword)
            tampilkan_tabel_perangkat(hasil, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "2":
            ruang = input("Masukkan nama ruangan: ")
            hasil = cari_perangkat_ruangan(daftar_perangkat, ruang)
            tampilkan_tabel_perangkat(hasil, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "3":
            id_target = input("Masukkan ID Perangkat yang dicari (cth: EL03): ").strip()
            hasil, langkah = cari_perangkat_id_binary(daftar_perangkat, id_target)
            if hasil:
                print(f"\n{Warna.HIJAU}[v] Perangkat ditemukan dalam {langkah} langkah rekursif O(log n):{Warna.RESET}")
                tampilkan_tabel_perangkat([hasil], profil_rumah["tarif"])
            else:
                print(f"\n{Warna.MERAH}[!] Perangkat dengan ID '{id_target}' tidak ditemukan (diperiksa dalam {langkah} langkah rekursi).{Warna.RESET}")
            jeda_layar()
        elif pilihan == "4":
            try:
                min_w = int(input("Masukkan batas minimal Watt: "))
                hasil = cari_perangkat_daya_tinggi(daftar_perangkat, min_w)
                tampilkan_tabel_perangkat(hasil, profil_rumah["tarif"])
            except ValueError:
                print(f"{Warna.MERAH}[!] Input harus angka!{Warna.RESET}")
            jeda_layar()
        elif pilihan == "5":
            terurut = urutkan_perangkat_biaya(daftar_perangkat, profil_rumah["tarif"], descending=True)
            print(f"\n[*] Data diurutkan dari Biaya Bulanan Tertinggi ke Terendah ({Warna.TEBAL}Optimized Bubble Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "6":
            terurut = urutkan_perangkat_vampire(daftar_perangkat, descending=True)
            print(f"\n[*] Data diurutkan dari Daya Standby Terbesar ({Warna.TEBAL}Bubble Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "7":
            terurut = urutkan_perangkat_watt_insertion(daftar_perangkat, descending=True)
            print(f"\n[*] Data diurutkan dari Beban Daya Aktif Terbesar ({Warna.TEBAL}Manual Insertion Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "8":
            terurut = urutkan_perangkat_prioritas(daftar_perangkat)
            print(f"\n[*] Data diurutkan dari Prioritas: Primer -> Sekunder -> Tersier ({Warna.TEBAL}Selection Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "9":
            # Cek bentrok jam 2 perangkat (Set Intersection)
            tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            id1 = input("\nMasukkan ID Perangkat Pertama (cth: EL02): ").strip().upper()
            id2 = input("Masukkan ID Perangkat Kedua   (cth: EL04): ").strip().upper()
            p1, _ = cari_perangkat_id_binary(daftar_perangkat, id1)
            p2, _ = cari_perangkat_id_binary(daftar_perangkat, id2)
            if p1 and p2:
                bentrok = deteksi_bentrok_jam_perangkat(p1, p2)
                print("\n" + "="*55)
                print(f" {Warna.CYAN}{Warna.TEBAL}HASIL DETEKSI IRISAN JAM (SET INTERSECTION){Warna.RESET}")
                print("="*55)
                print(f" Perangkat 1: {p1['nama']} ({p1['watt_aktif']} W) -> Jam: {p1.get('rentang_jam', [])}")
                print(f" Perangkat 2: {p2['nama']} ({p2['watt_aktif']} W) -> Jam: {p2.get('rentang_jam', [])}")
                if bentrok:
                    jam_str = ", ".join(f"{j:02d}:00" for j in bentrok)
                    beban_bersama = p1['watt_aktif'] + p2['watt_aktif']
                    print(f" {Warna.KUNING}[*] Jam Nyala Bersamaan (Irisan) : {jam_str}{Warna.RESET}")
                    print(f" Total Beban Tambahan saat Bentrok: {beban_bersama} Watt")
                else:
                    print(f" {Warna.HIJAU}[v] Tidak ada jam menyala yang bentrok (Irisan Himpunan Kosong).{Warna.RESET}")
                print("="*55)
            else:
                print(f"{Warna.MERAH}[!] Salah satu atau kedua ID perangkat tidak ditemukan!{Warna.RESET}")
            jeda_layar()
        elif pilihan == "10":
            # Gabungkan jam ruangan (Set Union)
            ruang1 = input("Masukkan Nama Ruangan Pertama (cth: Dapur): ").strip()
            ruang2 = input("Masukkan Nama Ruangan Kedua (opsional, ENTER jika hanya 1): ").strip()
            gabungan, jam_a, jam_b = gabungkan_jam_aktif_ruangan(daftar_perangkat, ruang1, ruang2 if ruang2 else None)
            print("\n" + "="*55)
            print(f" {Warna.CYAN}{Warna.TEBAL}HASIL PENGGABUNGAN JAM OPERASIONAL (SET UNION){Warna.RESET}")
            print("="*55)
            print(f" Ruangan 1 [{ruang1}]  : {jam_a if jam_a else '(tidak ada perangkat aktif)'}")
            if ruang2:
                print(f" Ruangan 2 [{ruang2}]  : {jam_b if jam_b else '(tidak ada perangkat aktif)'}")
            print(f" {Warna.HIJAU}{Warna.TEBAL}Total Jam Terbuka (Union) : {gabungan}{Warna.RESET}")
            print(f" Total Durasi Aktif Unik   : {len(gabungan)} Jam dalam sehari")
            print("="*55)
            jeda_layar()
        elif pilihan == "11":
            boros = deteksi_perangkat_boros(daftar_perangkat)
            print(f"\n[*] Hasil Deteksi Himpunan Perangkat Non-Hemat Energi ({Warna.TEBAL}Set Difference{Warna.RESET}):")
            tampilkan_tabel_perangkat(boros, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "0":
            break
        else:
            print(f"{Warna.MERAH}[!] Pilihan tidak valid!{Warna.RESET}")

def menu_profil_daya(profil_rumah):
    """Sub-menu untuk mengubah profil daya rumah dan transaksi token PLN."""
    while True:
        print("\n" + "="*55)
        print(f"          {Warna.CYAN}{Warna.TEBAL}PENGATURAN DAYA RUMAH & TOKEN LISTRIK{Warna.RESET}")
        print("="*55)
        print(f" Golongan Saat Ini    : {profil_rumah['golongan']} ({profil_rumah['va']} VA)")
        print(f" Batas Daya Aman      : {profil_rumah['batas_watt']} Watt")
        print(f" Tarif Dasar Listrik  : {format_rupiah(profil_rumah['tarif'])} /kWh")
        print(f" Sisa Token di Meter  : {Warna.HIJAU}{Warna.TEBAL}{profil_rumah['sisa_token_kwh']:.2f} kWh{Warna.RESET}")
        print("-" * 55)
        print("1. Ubah Golongan Daya PLN (Pilih Daftar Tarif)")
        print("2. Beli / Top-Up Token Listrik Baru (Cetak Struk 20 Digit)")
        print("3. Perbarui Sisa Token kWh Meteran Manual")
        print("0. Kembali ke Menu Utama")
        print("="*55)
        pilihan = input("Pilih Menu [0-3]: ").strip()

        if pilihan == "1":
            print("\nDAFTAR GOLONGAN TARIF PLN TERSEDIA:")
            # [MATERI: TUPLE UNPACKING]
            for i, gol in enumerate(GOLONGAN_PLN, 1):
                kode, va, batas_w, tarif = gol
                print(f"{i}. {kode:<8} | Daya: {va:>4} VA | Batas Aman: {batas_w:>4} W | {format_rupiah(tarif)}/kWh")

            pilih_gol = input(f"Pilih Golongan [1-{len(GOLONGAN_PLN)}]: ").strip()
            if pilih_gol.isdigit() and 1 <= int(pilih_gol) <= len(GOLONGAN_PLN):
                idx = int(pilih_gol) - 1
                kode, va, batas_w, tarif = GOLONGAN_PLN[idx]
                profil_rumah["golongan"] = kode
                profil_rumah["va"] = va
                profil_rumah["batas_watt"] = batas_w
                profil_rumah["tarif"] = tarif
                simpan_profil(kode, va, batas_w, tarif, profil_rumah["sisa_token_kwh"])
                print(f"\n{Warna.HIJAU}[OK] Profil berhasil diubah ke {kode} ({va} VA)!{Warna.RESET}")
            else:
                print(f"{Warna.MERAH}[!] Pilihan golongan tidak valid.{Warna.RESET}")
            jeda_layar()

        elif pilihan == "2":
            print("\nPILIH NOMINAL PEMBELIAN TOKEN LISTRIK (PLN PRABAYAR):")
            print("1. Rp 20.000")
            print("2. Rp 50.000")
            print("3. Rp 100.000")
            print("4. Rp 200.000")
            print("5. Rp 500.000")
            print("6. Nominal Kustom")
            opsi_nom = input("Pilih Opsi [1-6]: ").strip()
            daftar_nom = {"1": 20000, "2": 50000, "3": 100000, "4": 200000, "5": 500000}

            nominal = 0
            if opsi_nom in daftar_nom:
                nominal = daftar_nom[opsi_nom]
            elif opsi_nom == "6":
                try:
                    nominal = float(input("Masukkan nominal pembelian (Rp): ").replace(".", "").replace(",", ""))
                except ValueError:
                    print(f"{Warna.MERAH}[!] Nominal tidak valid!{Warna.RESET}")
            else:
                print(f"{Warna.MERAH}[!] Pilihan tidak valid.{Warna.RESET}")

            if nominal >= 10000:
                struk = beli_token_listrik(profil_rumah, nominal)
                tampilkan_struk_token(struk, profil_rumah)
            elif nominal > 0:
                print(f"{Warna.MERAH}[!] Minimal pembelian token PLN adalah Rp 10.000!{Warna.RESET}")
            jeda_layar()

        elif pilihan == "3":
            try:
                token_input = float(input("Masukkan sisa kWh di meteran listrik saat ini: "))
                if token_input >= 0:
                    profil_rumah["sisa_token_kwh"] = token_input
                    simpan_profil(
                        profil_rumah["golongan"],
                        profil_rumah["va"],
                        profil_rumah["batas_watt"],
                        profil_rumah["tarif"],
                        profil_rumah["sisa_token_kwh"]
                    )
                    print(f"\n{Warna.HIJAU}[OK] Sisa token berhasil diperbarui menjadi {token_input:.2f} kWh!{Warna.RESET}")
                else:
                    print(f"{Warna.MERAH}[!] Nilai kWh tidak boleh negatif.{Warna.RESET}")
            except ValueError:
                print(f"{Warna.MERAH}[!] Masukkan angka desimal/bulat yang valid.{Warna.RESET}")
            jeda_layar()

        elif pilihan == "0":
            break
        else:
            print(f"{Warna.MERAH}[!] Pilihan tidak valid!{Warna.RESET}")

def main():
    """Fungsi utama program (Entry Point)."""
    # Memuat profil dan daftar perangkat dari file teks
    profil_rumah = muat_profil()
    daftar_perangkat = muat_perangkat()

    # [MATERI: WHILE LOOP - NAVIGASI APLIKASI CLI]
    while True:
        print("\n" + "="*65)
        print(f"     {Warna.CYAN}{Warna.TEBAL}⚡ WATTWISE HOME — AUDIT LISTRIK & ANTI-JEGLEK ⚡{Warna.RESET}")
        print(f"   Daya: {Warna.KUNING}{profil_rumah['golongan']} ({profil_rumah['va']} VA){Warna.RESET} | Sisa Token: {Warna.HIJAU}{profil_rumah['sisa_token_kwh']:.1f} kWh{Warna.RESET}")
        print("="*65)
        print("1. Manajemen Data Perangkat Elektronik       (CRUD Lengkap)")
        print("2. Pencarian & Pengurutan Data               (Search & Sort Manual)")
        print("3. Simulasi Beban 24 Jam & Anti-Jeglek       (Nested Loop Matrix)")
        print("4. Detektor Vampire Power & Audit Ruangan    (Kebocoran Standby)")
        print("5. Prediksi Habisnya Token & Budget Diet     (Fitur Cerdas)")
        print("6. Pengaturan Profil Daya Rumah & Token      (Tuple Tarif PLN)")
        print("7. Export Laporan Resmi Audit Listrik        (File .txt)")
        print("0. Keluar Aplikasi")
        print("="*65)

        pilihan = input("Masukkan Pilihan Anda [0-7]: ").strip()

        if pilihan == "1":
            menu_kelola_perangkat(daftar_perangkat, profil_rumah)
        elif pilihan == "2":
            menu_pencarian_pengurutan(daftar_perangkat, profil_rumah)
        elif pilihan == "3":
            simulasi_beban_24jam(daftar_perangkat, profil_rumah["batas_watt"], profil_rumah["va"])
            jeda_layar()
        elif pilihan == "4":
            audit_per_ruangan(daftar_perangkat, profil_rumah["tarif"])
            analisis_vampire_power(daftar_perangkat, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "5":
            prediksi_habis_token(daftar_perangkat, profil_rumah)
            smart_budget_optimizer(daftar_perangkat, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "6":
            menu_profil_daya(profil_rumah)
        elif pilihan == "7":
            export_laporan_audit(daftar_perangkat, profil_rumah)
            jeda_layar()
        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan WattWise Home!")
            print("Bijak menggunakan energi, selamatkan kantong & bumi.\n")
            sys.exit(0)
        else:
            print("[!] Pilihan menu tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
