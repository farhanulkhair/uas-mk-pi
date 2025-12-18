# 🐾 Penelusuran Artikel Hewan

Aplikasi web modern untuk mencari artikel tentang perawatan hewan menggunakan algoritma Machine Learning (Cosine Similarity & Jaccard Similarity).

## ✨ Fitur

- 🔍 Pencarian artikel dengan dua algoritma: Cosine Similarity & Jaccard Similarity
- 🎨 Desain modern dengan efek Glassmorphism
- 📊 Menampilkan skor relevansi untuk setiap hasil
- 🖼️ Background dinamis (berbeda untuk halaman search dan results)
- ⚡ Cepat dan efisien dengan caching

## 🚀 Cara Menjalankan Lokal

### Prasyarat

- Python 3.8 atau lebih baru
- pip

### Instalasi

1. Clone repository ini:

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

2. Buat virtual environment (opsional tapi direkomendasikan):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:

```bash
streamlit run app.py
```

5. Buka browser dan akses: `http://localhost:8501`

## 🌐 Deploy ke Streamlit Cloud

### Langkah-langkah Deploy:

1. **Push ke GitHub**

   - Upload semua file project ke GitHub repository
   - Pastikan file berikut ada:
     - `app.py`
     - `requirements.txt`
     - `cleaned_hewania_articles_tokenized.csv`
     - `stopword.txt`
     - `templates/assets/` (background & logo)
     - `.streamlit/config.toml`

2. **Deploy di Streamlit Cloud**

   - Kunjungi [share.streamlit.io](https://share.streamlit.io)
   - Login dengan akun GitHub
   - Klik "New app"
   - Pilih repository, branch, dan file `app.py`
   - Klik "Deploy"

3. **Selesai!**
   - App akan otomatis deploy dalam beberapa menit
   - Dapatkan URL public yang bisa dibagikan

## 📁 Struktur File

```
Project UAS/
├── app.py                                        # Aplikasi Streamlit utama
├── requirements.txt                              # Dependencies
├── cleaned_hewania_articles_tokenized.csv        # Dataset artikel
├── stopword.txt                                  # Stopwords bahasa Indonesia
├── templates/
│   └── assets/
│       ├── background.jpg                        # Background halaman search
│       ├── background2.jpg                       # Background halaman results
│       └── logo.png                              # Logo aplikasi
├── .streamlit/
│   └── config.toml                               # Konfigurasi Streamlit
└── README.md                                     # Dokumentasi
```

## 🎨 Teknologi yang Digunakan

- **Streamlit** - Framework web app
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine Learning (TF-IDF, Cosine Similarity)
- **Sastrawi** - Indonesian text processing & stemming

## 📝 Catatan

- Dataset berisi artikel dari website Hewania tentang perawatan hewan
- Aplikasi menggunakan preprocessing text (lowercase, remove punctuation, stopword removal, stemming)
- Hasil pencarian diurutkan berdasarkan skor relevansi tertinggi

## 👨‍💻 Developer

Dibuat untuk Project UAS Mata Kuliah Penulusuran Informasi

---

💜 Dibuat dengan Streamlit & Penulusuran Informasi
