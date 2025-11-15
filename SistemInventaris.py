obat_list = []

def tambah_obat():
    print("=== Tambah Obat ===")
    kode = input("Masukan kode obat: ")
    nama = input("Masukan nama obat: ")
    stok = input("Masukan stok obat: ")

    obat = {
        "kode": kode,
        "nama": nama,
        "stok": stok
    }

    obat_list.append(obat)
    print("-- Obat berhasil ditambahkan --")

def daftar_obat():
    print("=== Daftar Obat ===")

    if len(obat_list) == 0:
        print("-- Tidak ada obat yang tersedia --")
    

    for i in range(len(obat_list)):
        print(obat_list[i]["kode"], "-", obat_list[i]["nama"], "| Stok:", obat_list[i]["stok"])
    print()

def menu():
    while True:
        print("""
===== Sistem Inventaris Obat (Versi Mudah) =====
1. Tambah Obat
2. Daftar Obat
3. Update Stok
4. Hapus Obat
0. Keluar
""")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_obat()
        elif pilihan == "2":
            daftar_obat()
        elif pilihan == "3":
            update_stok
        elif pilihan == "4":
            hapus_obat
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid!")

menu()
