import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

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
        self.pq = []
        self.tree = None

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
        
