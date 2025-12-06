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

2.     def insert_tree(self, node, key, data):
        if not node: return Node(key, data)
        if key < node.key:
            node.left = self.insert_tree(node.left, key, data)
        else:
            node.right = self.insert_tree(node.right, key, data)
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

    def cari(self, n):
        return self.hash.get(n)

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
        if datetime.strptime(o.exp, "%Y-%m-%d") < datetime.today():
            return "exp"
        o.stok -= j
        return True

    def sort_nama(self):
        a = self.arr[:]
        for i in range(len(a) - 1):
            for j in range(len(a) - i - 1):
                if a[j].nama > a[j + 1].nama:
                    a[j], a[j + 1] = a[j + 1], a[j]
        return a
        
