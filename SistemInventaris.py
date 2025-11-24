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

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ================= MODEL & STRUCTURE =================
class Obat:
    def _init_(self, nama, harga, stok, exp):
        self.nama, self.harga, self.stok, self.exp = nama, harga, stok, exp

    def _repr_(self):
        return f"{self.nama} | Rp{self.harga} | Stok:{self.stok} | Exp:{self.exp}"

class Node:
    def _init_(self, key, data):
        self.key, self.data = key, data
        self.left = self.right = None

class Inventory:
    def _init_(self):
        self.arr = []
        self.hash = {}
        self.stack = []
        self.queue = []
        self.pq = []
        self.tree = None
        self.graph = {}

    def insert_tree(self, node, key, data):
        if not node: return Node(key, data)
        if key < node.key: node.left = self.insert_tree(node.left, key, data)
        else: node.right = self.insert_tree(node.right, key, data)
        return node

    def tambah(self, n, h, s, e):
        if n in self.hash: return False
        o = Obat(n, h, s, e)
        self.arr.append(o)
        self.hash[n] = o
        self.pq.append((h, o))
        self.pq.sort()
        self.tree = self.insert_tree(self.tree, h, o)
        return True

    def cari(self, n): return self.hash.get(n)

    def hapus(self, n):
        o = self.cari(n)
        if not o: return False
        self.arr.remove(o)
        del self.hash[n]
        return True

    def update(self, n, h, s, e):
        o = self.cari(n)
        if not o: return False
        o.harga, o.stok, o.exp = h, s, e
        return True

    def beli(self, n, j):
        o = self.cari(n)
        if not o: return None
        if o.stok < j: return False
        if datetime.strptime(o.exp, "%Y-%m-%d") < datetime.today(): return "exp"
        o.stok -= j
        return True

    def sort_nama(self):
        a = self.arr[:]
        for i in range(len(a)-1):
            for j in range(len(a)-i-1):
                if a[j].nama > a[j+1].nama:
                    a[j], a[j+1] = a[j+1], a[j]
        return a

# ================= GUI =================
class App:
    def _init_(self, root):
        self.inv = Inventory()
        root.title("Inventaris Apotek - FIXED VERSION")
        root.geometry("720x600")

        # Scrollable area
        container = ttk.Frame(root)
        canvas = tk.Canvas(container, height=560)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.frame = ttk.Frame(canvas)

        self.frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Input fields
        self.field("Nama", "nama", 0)
        self.field("Harga", "harga", 1)
        self.field("Stok", "stok", 2)
        self.field("Exp (YYYY-MM-DD)", "exp", 3)

        ttk.Button(self.frame, text="Tambah", command=self.tambah).grid(row=4, column=0, pady=6)
        ttk.Button(self.frame, text="Update", command=self.update).grid(row=4, column=1)
        ttk.Button(self.frame, text="Hapus", command=self.hapus).grid(row=4, column=2)

        ttk.Separator(self.frame).grid(row=5, column=0, columnspan=3, sticky="ew", pady=10)

        # Penjualan
        self.field("Beli Nama", "beli_nama", 6)
        self.field("Jumlah", "jumlah", 7)
        ttk.Button(self.frame, text="Beli Obat", command=self.beli).grid(row=8, column=0, columnspan=3, pady=6)

        ttk.Separator(self.frame).grid(row=9, column=0, columnspan=3, pady=10, sticky="ew")

        # Cari
        self.field("Cari Nama", "cari_nama", 10)
        ttk.Button(self.frame, text="Cari", command=self.cari).grid(row=10, column=2)
        ttk.Button(self.frame, text="Sort Nama", command=self.sort).grid(row=11, column=0, pady=8)

        # Listbox
        self.box = tk.Listbox(self.frame, width=95, height=12, font=("Consolas", 10))
        self.box.grid(row=12, column=0, columnspan=3, pady=10)

    # Create field safely
    def field(self, label, name, row):
        ttk.Label(self.frame, text=label).grid(row=row, column=0, sticky="w", pady=3)
        entry = ttk.Entry(self.frame, width=30)
        entry.grid(row=row, column=1, padx=10)
        setattr(self, name, entry)

    # ========== ACTIONS ==========
    def tambah(self):
        try: h = int(self.harga.get()); s = int(self.stok.get())
        except: return messagebox.showerror("Err","Harga/Stok harus angka!")

        if self.inv.tambah(self.nama.get(), h, s, self.exp.get()):
            messagebox.showinfo("OK", "Obat ditambahkan")
        else:
            messagebox.showerror("Err", "Nama sudah ada")
        self.refresh()

    def update(self):
        try: h = int(self.harga.get()); s = int(self.stok.get())
        except: return messagebox.showerror("Err","Angka invalid")

        if self.inv.update(self.nama.get(), h, s, self.exp.get()):
            messagebox.showinfo("OK","Data diperbarui")
        else:
            messagebox.showerror("Err","Obat tidak ditemukan")
        self.refresh()

    def hapus(self):
        if self.inv.hapus(self.nama.get()):
            messagebox.showinfo("OK","Dihapus")
        else:
            messagebox.showerror("Err","Tidak ada")
        self.refresh()

    def beli(self):
        try: j=int(self.jumlah.get())
        except: return messagebox.showerror("Err","Jumlah harus angka!")

        res = self.inv.beli(self.beli_nama.get(), j)
        if res is None: return messagebox.showerror("Err","Tidak ditemukan")
        if res is False: return messagebox.showerror("Err","Stok kurang")
        if res == "exp": return messagebox.showerror("Err","Obat sudah kadaluarsa!")
        messagebox.showinfo("OK","Pembelian berhasil")
        self.refresh()

    def cari(self):
        o = self.inv.cari(self.cari_nama.get())
        messagebox.showinfo("Hasil", repr(o) if o else "Tidak ditemukan")

    def sort(self):
        self.box.delete(0, tk.END)
        for o in self.inv.sort_nama(): self.box.insert(tk.END, repr(o))

    def refresh(self):
        self.box.delete(0, tk.END)
        for o in self.inv.arr:
            self.box.insert(tk.END, repr(o))

# ================ MAIN ===================
root = tk.Tk()
App(root)
root.mainloop()
