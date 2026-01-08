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
Aplikasi ini telah menerapkan 8 standar keamanan wajib untuk memitigasi risiko serangan web umum:
1. Proteksi Brute Force (Account Lockout)
Sistem menerapkan mekanisme Rate Limiting pada halaman login.
Mekanisme: Jika pengguna gagal login 5 kali berturut-turut, akun akan terkunci otomatis selama 15 menit.
Tujuan: Mencegah peretas menebak password secara paksa menggunakan software otomatis.

2. Sanitasi File & Anti-Webshell (UUID)
Mencegah celah keamanan pada fitur upload file.
Anti-Hack Renaming: Nama file yang diupload otomatis diubah menjadi kode acak (UUID4) oleh sistem.
Validasi Ketat: Sistem menolak file selain dokumen/gambar dan membatasi ukuran maksimal 5MB.
Tujuan: Mencegah hacker menimpa file sistem (Overwriting), menyisipkan script berbahaya (Webshell), atau melumpuhkan server (DoS).

3. Privasi Data (Anti-IDOR)
Mencegah serangan Insecure Direct Object References.
Mekanisme: Validasi kepemilikan dilakukan di backend. Pengguna hanya diizinkan melihat, mengunduh, dan menghapus file miliknya sendiri.
Tujuan: Mencegah Pengguna A mengakses data rahasia milik Pengguna B meskipun mengetahui URL/ID file tersebut.

4. Manajemen Rahasia (No Hardcoded Secrets)
Pemisahan konfigurasi sensitif dari kode program.
Mekanisme: Secret Key dan pengaturan Debug disimpan dalam file .env yang tidak diikutsertakan dalam repositori publik.
Tujuan: Mencegah kebocoran kredensial aplikasi jika kode sumber (source code) jatuh ke tangan yang salah.

5. Konfirmasi Hapus (Sudo Mode)
Verifikasi ganda untuk tindakan destruktif.
Mekanisme: Pengguna wajib memasukkan password akun saat ingin menghapus file.
Tujuan: Mencegah penghapusan data secara tidak sengaja atau jika sesi browser pengguna sedang dibajak orang lain (Session Hijacking fisik).

6. Proteksi CSRF (Cross-Site Request Forgery)
Melindungi formulir dari manipulasi eksternal.
Mekanisme: Setiap form (Login, Upload, Delete) dilindungi oleh token unik (CSRF Token) yang divalidasi server.
Tujuan: Mencegah penyerang memaksa pengguna melakukan aksi (seperti hapus data) tanpa sepengetahuan pengguna melalui link jebakan.

7. Password Hashing (Tidak Ada Plaintext)
Penyimpanan kredensial yang aman.
Mekanisme: Password pengguna tidak disimpan dalam teks asli, melainkan di-hash menggunakan algoritma PBKDF2/Argon2 (SHA256).
Tujuan: Menjaga keamanan akun pengguna meskipun database berhasil dicuri oleh peretas.

8. Keamanan Sesi (Secure Session)
Perlindungan sesi browser pengguna.
HttpOnly Cookies: Cookie sesi tidak bisa diakses lewat JavaScript (Anti-XSS).
Anti-Back Button: Setelah logout, tombol "Back" pada browser tidak akan menampilkan halaman dashboard lagi (Halaman dilindungi decorator @login_required & header no-cache).
Tujuan: Menjaga kerahasiaan data jika komputer digunakan secara bergantian di tempat umum.


