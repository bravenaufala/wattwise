import os
import sys

# Aktifkan dukungan ANSI escape color pada terminal Windows
os.system("")

from modul_crud import (
    GOLONGAN_PLN,
    Warna,
    bersihkan_layar,
    cetak_header,
    cetak_garis,
    muat_profil,
    simpan_profil,
    muat_perangkat,
    tambah_perangkat,
    tampilkan_tabel_perangkat,
    ubah_perangkat,
    hapus_perangkat,
    format_rupiah,
    lihat_log_aktivitas
)
from modul_analisis import (
    simulasi_beban_24jam,
    analisis_vampire_power,
    audit_per_ruangan,
    ambil_himpunan_ruangan,
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
    export_laporan_audit,
    smart_budget_optimizer
)
from modul_prediksi import (
    prediksi_habis_token,
    beli_token_listrik,
    tampilkan_struk_token,
    tampilkan_grafik_sisa_token
)


def jeda_layar():
    input(f"\n  {Warna.REDUP}[ Tekan ENTER untuk kembali... ]{Warna.RESET}")


def cetak_item_menu(nomor, label, keterangan="", lebar_label=42):
    nomor_fmt = f"{Warna.CYAN}{Warna.TEBAL}[{nomor:>2}]{Warna.RESET}" if len(str(nomor)) > 1 else f"{Warna.CYAN}{Warna.TEBAL}[{nomor}]{Warna.RESET} "
    if keterangan:
        print(f"  {nomor_fmt} {label:<{lebar_label}} {Warna.REDUP}{keterangan}{Warna.RESET}")
    else:
        print(f"  {nomor_fmt} {label}")


def menu_kelola_perangkat(daftar_perangkat, profil_rumah):
    while True:
        bersihkan_layar()
        cetak_header("MANAJEMEN DATA PERANGKAT (CRUD)", f"Total Tercatat: {len(daftar_perangkat)} perangkat", lebar=66)
        cetak_item_menu(1, "Tambah Perangkat Baru", "(Create)", 36)
        cetak_item_menu(2, "Lihat Inventaris Perangkat", "(Read / Filter Ruangan)", 36)
        cetak_item_menu(3, "Ubah Data Perangkat", "(Update + Diff)", 36)
        cetak_item_menu(4, "Hapus Perangkat", "(Delete)", 36)
        cetak_item_menu(5, "Riwayat Log Aktivitas", "(Audit Trail)", 36)
        cetak_garis(66)
        cetak_item_menu(0, "Kembali ke Menu Utama", "", 36)
        cetak_garis(66)
        pilihan = input("  Pilih menu [0-5]: ").strip()

        if pilihan == "1":
            bersihkan_layar()
            tambah_perangkat(daftar_perangkat)
            jeda_layar()
        elif pilihan == "2":
            bersihkan_layar()
            if not daftar_perangkat:
                print(f"\n  {Warna.KUNING}[i] Belum ada data perangkat. Silakan tambahkan perangkat terlebih dahulu.{Warna.RESET}")
                jeda_layar()
                continue

            cetak_header("OPSI TAMPILAN INVENTARIS", lebar=54)
            cetak_item_menu(1, "Tampilkan Semua Alat", "", 34)
            cetak_item_menu(2, "Filter Berdasarkan Ruangan", "", 34)
            cetak_garis(54)
            sub_pilih = input("  Pilih opsi [1/2, default 1]: ").strip()

            if sub_pilih == "2":
                ruangan_unik = sorted(list(ambil_himpunan_ruangan(daftar_perangkat)))
                if not ruangan_unik:
                    print(f"  {Warna.KUNING}[!] Belum ada data ruangan.{Warna.RESET}")
                else:
                    print(f"\n  {Warna.CYAN}Daftar Ruangan Tersedia:{Warna.RESET}")
                    for idx_r, r in enumerate(ruangan_unik, 1):
                        print(f"    {idx_r}. {r}")
                    input_ruang = input(f"  Pilih nomor [1-{len(ruangan_unik)}] atau ketik nama ruangan: ").strip()

                    ruang_target = ""
                    if input_ruang.isdigit() and 1 <= int(input_ruang) <= len(ruangan_unik):
                        ruang_target = ruangan_unik[int(input_ruang) - 1]
                    elif input_ruang:
                        ruang_target = input_ruang

                    if ruang_target:
                        hasil_filter = cari_perangkat_ruangan(daftar_perangkat, ruang_target)
                        if hasil_filter:
                            bersihkan_layar()
                            tampilkan_tabel_perangkat(hasil_filter, profil_rumah["tarif"], judul_filter=ruang_target)
                        else:
                            print(f"\n  {Warna.MERAH}[!] Tidak ada perangkat ditemukan di ruangan '{ruang_target}'!{Warna.RESET}")
                    else:
                        print(f"  {Warna.KUNING}[*] Pemilihan ruangan dibatalkan.{Warna.RESET}")
            else:
                bersihkan_layar()
                tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "3":
            bersihkan_layar()
            tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            ubah_perangkat(daftar_perangkat)
            jeda_layar()
        elif pilihan == "4":
            bersihkan_layar()
            tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            hapus_perangkat(daftar_perangkat)
            jeda_layar()
        elif pilihan == "5":
            bersihkan_layar()
            lihat_log_aktivitas()
            jeda_layar()
        elif pilihan == "0":
            break
        else:
            print(f"\n  {Warna.MERAH}[!] Pilihan tidak valid!{Warna.RESET}")
            jeda_layar()


