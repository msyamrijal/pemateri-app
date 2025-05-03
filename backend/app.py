from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__,
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pemateri.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # Enable CORS

# Inisialisasi database
db = SQLAlchemy(app)

# Model Database
class Pemateri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institusi = db.Column(db.String(50), nullable=False)
    mata_pelajaran = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.String(20), nullable=False)
    peserta = db.Column(db.String(200), nullable=False)

# Buat tabel database
with app.app_context():
    db.create_all()
    print("Database initialized!")

# ================= ROUTES =================

@app.route('/')
def home():
    """Render halaman utama"""
    return render_template('index.html')

# Get all data
@app.route('/api/pemateri', methods=['GET'])
def get_all_pemateri():
    pemateri = Pemateri.query.all()
    return jsonify([{
        'id': p.id,
        'institusi': p.institusi,
        'mata_pelajaran': p.mata_pelajaran,
        'tanggal': p.tanggal,
        'peserta': p.peserta
    } for p in pemateri])

# Add new data
@app.route('/api/pemateri', methods=['POST'])
def add_pemateri():
    data = request.get_json()
    
    if not all(key in data for key in ['institusi', 'mata_pelajaran', 'tanggal', 'peserta']):
        return jsonify({'error': 'Data tidak lengkap!'}), 400
    
    new_entry = Pemateri(
        institusi=data['institusi'],
        mata_pelajaran=data['mata_pelajaran'],
        tanggal=data['tanggal'],
        peserta=data['peserta']
    )
    
    db.session.add(new_entry)
    db.session.commit()
    
    return jsonify({'message': 'Data berhasil ditambahkan!', 'id': new_entry.id}), 201

# Delete data
@app.route('/api/pemateri/<int:id>', methods=['DELETE'])
def delete_pemateri(id):
    pemateri = Pemateri.query.get_or_404(id)
    db.session.delete(pemateri)
    db.session.commit()
    return jsonify({'message': 'Data berhasil dihapus!'})

# ================= CONFIGURASI PRODUKSI =================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)