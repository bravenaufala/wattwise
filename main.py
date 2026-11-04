# ==============================================================================
# WATTWISE HOME — SIMULATOR AUDIT LISTRIK, ANTI-JEGLEK & DETEKTOR VAMPIRE POWER
# File Utama: main.py
# Mata Kuliah: Praktikum Dasar Pemrograman (Python)
# Tim Pengembang:
# - Anggota 1: Core Data, File Handling, CRUD (Create & Read)
# - Anggota 2: CRUD (Update & Delete), Searching, Sorting & Set Operations
# - Anggota 3: Nested Loop (Simulasi 24 Jam), Export Laporan, Prediksi & Budget Optimizer
# ==============================================================================

import sys
import os

# Import fungsi-fungsi modular dari berkas terpisah
from modul_crud import (
    GOLONGAN_PLN,
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
    urutkan_perangkat_biaya,
    urutkan_perangkat_vampire,
    urutkan_perangkat_prioritas,
    deteksi_bentrok_jam_perangkat,
    deteksi_perangkat_boros,
    export_laporan_audit
)

from modul_prediksi import (
    prediksi_habis_token,
    smart_budget_optimizer
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
        print("\n" + "="*55)
        print("       FITUR PENCARIAN & PENGURUTAN (SEARCH & SORT)")
        print("="*55)
        print("1. Cari Perangkat Berdasarkan Nama       (Linear Search)")
        print("2. Cari Perangkat Berdasarkan Ruangan    (Linear Search)")
        print("3. Filter Perangkat Daya Tinggi (Watt)")
        print("4. Urutkan dari yang Paling Boros        (Bubble Sort)")
        print("5. Urutkan berdasarkan Vampire Power     (Bubble Sort)")
        print("6. Urutkan berdasarkan Tingkat Prioritas (Selection Sort)")
        print("7. Deteksi Perangkat Non-Hemat Energi    (Set Difference)")
        print("0. Kembali ke Menu Utama")
        print("="*55)
        pilihan = input("Pilih Opsi [0-7]: ").strip()

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
            try:
                min_w = int(input("Masukkan batas minimal Watt: "))
                hasil = cari_perangkat_daya_tinggi(daftar_perangkat, min_w)
                tampilkan_tabel_perangkat(hasil, profil_rumah["tarif"])
            except ValueError:
                print("[!] Input harus angka!")
            jeda_layar()
        elif pilihan == "4":
            terurut = urutkan_perangkat_biaya(daftar_perangkat, profil_rumah["tarif"], descending=True)
            print("\n[*] Data diurutkan dari Biaya Bulanan Tertinggi ke Terendah:")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "5":
            terurut = urutkan_perangkat_vampire(daftar_perangkat, descending=True)
            print("\n[*] Data diurutkan dari Daya Standby Terbesar:")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "6":
            terurut = urutkan_perangkat_prioritas(daftar_perangkat)
            print("\n[*] Data diurutkan dari Prioritas: Primer -> Sekunder -> Tersier:")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "7":
            boros = deteksi_perangkat_boros(daftar_perangkat)
            print("\n[*] Hasil Deteksi Himpunan Perangkat Non-Hemat Energi (Daya > 200W atau Standby > 15W):")
            tampilkan_tabel_perangkat(boros, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "0":
            break
        else:
            print("[!] Pilihan tidak valid!")

def menu_profil_daya(profil_rumah):
    """Sub-menu untuk mengubah profil daya rumah dan golongan PLN."""
    while True:
        print("\n" + "="*55)
        print("          PENGATURAN DAYA RUMAH & TOKEN LISTRIK")
        print("="*55)
        print(f" Golongan Saat Ini    : {profil_rumah['golongan']} ({profil_rumah['va']} VA)")
        print(f" Batas Daya Aman      : {profil_rumah['batas_watt']} Watt")
        print(f" Tarif Dasar Listrik  : {format_rupiah(profil_rumah['tarif'])} /kWh")
        print(f" Sisa Token di Meter  : {profil_rumah['sisa_token_kwh']:.2f} kWh")
        print("-" * 55)
        print("1. Ubah Golongan Daya PLN (Pilih Daftar Tarif)")
        print("2. Perbarui Sisa Token kWh Meteran")
        print("0. Kembali ke Menu Utama")
        print("="*55)
        pilihan = input("Pilih Menu [0-2]: ").strip()

        if pilihan == "1":
            print("\nDAFTAR GOLONGAN TARIF PLN TERSEDIA:")
            # [MATERI: TUPLE UNPACKING]
            for i, gol in enumerate(GOLONGAN_PLN, 1):
                kode, va, batas_w, tarif = gol
                print(f"{i}. {kode:<8} | Daya: {va:>4} VA | Batas Aman: {batas_w:>4} W | {format_rupiah(tarif)}/kWh")

            pilih_gol = input(f"Pilih Golongan [1-{len(GOLONGAN_PLN)}]: ").strip()
            if pilih_gol.isdigit() and 1 <= int(pilih_gol) <= len(GOLONGAN_PLN):
                idx = int(pilih_gol) - 1
                # [MATERI: TUPLE UNPACKING LAGI]
                kode, va, batas_w, tarif = GOLONGAN_PLN[idx]
                profil_rumah["golongan"] = kode
                profil_rumah["va"] = va
                profil_rumah["batas_watt"] = batas_w
                profil_rumah["tarif"] = tarif
                simpan_profil(kode, va, batas_w, tarif, profil_rumah["sisa_token_kwh"])
                print(f"\n[OK] Profil berhasil diubah ke {kode} ({va} VA)!")
            else:
                print("[!] Pilihan golongan tidak valid.")
            jeda_layar()

        elif pilihan == "2":
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
                    print(f"\n[OK] Sisa token berhasil diperbarui menjadi {token_input:.2f} kWh!")
                else:
                    print("[!] Nilai kWh tidak boleh negatif.")
            except ValueError:
                print("[!] Masukkan angka desimal/bulat yang valid.")
            jeda_layar()

        elif pilihan == "0":
            break
        else:
            print("[!] Pilihan tidak valid!")

def main():
    """Fungsi utama program (Entry Point)."""
    # Memuat profil dan daftar perangkat dari file teks
    profil_rumah = muat_profil()
    daftar_perangkat = muat_perangkat()

    # [MATERI: WHILE LOOP - NAVIGASI APLIKASI CLI]
    while True:
        print("\n" + "="*65)
        print("          ⚡ WATTWISE HOME — AUDIT LISTRIK & ANTI-JEGLEK ⚡")
        print(f"      Daya Rumah: {profil_rumah['golongan']} ({profil_rumah['va']} VA) | Token: {profil_rumah['sisa_token_kwh']:.1f} kWh")
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
