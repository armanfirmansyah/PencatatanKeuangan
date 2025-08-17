import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / 'transactions.json'


def load_transactions():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return []


def save_transactions(transactions):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, ensure_ascii=False, indent=2)


def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_nominal(nominal_str):
    try:
        float(nominal_str)
        return True
    except ValueError:
        return False


def add_transaction():
    date_str = input('Tanggal (YYYY-MM-DD): ')
    if not validate_date(date_str):
        print('Format tanggal salah.')
        return
    description = input('Deskripsi: ')
    nominal_str = input('Nominal: ')
    if not validate_nominal(nominal_str):
        print('Nominal harus numerik.')
        return
    trans_type = input('Tipe (masuk/keluar): ').lower()
    if trans_type not in {'masuk', 'keluar'}:
        print("Tipe harus 'masuk' atau 'keluar'.")
        return
    transaction = {
        'tanggal': date_str,
        'deskripsi': description,
        'nominal': float(nominal_str),
        'tipe': trans_type,
    }
    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)
    print('Transaksi berhasil ditambahkan.')


def show_totals():
    transactions = load_transactions()
    total_in = sum(t['nominal'] for t in transactions if t['tipe'] == 'masuk')
    total_out = sum(t['nominal'] for t in transactions if t['tipe'] == 'keluar')
    print(f'Total pemasukan: {total_in}')
    print(f'Total pengeluaran: {total_out}')


def filter_by_date():
    start = input('Tanggal mulai (YYYY-MM-DD): ')
    if not validate_date(start):
        print('Format tanggal mulai salah.')
        return
    end = input('Tanggal akhir (YYYY-MM-DD): ')
    if not validate_date(end):
        print('Format tanggal akhir salah.')
        return
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')
    transactions = load_transactions()
    filtered = [t for t in transactions if start_dt <= datetime.strptime(t['tanggal'], '%Y-%m-%d') <= end_dt]
    if not filtered:
        print('Tidak ada transaksi dalam rentang tersebut.')
        return
    for t in filtered:
        print(f"{t['tanggal']} - {t['deskripsi']} - {t['tipe']} - {t['nominal']}")


def main():
    while True:
        print('\nMenu:')
        print('1. Tambah transaksi')
        print('2. Menampilkan total pemasukan/pengeluaran')
        print('3. Memfilter transaksi berdasarkan rentang tanggal')
        print('4. Keluar')
        choice = input('Pilih menu: ')
        if choice == '1':
            add_transaction()
        elif choice == '2':
            show_totals()
        elif choice == '3':
            filter_by_date()
        elif choice == '4':
            break
        else:
            print('Menu tidak valid.')


if __name__ == '__main__':
    main()
