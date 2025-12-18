# 🚀 Panduan Deploy ke Streamlit Cloud

Panduan lengkap untuk mempublish aplikasi Anda ke Streamlit Cloud secara GRATIS!

## 📋 Persiapan

### File yang Dibutuhkan:
✅ `streamlit_app.py` - Aplikasi utama  
✅ `requirements.txt` - Dependencies  
✅ `cleaned_hewania_articles_tokenized.csv` - Dataset  
✅ `stopword.txt` - Stopwords  
✅ `.streamlit/config.toml` - Konfigurasi (opsional)  

## 🌐 Langkah-langkah Deploy

### 1️⃣ Persiapkan GitHub Repository

**Jika belum punya repository:**

1. Buka [GitHub.com](https://github.com) dan login
2. Klik tombol **"New"** atau **"+"** → **"New repository"**
3. Beri nama, misal: `animal-article-search`
4. Set ke **Public** (wajib untuk Streamlit Cloud gratis)
5. Klik **"Create repository"**

**Upload file ke GitHub:**

Menggunakan GitHub Web:
- Klik **"Add file"** → **"Upload files"**
- Drag & drop semua file yang dibutuhkan
- Commit changes

Atau menggunakan Git Command:
```bash
git init
git add streamlit_app.py requirements.txt cleaned_hewania_articles_tokenized.csv stopword.txt .streamlit/
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main
```

### 2️⃣ Deploy di Streamlit Cloud

1. **Kunjungi Streamlit Cloud**
   - Buka [share.streamlit.io](https://share.streamlit.io)
   - Klik **"Sign in"** dengan akun GitHub

2. **Deploy App Baru**
   - Klik **"New app"** di dashboard
   - Atau langsung ke: [share.streamlit.io/deploy](https://share.streamlit.io/deploy)

3. **Isi Form Deploy:**
   - **Repository:** Pilih `USERNAME/animal-article-search`
   - **Branch:** `main` (atau `master`)
   - **Main file path:** `streamlit_app.py`
   - **App URL (optional):** Bisa custom atau biarkan default

4. **Advanced Settings (Optional)**
   - Python version: 3.9 atau lebih tinggi
   - Biarkan default jika tidak perlu custom

5. **Klik "Deploy!"**
   - Tunggu 2-5 menit proses deployment
   - App akan otomatis install dependencies dari `requirements.txt`

### 3️⃣ Selesai! 🎉

- App Anda sekarang live dan bisa diakses siapa saja
- URL akan berbentuk: `https://APPNAME-USERNAME.streamlit.app`
- Share URL ini ke siapa saja!

## 🔄 Update Aplikasi

Jika ingin update aplikasi:

1. Edit file di repository GitHub
2. Commit & push changes
3. Streamlit Cloud akan **otomatis re-deploy** dalam beberapa menit

Atau manual reboot:
- Buka dashboard Streamlit Cloud
- Klik menu (⋮) pada app Anda
- Pilih **"Reboot app"**

## ⚙️ Troubleshooting

### ❌ Error saat Deploy

**"Requirements installation failed"**
- Pastikan `requirements.txt` format benar
- Cek versi package compatibility

**"File not found: cleaned_hewania_articles_tokenized.csv"**
- Pastikan file CSV sudah di-upload ke GitHub
- Cek nama file (case-sensitive!)

**"Module not found"**
- Tambahkan missing module ke `requirements.txt`
- Push changes ke GitHub

### 🐌 App Lambat / Sleep

App gratis Streamlit Cloud akan "sleep" jika tidak diakses beberapa hari:
- Akses ulang URL → app akan wake up otomatis (30-60 detik)
- Tidak ada data yang hilang

### 📊 Resource Limits (Free Tier)

- **CPU:** 1 core
- **RAM:** 1 GB
- **Storage:** 100 MB (untuk repo files)
- **Bandwidth:** Unlimited
- **Apps:** 1 app public (unlimited private dengan Teams)

Tips optimasi:
- Gunakan `@st.cache_data` untuk cache data besar
- Gunakan `@st.cache_resource` untuk model/stemmer
- Compress/optimize dataset jika terlalu besar

## 🎓 Tips Pro

1. **Custom Domain (Optional)**
   - Bisa setup custom domain di settings
   - Butuh upgrade ke Streamlit Cloud Teams

2. **Environment Variables**
   - Untuk API keys atau secrets
   - Gunakan Streamlit Secrets Management
   - Buat file `.streamlit/secrets.toml` (local only, jangan push!)

3. **Analytics**
   - Lihat visitor stats di dashboard
   - Monitor performance & errors

4. **Backup**
   - Selalu simpan backup code di local
   - GitHub = backup otomatis

## 📞 Butuh Bantuan?

- 📚 [Streamlit Docs](https://docs.streamlit.io)
- 💬 [Streamlit Forum](https://discuss.streamlit.io)
- 🐛 [GitHub Issues](https://github.com/streamlit/streamlit/issues)

---

**Selamat! Aplikasi Anda sekarang online dan bisa diakses siapa saja! 🎊**