def menu_pencarian_pengurutan(daftar_perangkat, profil_rumah):
    while True:
        bersihkan_layar()
        cetak_header("PENCARIAN, PENGURUTAN & OPERASI SET", lebar=72)
        cetak_item_menu(1, "Cari Berdasarkan Nama", "(Linear Search)", 40)
        cetak_item_menu(2, "Cari Berdasarkan Ruangan", "(Linear Search)", 40)
        cetak_item_menu(3, "Cari Berdasarkan ID", "(Binary Search Rekursif)", 40)
        cetak_item_menu(4, "Filter Perangkat Daya Tinggi", "(Min Watt)", 40)
        cetak_garis(72)
        cetak_item_menu(5, "Urutkan Paling Boros", "(Bubble Sort)", 40)
        cetak_item_menu(6, "Urutkan Vampire Power", "(Bubble Sort)", 40)
        cetak_item_menu(7, "Urutkan Daya Aktif Watt", "(Insertion Sort)", 40)
        cetak_item_menu(8, "Urutkan Tingkat Prioritas", "(Selection Sort)", 40)
        cetak_garis(72)
        cetak_item_menu(9, "Cek Bentrok Jam 2 Perangkat", "(Set Intersection)", 40)
        cetak_item_menu(10, "Gabungkan Jam Operasional Ruangan", "(Set Union)", 40)
        cetak_item_menu(11, "Deteksi Perangkat Non-Hemat", "(Set Difference)", 40)
        cetak_garis(72)
        cetak_item_menu(0, "Kembali ke Menu Utama", "", 40)
        cetak_garis(72)
        pilihan = input("  Pilih opsi [0-11]: ").strip()

        if pilihan == "1":
            keyword = input("  Masukkan kata kunci nama: ")
            bersihkan_layar()
            hasil = cari_perangkat_nama(daftar_perangkat, keyword)
            tampilkan_tabel_perangkat(hasil, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "2":
            ruang = input("  Masukkan nama ruangan: ")
            bersihkan_layar()
            hasil = cari_perangkat_ruangan(daftar_perangkat, ruang)
            tampilkan_tabel_perangkat(hasil, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "3":
            id_target = input("  Masukkan ID Perangkat (cth: EL03): ").strip()
            bersihkan_layar()
            hasil, langkah = cari_perangkat_id_binary(daftar_perangkat, id_target)
            if hasil:
                print(f"\n  {Warna.HIJAU}[v] Perangkat ditemukan dalam {langkah} langkah rekursif:{Warna.RESET}")
                tampilkan_tabel_perangkat([hasil], profil_rumah["tarif"])
            else:
                print(f"\n  {Warna.MERAH}[!] Perangkat dengan ID '{id_target}' tidak ditemukan ({langkah} langkah).{Warna.RESET}")
            jeda_layar()
        elif pilihan == "4":
            try:
                min_w = int(input("  Masukkan batas minimal Watt: "))
                bersihkan_layar()
                hasil = cari_perangkat_daya_tinggi(daftar_perangkat, min_w)
                tampilkan_tabel_perangkat(hasil, profil_rumah["tarif"])
            except ValueError:
                print(f"  {Warna.MERAH}[!] Input harus angka!{Warna.RESET}")
            jeda_layar()
        elif pilihan == "5":
            bersihkan_layar()
            terurut = urutkan_perangkat_biaya(daftar_perangkat, profil_rumah["tarif"], descending=True)
            print(f"\n  [*] Diurutkan dari Biaya Bulanan Tertinggi ({Warna.TEBAL}Bubble Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "6":
            bersihkan_layar()
            terurut = urutkan_perangkat_vampire(daftar_perangkat, descending=True)
            print(f"\n  [*] Diurutkan dari Daya Standby Terbesar ({Warna.TEBAL}Bubble Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "7":
            bersihkan_layar()
            terurut = urutkan_perangkat_watt_insertion(daftar_perangkat, descending=True)
            print(f"\n  [*] Diurutkan dari Daya Aktif Terbesar ({Warna.TEBAL}Insertion Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "8":
            bersihkan_layar()
            terurut = urutkan_perangkat_prioritas(daftar_perangkat)
            print(f"\n  [*] Diurutkan dari Prioritas: Primer -> Sekunder -> Tersier ({Warna.TEBAL}Selection Sort{Warna.RESET}):")
            tampilkan_tabel_perangkat(terurut, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "9":
            bersihkan_layar()
            tampilkan_tabel_perangkat(daftar_perangkat, profil_rumah["tarif"])
            id1 = input("\n  Masukkan ID Perangkat Pertama (cth: EL02): ").strip().upper()
            id2 = input("  Masukkan ID Perangkat Kedua   (cth: EL04): ").strip().upper()
            p1, _ = cari_perangkat_id_binary(daftar_perangkat, id1)
            p2, _ = cari_perangkat_id_binary(daftar_perangkat, id2)
            if p1 and p2:
                bentrok = deteksi_bentrok_jam_perangkat(p1, p2)
                cetak_header("HASIL DETEKSI IRISAN JAM (SET INTERSECTION)", lebar=64)
                print(f"  Perangkat 1 : {p1['nama']} ({p1['watt_aktif']} W) -> {p1.get('rentang_jam', [])}")
                print(f"  Perangkat 2 : {p2['nama']} ({p2['watt_aktif']} W) -> {p2.get('rentang_jam', [])}")
                cetak_garis(64)
                if bentrok:
                    jam_str = ", ".join(f"{j:02d}:00" for j in bentrok)
                    beban_bersama = p1["watt_aktif"] + p2["watt_aktif"]
                    print(f"  {Warna.KUNING}[*] Jam Nyala Bersamaan : {jam_str}{Warna.RESET}")
                    print(f"  Total Beban Gabungan    : {Warna.TEBAL}{beban_bersama} Watt{Warna.RESET}")
                else:
                    print(f"  {Warna.HIJAU}[v] Tidak ada jam menyala yang bentrok.{Warna.RESET}")
                cetak_garis(64)
            else:
                print(f"  {Warna.MERAH}[!] Salah satu atau kedua ID perangkat tidak ditemukan!{Warna.RESET}")
            jeda_layar()
        elif pilihan == "10":
            ruang1 = input("  Masukkan Nama Ruangan Pertama (cth: Dapur): ").strip()
            ruang2 = input("  Masukkan Nama Ruangan Kedua (opsional, ENTER jika 1): ").strip()
            bersihkan_layar()
            gabungan, jam_a, jam_b = gabungkan_jam_aktif_ruangan(daftar_perangkat, ruang1, ruang2 if ruang2 else None)
            cetak_header("PENGGABUNGAN JAM OPERASIONAL (SET UNION)", lebar=64)
            print(f"  Ruangan 1 [{ruang1}] : {jam_a if jam_a else '(tidak ada perangkat aktif)'}")
            if ruang2:
                print(f"  Ruangan 2 [{ruang2}] : {jam_b if jam_b else '(tidak ada perangkat aktif)'}")
            cetak_garis(64)
            print(f"  {Warna.HIJAU}{Warna.TEBAL}Total Jam Aktif (Union) : {gabungan}{Warna.RESET}")
            print(f"  Total Durasi Aktif Unik : {len(gabungan)} jam / hari")
            cetak_garis(64)
            jeda_layar()
        elif pilihan == "11":
            bersihkan_layar()
            boros = deteksi_perangkat_boros(daftar_perangkat)
            print(f"\n  [*] Deteksi Perangkat Non-Hemat Energi ({Warna.TEBAL}Set Difference{Warna.RESET}):")
            tampilkan_tabel_perangkat(boros, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "0":
            break
        else:
            print(f"\n  {Warna.MERAH}[!] Pilihan tidak valid!{Warna.RESET}")
            jeda_layar()


def menu_profil_daya(profil_rumah):
    while True:
        bersihkan_layar()
        cetak_header("PENGATURAN DAYA RUMAH & TOKEN LISTRIK", lebar=66)
        print(f"  Golongan Saat Ini   : {Warna.KUNING}{profil_rumah['golongan']} ({profil_rumah['va']} VA){Warna.RESET}")
        print(f"  Batas Daya Aman     : {profil_rumah['batas_watt']} Watt")
        print(f"  Tarif Dasar Listrik : {format_rupiah(profil_rumah['tarif'])} /kWh")
        print(f"  Sisa Token di Meter : {Warna.HIJAU}{Warna.TEBAL}{profil_rumah['sisa_token_kwh']:.2f} kWh{Warna.RESET}")
        cetak_garis(66)
        cetak_item_menu(1, "Ubah Golongan Daya PLN", "(Tuple Tarif)", 38)
        cetak_item_menu(2, "Beli / Top-Up Token Listrik", "(Struk 20 Digit)", 38)
        cetak_item_menu(3, "Perbarui Sisa Token Manual", "(Input kWh)", 38)
        cetak_garis(66)
        cetak_item_menu(0, "Kembali ke Menu Utama", "", 38)
        cetak_garis(66)
        pilihan = input("  Pilih menu [0-3]: ").strip()

        if pilihan == "1":
            print("\n  DAFTAR GOLONGAN TARIF PLN:")
            cetak_garis(66)
            for i, gol in enumerate(GOLONGAN_PLN, 1):
                kode, va, batas_w, tarif = gol
                print(f"  [{i}] {kode:<8} │ {va:>4} VA │ Batas Aman: {batas_w:>4} W │ {format_rupiah(tarif)}/kWh")
            cetak_garis(66)

            pilih_gol = input(f"  Pilih golongan [1-{len(GOLONGAN_PLN)}]: ").strip()
            if pilih_gol.isdigit() and 1 <= int(pilih_gol) <= len(GOLONGAN_PLN):
                kode, va, batas_w, tarif = GOLONGAN_PLN[int(pilih_gol) - 1]
                profil_rumah["golongan"] = kode
                profil_rumah["va"] = va
                profil_rumah["batas_watt"] = batas_w
                profil_rumah["tarif"] = tarif
                simpan_profil(kode, va, batas_w, tarif, profil_rumah["sisa_token_kwh"])
                print(f"\n  {Warna.HIJAU}[OK] Profil berhasil diubah ke {kode} ({va} VA)!{Warna.RESET}")
            else:
                print(f"  {Warna.MERAH}[!] Pilihan golongan tidak valid.{Warna.RESET}")
            jeda_layar()

        elif pilihan == "2":
            print("\n  PILIH NOMINAL TOKEN LISTRIK (PLN PRABAYAR):")
            cetak_garis(66)
            print("  [1] Rp 20.000      [2] Rp 50.000      [3] Rp 100.000")
            print("  [4] Rp 200.000     [5] Rp 500.000     [6] Nominal Kustom")
            cetak_garis(66)
            opsi_nom = input("  Pilih opsi [1-6]: ").strip()
            daftar_nom = {"1": 20000, "2": 50000, "3": 100000, "4": 200000, "5": 500000}

            nominal = 0
            if opsi_nom in daftar_nom:
                nominal = daftar_nom[opsi_nom]
            elif opsi_nom == "6":
                try:
                    nominal = float(input("  Masukkan nominal pembelian (Rp): ").replace(".", "").replace(",", ""))
                except ValueError:
                    print(f"  {Warna.MERAH}[!] Nominal tidak valid!{Warna.RESET}")
            else:
                print(f"  {Warna.MERAH}[!] Pilihan tidak valid.{Warna.RESET}")

            if nominal >= 10000:
                bersihkan_layar()
                struk = beli_token_listrik(profil_rumah, nominal)
                tampilkan_struk_token(struk, profil_rumah)
            elif nominal > 0:
                print(f"  {Warna.MERAH}[!] Minimal pembelian token PLN adalah Rp 10.000!{Warna.RESET}")
            jeda_layar()

        elif pilihan == "3":
            try:
                token_input = float(input("  Masukkan sisa kWh di meteran listrik saat ini: "))
                if token_input >= 0:
                    profil_rumah["sisa_token_kwh"] = token_input
                    simpan_profil(
                        profil_rumah["golongan"],
                        profil_rumah["va"],
                        profil_rumah["batas_watt"],
                        profil_rumah["tarif"],
                        profil_rumah["sisa_token_kwh"]
                    )
                    print(f"\n  {Warna.HIJAU}[OK] Sisa token berhasil diperbarui menjadi {token_input:.2f} kWh!{Warna.RESET}")
                else:
                    print(f"  {Warna.MERAH}[!] Nilai kWh tidak boleh negatif.{Warna.RESET}")
            except ValueError:
                print(f"  {Warna.MERAH}[!] Masukkan angka desimal/bulat yang valid.{Warna.RESET}")
            jeda_layar()

        elif pilihan == "0":
            break
        else:
            print(f"\n  {Warna.MERAH}[!] Pilihan tidak valid!{Warna.RESET}")
            jeda_layar()


def main():
    profil_rumah = muat_profil()
    daftar_perangkat = muat_perangkat()

    while True:
        bersihkan_layar()
        cetak_header(
            "WATTWISE HOME - AUDIT LISTRIK & ANTI-JEGLEK",
            f"Daya: {profil_rumah['golongan']} ({profil_rumah['va']} VA)  |  Batas Aman: {profil_rumah['batas_watt']} W  |  Token: {profil_rumah['sisa_token_kwh']:.1f} kWh",
            lebar=74
        )
        cetak_item_menu(1, "Manajemen Data Perangkat Elektronik", "(CRUD & Log)")
        cetak_item_menu(2, "Pencarian, Pengurutan & Operasi Set", "(Search & Sort)")
        cetak_item_menu(3, "Simulasi Beban 24 Jam & Anti-Jeglek", "(Matriks Beban)")
        cetak_item_menu(4, "Detektor Vampire Power & Audit Ruangan", "(Daya Standby)")
        cetak_item_menu(5, "Prediksi Habisnya Token & Grafik Token", "(Analisis Token)")
        cetak_item_menu(6, "Pengaturan Profil Daya & Beli Token", "(Tarif PLN)")
        cetak_item_menu(7, "Export Laporan Resmi Audit Listrik", "(File .txt)")
        cetak_item_menu(8, "Smart Budget Optimizer", "(Greedy + Exclusion)")
        cetak_garis(74)
        cetak_item_menu(0, "Keluar Aplikasi")
        cetak_garis(74)

        pilihan = input("  Masukkan pilihan [0-8]: ").strip()

        if pilihan == "1":
            menu_kelola_perangkat(daftar_perangkat, profil_rumah)
        elif pilihan == "2":
            menu_pencarian_pengurutan(daftar_perangkat, profil_rumah)
        elif pilihan == "3":
            bersihkan_layar()
            simulasi_beban_24jam(daftar_perangkat, profil_rumah["batas_watt"], profil_rumah["va"])
            jeda_layar()
        elif pilihan == "4":
            bersihkan_layar()
            audit_per_ruangan(daftar_perangkat, profil_rumah["tarif"])
            analisis_vampire_power(daftar_perangkat, profil_rumah["tarif"])
            jeda_layar()
        elif pilihan == "5":
            bersihkan_layar()
            prediksi_habis_token(daftar_perangkat, profil_rumah)
            tampilkan_grafik_sisa_token()
            jeda_layar()
        elif pilihan == "6":
            menu_profil_daya(profil_rumah)
        elif pilihan == "7":
            bersihkan_layar()
            export_laporan_audit(daftar_perangkat, profil_rumah)
            jeda_layar()
        elif pilihan == "8":
            bersihkan_layar()
            try:
                cetak_header("SMART BUDGET OPTIMIZER", "Algoritma Greedy + Exclusion List", lebar=78)
                anggaran = float(input("  Masukkan anggaran maksimal per bulan (Rp): ").strip().replace(".", ""))
                if anggaran <= 0:
                    print(f"  {Warna.MERAH}[!] Anggaran harus lebih dari 0!{Warna.RESET}")
                else:
                    bersihkan_layar()
                    smart_budget_optimizer(daftar_perangkat, anggaran, profil_rumah["tarif"])
            except ValueError:
                print(f"  {Warna.MERAH}[!] Anggaran harus berupa angka!{Warna.RESET}")
            jeda_layar()
        elif pilihan == "0":
            bersihkan_layar()
            print("\n  Terima kasih telah menggunakan WattWise Home.")
            print("  Bijak menggunakan energi, hemat biaya listrik sehari-hari.\n")
            sys.exit(0)
        else:
            print(f"\n  {Warna.MERAH}[!] Pilihan menu tidak valid. Silakan coba lagi.{Warna.RESET}")
            jeda_layar()


if __name__ == "__main__":
    main()
