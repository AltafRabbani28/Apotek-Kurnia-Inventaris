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
        
