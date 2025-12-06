import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ObatNode:
    def _init_(self, nama, harga, stok, kadaluarsa):
        self.nama = nama
        self.harga = harga
        self.stok = stok
        self.kadaluarsa = kadaluarsa
        self.next = None

    def _repr_(self):
        return f"{self.nama} | Rp{self.harga} | Stok:{self.stok} | Exp:{self.kadaluarsa}"
        
class Inventori:
    def _init_(self):
        self.head = None       # Linked List
        self.hash = {}         # Hash Table
        self.queue = []        # Queue untuk pembelian

    def tambah(self, nama, harga, stok, exp):
        if nama in self.hash:
            return False

        node = ObatNode(nama, harga, stok, exp)
        node.next = self.head
        self.head = node

        self.hash[nama] = node
        return True

    def ubah(self, nama, harga, stok, exp):
        if nama not in self.hash:
            return False

        o = self.hash[nama]
        o.harga = harga
        o.stok = stok
        o.kadaluarsa = exp
        return True

    def hapus(self, nama):
        if nama not in self.hash:
            return False

        curr = self.head
        prev = None

        while curr:
            if curr.nama == nama:
                break
            prev = curr
            curr = curr.next

        if prev:
            prev.next = curr.next
        else:
            self.head = curr.next

        del self.hash[nama]
        return True


    def beli(self, nama, jumlah):
        if nama not in self.hash:
            return None

        o = self.hash[nama]
        if o.stok < jumlah:
            return False

        try:
            if datetime.strptime(o.kadaluarsa, "%Y-%m-%d") < datetime.today():
                return "exp"
        except:
            return "format"

        self.queue.append((nama, jumlah))

        nama_beli, jml = self.queue.pop(0)
        o.stok -= jml
        return True

    def cari(self, nama):
        return self.hash.get(nama)

    # bubble sort
    def sort_nama(self):
        arr = []
        curr = self.head
        while curr:
            arr.append(curr)
            curr = curr.next

        for i in range(len(arr) - 1):
            for j in range(len(arr) - i - 1):
                if arr[j].nama > arr[j + 1].nama:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr

    # linked list (smw list)
    def semua(self):
        hasil = []
        curr = self.head
        while curr:
            hasil.append(curr)
            curr = curr.next
        return hasil
#GUI
class Aplikasi:
    def __init__(self, root):
        self.inv = Inventori()
        root.title("Inventaris Apotek")
        root.geometry("1000x600")
        root.resizable(False, False)

        main = ttk.Frame(root, padding=10)
        main.pack(fill="both", expand=True)

        kiri = ttk.Frame(main)
        kiri.grid(row=0, column=0, sticky="nw")

        kanan = ttk.Frame(main)
        kanan.grid(row=0, column=1, sticky="ne", padx=25)

        # nama input
        self.field(kiri, "Nama Obat", "nama", 0)
        self.field(kiri, "Harga", "harga", 1)
        self.field(kiri, "Stok", "stok", 2)
        self.field(kiri, "Kadaluarsa (YYYY-MM-DD)", "exp", 3)
