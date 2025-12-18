@echo off
echo ========================================
echo   Starting Aplikasi Pencarian Artikel Hewan
echo ========================================
echo.
echo Mengaktifkan virtual environment...
call envUAS\Scripts\activate.bat

echo.
echo Menjalankan Streamlit...
echo.
echo Browser akan terbuka otomatis di: http://localhost:8501
echo Tekan Ctrl+C untuk menghentikan aplikasi
echo.

streamlit run streamlit_app.py

pause

