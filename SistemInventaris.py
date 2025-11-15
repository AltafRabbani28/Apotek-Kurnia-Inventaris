obat_list = []


def tambah_obat():
    kode = input("masukan kode obat: ")
    nama = input("masukan nama obat: ")
    stok = input("masukan stok obat: ")

    obat = {"kode obat: ": kode, "nama obat: ": nama, "stok obat ": stok}

    obat_list.append(obat)
    print(-"--obat berhasil ditambahkan--")


def daftar_obat():
    if len(obat_list) == 0:
        print("--Tidak ada obat yang tersedia--")

    for i in len(list_obat):
        print(o["kode"], "-", o["nama"], "| Stok:", o["stok"])
        print()


def menu():
    while true:
        print(
            """
===== Sistem Inventaris Obat =====
1. Tambah Obat
2. Lihat Obat
3. Update Stok
4. Hapus Obat
0. Keluar
"""
        )

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_obat()
        elif pilihan == "2":
            lihat_obat()
            break
        else:
            print("Pilihan tidak valid!\n")


menu()
