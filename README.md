# ♻️ EcoScan
EcoScan adalah aplikasi berbasis web yang memanfaatkan Artificial Intelligence (AI) untuk mengidentifikasi jenis sampah melalui gambar serta memberikan rekomendasi pengelolaan berdasarkan konsep **Reduce, Reuse, dan Recycle (3R)**. Proyek ini dikembangkan untuk membantu meningkatkan kesadaran masyarakat terhadap pengelolaan sampah yang lebih efektif dan berkelanjutan.

---

## 🎯 Objectives
* Mengidentifikasi jenis sampah secara otomatis menggunakan AI.
* Memberikan rekomendasi pengelolaan berbasis konsep 3R.
* Meningkatkan kesadaran masyarakat terhadap pengelolaan sampah.
* Menyediakan dashboard visualisasi data hasil klasifikasi.

---

## ✨ Features
* 🤖 AI Waste Classification
* ♻️ 3R Recommendation System
* 📊 Interactive Dashboard
* 🌐 Web-Based Application
* 📷 Image Upload Prediction

EcoScan mengintegrasikan Artificial Intelligence, Data Science, dan Full Stack Development untuk menyediakan platform klasifikasi dan pengelolaan sampah secara end-to-end.

---

## 🧠 AI Model
| Detail              | Information               |
| ------------------- | ------------------------- |
| Architecture        | Custom Wide ResNet CNN    |
| Validation Accuracy | 85.16%                    |
| Number of Classes   | 7 Categories              |
| Input Size          | 224 × 224 RGB             |
| Model Format        | Keras SavedModel (.keras) |

### Waste Categories
* Kaca
* Kardus
* Kertas
* Logam
* Organik
* Plastik
* Residu

---

## 📊 Data Science Process
* Data Gathering
* Data Assessing
* Data Cleaning
* Exploratory Data Analysis (EDA)
* Mapping 3R
* Data Preparation
* Model Development
* Data Visualization

---

## 🛠️ Tech Stack
### Artificial Intelligence
* Python
* TensorFlow
* Keras
* FastAPI
### Data Science
* Pandas
* NumPy
* Matplotlib
### Full Stack Development
* HTML
* CSS
* JavaScript

---

## 📂 Repository Structure
```bash
EcoScan/
│
├── Artificial Intelligence/
│   ├── Model Training
│   ├── Inference API
│   └── Saved Model
│
├── Data Science/
│   ├── Data Gathering
│   ├── Data Cleaning
│   ├── EDA
│   ├── Visualization
│   └── 3R Mapping
│
├── FullStack/
│   ├── Frontend
│   ├── Backend Integration
│   └── Dashboard
│
└── README.md
```

---

## 🚀 Installation
### Clone Repository
```bash
git clone https://github.com/BayuHamzah19/ecoscan-backend-CC26-PSU289.git
```

### Masuk ke Folder Project
```bash
cd ecoscan-backend-CC26-PSU289
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Jalankan API
```bash
uvicorn app:app --reload
```
atau
```bash
python app.py
```

### Akses API
```bash
http://localhost:8000
```

---

## 🔄 System Workflow

1. User mengunggah gambar sampah.
2. Sistem mengirim gambar ke API.
3. Model AI melakukan klasifikasi jenis sampah.
4. Sistem menampilkan hasil prediksi.
5. Sistem memberikan rekomendasi pengelolaan berdasarkan konsep 3R.
6. Hasil klasifikasi ditampilkan pada dashboard.

---

## 👥 Team Members
### Artificial Intelligence Engineer
* Mohammad Bayu Hamzah Nasikhin
* Maulana Hidayah Syaif Ali Khan
### Data Scientist
* Silvia Nur Diahsari
* Sinara Meyda Setio Putri
### Full Stack Web Developer
* Muhammad Shodiq Shirath
* Rahmania Farasya

---

## 📌 Project Information
**Capstone Project**
Coding Camp 2026 powered by DBS Foundation
**Theme:** Sustainable Living & Responsible Consumption

---

## 📄 License
This project was developed for educational purposes as part of the Coding Camp 2026 powered by DBS Foundation.

---

### ♻️ EcoScan
### AI-Powered Waste Classification and 3R Recommendation Platform
