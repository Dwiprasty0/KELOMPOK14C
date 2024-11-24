import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# File CSV untuk menyimpan data
CSV_FILE = "donasi.csv"

# Fungsi untuk memastikan file CSV ada dengan header
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Kategori", "Jenis Barang", "Kondisi Barang", "Lokasi Penyimpanan", "Nama Donatur", "Status Distribusi"])

# Fungsi untuk men-generate ID barang
def generate_id(category):
    prefix = {
        "Pakaian": "PK",
        "Makanan": "MK",
        "Elektronik": "EL",
        "Alat Tulis": "AT",
    }
    existing_data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            existing_data = [row for row in reader if row["Kategori"] == category]
    return f"{prefix.get(category, 'XX')}{len(existing_data) + 1:03}"

# Fungsi untuk menambah data barang
def add_data():
    kategori = kategori_var.get()
    jenis_barang = jenis_barang_entry.get()
    kondisi_barang = kondisi_barang_var.get()
    lokasi_penyimpanan = lokasi_penyimpanan_var.get()
    nama_donatur = nama_donatur_entry.get()
    status_distribusi = status_distribusi_var.get()

    if not (kategori and jenis_barang and kondisi_barang and lokasi_penyimpanan and nama_donatur):
        messagebox.showwarning("Input Error", "Harap isi semua field dengan benar!")
        return

    id_barang = generate_id(kategori)

    # Simpan data ke file CSV
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([id_barang, kategori, jenis_barang, kondisi_barang, lokasi_penyimpanan, nama_donatur, status_distribusi])

    messagebox.showinfo("Sukses", f"Barang berhasil ditambahkan dengan ID: {id_barang}")
    clear_inputs()

# Fungsi untuk membersihkan input
def clear_inputs():
    kategori_var.set("")
    jenis_barang_entry.delete(0, tk.END)
    kondisi_barang_var.set("")
    lokasi_penyimpanan_var.set("")
    nama_donatur_entry.delete(0, tk.END)
    status_distribusi_var.set("")

# Fungsi untuk menampilkan data
def view_data():
    category = filter_category_var.get()

    for row in tree.get_children():
        tree.delete(row)

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r") as file:
            reader = csv.DictReader(file)
            for item in reader:
                if not category or item["Kategori"] == category:
                    tree.insert("", tk.END, values=(item["ID"], item["Kategori"], item["Jenis Barang"], item["Kondisi Barang"], item["Lokasi Penyimpanan"], item["Nama Donatur"], item["Status Distribusi"]))

# Fungsi untuk mengedit data berdasarkan ID
def edit_data():
    item_id = edit_id_entry.get()
    new_status = edit_status_var.get()

    if not os.path.exists(CSV_FILE):
        messagebox.showwarning("Error", "Data belum ada!")
        return

    updated = False
    data = []

    with open(CSV_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == item_id:
                row["Status Distribusi"] = new_status
                updated = True
            data.append(row)

    if updated:
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["ID", "Kategori", "Jenis Barang", "Kondisi Barang", "Lokasi Penyimpanan", "Nama Donatur", "Status Distribusi"])
            writer.writeheader()
            writer.writerows(data)
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        edit_id_entry.delete(0, tk.END)
        edit_status_var.set("")
    else:
        messagebox.showwarning("Error", "ID Barang tidak ditemukan!")

# GUI Main Window
root = tk.Tk()
root.title("Sistem Pengelolaan Barang Donasi")
root.geometry("800x600")

# Tab Control
notebook = ttk.Notebook(root)

# Tab Input Data
input_tab = ttk.Frame(notebook)
notebook.add(input_tab, text="Input Data")

# Tab View Data
view_tab = ttk.Frame(notebook)
notebook.add(view_tab, text="Lihat Data")

# Tab Edit Data
edit_tab = ttk.Frame(notebook)
notebook.add(edit_tab, text="Edit Data")

notebook.pack(expand=True, fill="both")

# Input Data Form
kategori_var = tk.StringVar()
kondisi_barang_var = tk.StringVar()
lokasi_penyimpanan_var = tk.StringVar()
status_distribusi_var = tk.StringVar()

tk.Label(input_tab, text="Kategori:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
kategori_combo = ttk.Combobox(input_tab, textvariable=kategori_var, values=["Pakaian", "Makanan", "Elektronik", "Alat Tulis"])
kategori_combo.grid(row=0, column=1, pady=5, padx=5)

jenis_barang_entry = ttk.Entry(input_tab)
tk.Label(input_tab, text="Jenis Barang:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
jenis_barang_entry.grid(row=1, column=1, pady=5, padx=5)

tk.Label(input_tab, text="Kondisi Barang:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
kondisi_combo = ttk.Combobox(input_tab, textvariable=kondisi_barang_var, values=["Baru", "Bekas", "Layak Pakai"])
kondisi_combo.grid(row=2, column=1, pady=5, padx=5)

tk.Label(input_tab, text="Lokasi Penyimpanan:").grid(row=3, column=0, pady=5, padx=5, sticky="w")
lokasi_combo = ttk.Combobox(input_tab, textvariable=lokasi_penyimpanan_var, values=["Gudang A", "Gudang B"])
lokasi_combo.grid(row=3, column=1, pady=5, padx=5)

nama_donatur_entry = ttk.Entry(input_tab)
tk.Label(input_tab, text="Nama Donatur:").grid(row=4, column=0, pady=5, padx=5, sticky="w")
nama_donatur_entry.grid(row=4, column=1, pady=5, padx=5)

tk.Label(input_tab, text="Status Distribusi:").grid(row=5, column=0, pady=5, padx=5, sticky="w")
status_combo = ttk.Combobox(input_tab, textvariable=status_distribusi_var, values=["Tersedia", "Disalurkan"])
status_combo.grid(row=5, column=1, pady=5, padx=5)

tk.Button(input_tab, text="Tambah Barang", command=add_data).grid(row=6, column=0, columnspan=2, pady=10)

# View Data Section
filter_category_var = tk.StringVar()

tk.Label(view_tab, text="Filter Kategori:").pack(pady=5)
filter_category_combo = ttk.Combobox(view_tab, textvariable=filter_category_var, values=["", "Pakaian", "Makanan", "Elektronik", "Alat Tulis"])
filter_category_combo.pack(pady=5)

tree = ttk.Treeview(view_tab, columns=("ID", "Kategori", "Jenis Barang", "Kondisi Barang", "Lokasi Penyimpanan", "Nama Donatur", "Status Distribusi"), show="headings")
for col in ["ID", "Kategori", "Jenis Barang", "Kondisi Barang", "Lokasi Penyimpanan", "Nama Donatur", "Status Distribusi"]:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(expand=True, fill="both", pady=10)

tk.Button(view_tab, text="Tampilkan Data", command=view_data).pack(pady=5)

# Edit Data Section
edit_id_entry = ttk.Entry(edit_tab)
edit_status_var = tk.StringVar()

tk.Label(edit_tab, text="ID Barang:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
edit_id_entry.grid(row=0, column=1, pady=5, padx=5)

tk.Label(edit_tab, text="Status Baru:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
edit_status_combo = ttk.Combobox(edit_tab, textvariable=edit_status_var, values=["Tersedia", "Disalurkan"])
edit_status_combo.grid(row=1, column=1, pady=5, padx=5)

tk.Button(edit_tab, text="Edit Data", command=edit_data).grid(row=2, column=0, columnspan=2, pady=10)

# Inisialisasi CSV
initialize_csv()

root.mainloop()
