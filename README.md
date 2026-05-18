# ♻️ EcoScan AI - Trash Classification API

EcoScan AI adalah aplikasi API berbasis **FastAPI** yang digunakan untuk mendeteksi dan mengklasifikasikan jenis sampah secara otomatis menggunakan teknologi *Deep Learning*. API ini dirancang untuk diintegrasikan dengan aplikasi mobile atau frontend lainnya.

## 🧠 Detail Model
- **Arsitektur**: Custom Wide ResNet CNN
- **Akurasi Validasi**: 85.16%
- **Format Model**: Keras v3 SavedModel (`.keras`)
- **Input Ukuran Gambar**: 224 x 224 piksel (RGB)

## 📁 Daftar Kelas Sampah (7 Kelas)
Model ini dapat mengenali 7 kategori sampah berikut (berurutan secara alfabetis):
1. `Kaca`
2. `Kardus`
3. `Kertas`
4. `Logam`
5. `Organik`
6. `Plastik`
7. `Residu`

## 🛠️ Cara Menjalankan API di Lokal

### 1. Install Dependensi
Pastikan Anda sudah menginstal Python (disarankan versi 3.10 ke atas), lalu jalankan perintah:
```bash
pip install -r requirements.txt