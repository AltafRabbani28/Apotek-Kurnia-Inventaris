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
        self.head = None       
        self.hash = {}        
        self.queue = []       

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

        tk.Button(kiri, text="Tambah", bg="#007bff", fg="white",
                  width=12, command=self.tambah).grid(row=4, column=0, pady=4)

        tk.Button(kiri, text="Ubah", bg="#28a745", fg="white",
                  width=12, command=self.ubah).grid(row=4, column=1, pady=4)

        tk.Button(kiri, text="Hapus", bg="#dc3545", fg="white",
                  width=12, command=self.hapus).grid(row=4, column=2, pady=4)

        ttk.Separator(kiri).grid(row=5, column=0, columnspan=3, pady=15, sticky="ew")


        self.field(kiri, "Beli (Nama)", "beli_nama", 6)
        self.field(kiri, "Jumlah", "beli_jumlah", 7)

        tk.Button(kiri, text="Beli", bg="#ffc107", fg="black",
                  width=26, command=self.beli).grid(row=8, column=0, columnspan=3, pady=6)


    
        ttk.Label(kanan, text="📦 Daftar Obat", font=("Arial", 14, "bold")).pack()
        self.listbox = tk.Listbox(kanan, width=60, height=25, font=("Consolas", 11))
        self.listbox.pack(pady=10)


    def field(self, parent, label, name, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, pady=3, sticky="w")
        entry = ttk.Entry(parent, width=25)
        entry.grid(row=row, column=1)
        setattr(self, name, entry)


    def tambah(self):
        try:
            harga = int(self.harga.get())
            stok = int(self.stok.get())
        except:
            return messagebox.showerror("Err", "Harga/Stok harus angka!")

        if self.inv.tambah(self.nama.get(), harga, stok, self.exp.get()):
            messagebox.showinfo("OK", "Obat ditambahkan")
        else:
            messagebox.showerror("Err", "Nama sudah ada")
        self.refresh()

    def ubah(self):
        try:
            harga = int(self.harga.get())
            stok = int(self.stok.get())
        except:
            return messagebox.showerror("Err", "Harga/Stok harus angka!")

        if self.inv.ubah(self.nama.get(), harga, stok, self.exp.get()):
            messagebox.showinfo("OK", "Obat diperbarui")
        else:
            messagebox.showerror("Err", "Obat tidak ditemukan")
        self.refresh()

    def hapus(self):
        if self.inv.hapus(self.nama.get()):
            messagebox.showinfo("OK", "Obat dihapus")
        else:
            messagebox.showerror("Err", "Obat tidak ditemukan")
        self.refresh()

    def beli(self):
        try:
            jumlah = int(self.beli_jumlah.get())
        except:
            return messagebox.showerror("Err", "Jumlah harus angka!")

        res = self.inv.beli(self.beli_nama.get(), jumlah)

        if res is None:
            return messagebox.showerror("Err", "Obat tidak ditemukan")
        if res is False:
            return messagebox.showerror("Err", "Stok tidak cukup")
        if res == "exp":
            return messagebox.showerror("Err", "Obat kadaluarsa")
        if res == "format":
            return messagebox.showerror("Err", "Format tanggal salah")

        messagebox.showinfo("OK", "Pembelian berhasil")
        self.refresh()

    def cari(self):
        o = self.inv.cari(self.cari_nama.get())
        messagebox.showinfo("Hasil", repr(o) if o else "Tidak ditemukan")

    def urut_nama(self):
        arr = self.inv.sort_nama()
        self.listbox.delete(0, tk.END)
        for o in arr:
            self.listbox.insert(tk.END, repr(o))

    def refresh(self):
        self.listbox.delete(0, tk.END)
        for o in self.inv.semua():
            self.listbox.insert(tk.END, repr(o))

if __name__ == "__main__":
    root = tk.Tk()
    Aplikasi(root)
    root.mainloop()
