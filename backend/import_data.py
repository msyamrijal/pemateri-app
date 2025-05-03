import csv
from app import app, db, Pemateri

def import_data():
    with app.app_context():
        with open('data_pemateri.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Ubah format tanggal (hilangkan waktu)
                tanggal = row['Tanggal'].split()[0]  # Ambil hanya tanggal (YYYY-MM-DD)
                peserta = row['Peserta']

                # Simpan ke database
                pemateri = Pemateri(
                    institusi=row['Institusi'],
                    mata_pelajaran=row['Mata_Pelajaran'],
                    tanggal=tanggal,
                    peserta=peserta
                )
                db.session.add(pemateri)
            db.session.commit()
        print("Data berhasil diimport!")

if __name__ == '__main__':
    import_data()