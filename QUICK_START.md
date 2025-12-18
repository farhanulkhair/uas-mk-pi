# ⚡ Quick Start Guide

Panduan cepat untuk menjalankan aplikasi dalam 2 menit!

## 🖥️ Jalankan di Komputer Lokal

### Windows:
Klik dua kali file:
```
run_app.bat
```

### Mac/Linux:
Jalankan di terminal:
```bash
chmod +x run_app.sh
./run_app.sh
```

### Manual:
```bash
# Aktifkan virtual environment
envUAS\Scripts\activate    # Windows
source envUAS/bin/activate # Mac/Linux

# Jalankan aplikasi
streamlit run streamlit_app.py
```

Aplikasi akan terbuka otomatis di browser: `http://localhost:8501`

---

## 🌐 Publish Online (GRATIS)

### Langkah 1: Upload ke GitHub
1. Buat repository baru di [GitHub.com](https://github.com/new)
2. Upload file berikut:
   - `streamlit_app.py`
   - `requirements.txt`
   - `cleaned_hewania_articles_tokenized.csv`
   - `stopword.txt`
   - `.streamlit/` folder

### Langkah 2: Deploy di Streamlit Cloud
1. Kunjungi [share.streamlit.io](https://share.streamlit.io)
2. Login dengan GitHub
3. Klik **"New app"**
4. Pilih repository dan file `streamlit_app.py`
5. Klik **"Deploy"**

### Selesai! 🎉
Aplikasi Anda sekarang online dan bisa diakses siapa saja!

---

## 🎨 Preview Fitur

### 1. Pencarian Cerdas
- Ketik kata kunci (contoh: "kucing", "vaksin anjing")
- Pilih algoritma: Cosine atau Jaccard Similarity
- Klik tombol Cari

### 2. Hasil Relevan
- Artikel diurutkan berdasarkan skor relevansi
- Tampil dengan gambar dan preview konten
- Klik artikel untuk baca selengkapnya

### 3. Navigasi Mudah
- Pagination untuk hasil banyak
- Tombol Previous/Next
- Info halaman saat ini

---

## 💡 Tips Penggunaan

### Kata Kunci Efektif:
✅ "cara merawat kucing"  
✅ "vaksin anjing"  
✅ "makanan hamster"  
✅ "penyakit ikan koi"  

### Perbandingan Algoritma:

**Cosine Similarity:**
- Lebih bagus untuk pencarian umum
- Mempertimbangkan frekuensi kata
- Hasil lebih bervariasi

**Jaccard Similarity:**
- Lebih strict/ketat
- Fokus pada kata yang sama persis
- Hasil lebih spesifik

---

## 🆘 Troubleshooting

### ❌ "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### ❌ "FileNotFoundError: stopword.txt"
Pastikan file `stopword.txt` ada di folder yang sama dengan `streamlit_app.py`

### ❌ "Port already in use"
```bash
streamlit run streamlit_app.py --server.port 8502
```

### ❌ App lambat
- Tunggu cache loading pertama kali
- Selanjutnya akan cepat

---

## 📱 Screenshots

### Halaman Utama
- Search box dengan animasi
- Pilihan algoritma
- Background gradient indah

### Hasil Pencarian
- Card artikel dengan gambar
- Skor relevansi
- Link ke artikel asli
- Pagination

---

## 🚀 Selamat Mencoba!

Pertanyaan? Lihat:
- 📖 [README.md](README.md) - Dokumentasi lengkap
- 🌐 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Panduan deploy detail
- 🔄 [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md) - Perubahan dari Flask

**Happy Searching! 🐾✨**

