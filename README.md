
# Brankas Pribadi (Django)
## Cara Menjalankan Aplikasi
1) Masuk ke folder project
Buka terminal pada folder yang berisi file `manage.py`.
2) Buat & aktifkan Virtual Environment
**Windows**
python -m venv .venv
.venv\Scripts\activate
**Linux / Mac**
python -m venv .venv
source .venv/bin/activate
3) Install dependensi
python -m pip install -r requirements.txt
4) Buat file .env
Buat file bernama .env di root project (selevel manage.py), contoh isi:
DJANGO_SECRET_KEY=isi_dengan_secret_key_random
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
5) Siapkan database (migrations)
python manage.py makemigrations
python manage.py migrate
6) Jalankan server
python manage.py runserver
7) Akses aplikasi di browser
Login: http://127.0.0.1:8000/login/
---
## Fitur Utama
* Login & Register: Sistem pendaftaran dan masuk akun pengguna.
* Dashboard: Halaman khusus menampilkan daftar file milik pengguna sendiri.
* Upload: Unggah file dokumen atau gambar ke server.
* Download: Unduh file yang sudah disimpan sebelumnya.
* Delete: Menghapus file secara permanen dengan konfirmasi password.
---
## Aspek Keamanan (Security)
Aplikasi ini sudah menerapkan standar keamanan sebagai berikut:
1. Anti-Hack Nama File (UUID)
   Nama file yang diupload otomatis diubah menjadi kode acak oleh sistem.
   Tujuannya: Mencegah hacker menimpa file sistem atau menyisipkan script berbahaya (webshell).
2. Validasi File Ketat
   Sistem hanya menerima file dokumen/gambar dan membatasi ukuran maksimal 5MB.
   Tujuannya: Mencegah upload virus dan mencegah server penuh (Denial of Service).
3. Anti-Brute Force
   Jika gagal login 5 kali berturut-turut, akun akan terkunci otomatis selama 15 menit.
   Tujuannya: Mencegah penebakan password secara paksa menggunakan software otomatis.
4. Privasi Data (Anti-IDOR)
   Pengguna hanya diizinkan melihat, mengunduh, dan menghapus file miliknya sendiri.
   Tujuannya: Mencegah pengguna A mengakses data rahasia milik pengguna B.
5. Konfirmasi Hapus (Sudo Mode)
   Pengguna wajib memasukkan password akun saat ingin menghapus file.
   Tujuannya: Mencegah penghapusan data secara tidak sengaja atau jika sesi browser dibajak.
6. Keamanan Sesi (Anti-Back Button)
   Setelah logout, tombol "Back" pada browser tidak akan menampilkan halaman dashboard lagi.
   Tujuannya: Menjaga kerahasiaan data jika komputer digunakan secara bergantian.


