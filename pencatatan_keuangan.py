#!/usr/bin/env python3
"""Aplikasi pencatatan keuangan sederhana tanpa dependensi eksternal."""

import csv
import os
from datetime import datetime

DATA_FILE = "transaksi.csv"


def tambah_transaksi(keterangan: str, jumlah: float) -> None:
    """Simpan transaksi ke dalam berkas CSV."""
    file_baru = not os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if file_baru:
            writer.writerow(["tanggal", "keterangan", "jumlah"])
        writer.writerow([datetime.now().isoformat(), keterangan, f"{jumlah:.2f}"])


def tampilkan_transaksi() -> None:
    """Tampilkan seluruh transaksi dan total."""
    if not os.path.exists(DATA_FILE):
        print("Belum ada transaksi.")
        return
    total = 0.0
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("\nDaftar Transaksi:")
        for row in reader:
            print(f"{row['tanggal']} - {row['keterangan']} : {row['jumlah']}")
            try:
                total += float(row["jumlah"])
            except ValueError:
                pass
    print(f"Total: {total:.2f}\n")


def main() -> None:
    while True:
        print("=== Pencatatan Keuangan ===")
        print("1. Tambah transaksi")
        print("2. Tampilkan transaksi")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            ket = input("Keterangan: ")
            while True:
                try:
                    jumlah = float(input("Jumlah: "))
                    break
                except ValueError:
                    print("Masukkan angka yang benar.")
            tambah_transaksi(ket, jumlah)
            print("Transaksi tersimpan.\n")
        elif pilihan == "2":
            tampilkan_transaksi()
        elif pilihan == "3":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.\n")


if __name__ == "__main__":
    main()
