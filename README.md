# Brankas Pribadi (Django)
## Cara Menjalankan Aplikasi
1) Masuk ke folder project
Buka terminal pada folder yang berisi file `manage.py`.
2) Buat & aktifkan Virtual Environment
3) Windows
* python -m venv .venv
* .venv\Scripts\activate
4) Linux / Mac
* python -m venv .venv
* source .venv/bin/activate
5) Install dependensi
* python -m pip install -r requirements.txt
6) Siapkan database (migrations)
* python manage.py migrate
7) Jalankan server
* python manage.py runserver
8) Akses aplikasi di browser
* Login: http://127.0.0.1:8000/login/
---
## Fitur Utama
* Login & Register: Sistem pendaftaran dan masuk akun pengguna.
* Dashboard: Halaman khusus menampilkan daftar file milik pengguna sendiri.
* Upload: Unggah file dokumen atau gambar ke server.
* Download: Unduh file yang sudah disimpan sebelumnya.
* Delete: Menghapus file secara permanen dengan konfirmasi password.
---
## Aspek Keamanan (Security)
Aplikasi ini telah menerapkan standar keamanan wajib untuk memitigasi risiko serangan web umum:
1) Password Hashing (Tidak Ada Plaintext)
* Mekanisme: Registrasi dan login memakai form bawaan Django (UserCreationForm dan AuthenticationForm) yang menyimpan password dalam bentuk hash (PBKDF2/HMAC-SHA256 dan kompatibel Argon2), bukan teks asli.
* Tujuan: Jika database mengalami kebocoran, password tidak bisa dibaca secara langsung.

2) Proteksi CSRF (Cross-Site Request Forgery)
* Mekanisme: Semua form POST (login, upload, delete) dilindungi CSRF Middleware dan token {% csrf_token %} Sehingga request tanpa token valid akan ditolak.
* Tujuan: Mencegah attack dari pihak ketiga tanpa izin user.

3) Input Validation (Anti SQL Injection & XSS)
* Mekanisme: Validasi dilakukan lewat constraint pada Model (tipe data, panjang karakter) dan Django ORM (parameterized query). Payload seperti SQL injection dan <script>...</script> tidak dieksekusi.
* Tujuan: Mencegah manipulasi query database dan eksekusi script berbahaya (XSS).

4) File Upload Sanitization (Whitelist Ekstensi + Batas Ukuran)
* Mekanisme: Upload file dibatasi dengan whitelist ekstensi (dokumen/gambar) dan ukuran file melalui validator. File di luar ketentuan (contoh .exe) akan ditolak.
* Tujuan: Mencegah upload malware/webshell dan mengurangi risiko DoS melalui file besar.

5) Sanitasi Nama File (Anti Webshell / Overwrite)
* Mekanisme: Nama file diubah menjadi nama aman/unik (misal berbasis UUID/random) agar tidak bisa menimpa file sistem atau “menyisipkan” nama file yang berbahaya.
* Tujuan: Mencegah overwriting file, path trick dan mempersulit penyisipan webshell.

6) Privasi Data & Isolasi (Anti-IDOR / Object-Level Authorization)
* Mekanisme: Data dashboard difilter berdasarkan request.user, sehingga user hanya melihat file miliknya.
* Tujuan: Mencegah user A mengakses file user B walaupun tahu URL/ID.

7) Secure Download
* Mekanisme: Sebelum file dikirim ke client, sistem melakukan pengecekan hak akses (owner check) secara real-time.
* Tujuan: Memastikan hanya pemilik sah yang dapat mengunduh file.

8) Access Control untuk Aksi Destruktif (Delete Protection / Sudo Mode)
* Mekanisme: Penghapusan file tidak hanya mengandalkan sesi login, tetapi juga meminta konfirmasi tambahan berupa input ulang password sebelum delete dieksekusi.
* Tujuan: Mencegah penghapusan tidak sengaja dan mengurangi risiko saat sesi dibajak atau ditinggal terbuka.

9) Manajemen Rahasia (No Hardcoded Secrets)
* Mekanisme: SECRET_KEY dan konfigurasi sensitif tidak ditulis di source code, tetapi diletakkan di .env/environment variables (via python-dotenv).
* Tujuan: Mencegah kebocoran secret jika source code tersebar atau dipublikasikan.

10) Keamanan Sesi (Secure Session Cookie)
* Mekanisme: Cookie sesi sessionid diberi flag HttpOnly sehingga tidak dapat diakses oleh JavaScript sehingga menekan risiko pencurian sesi via XSS.
* Tujuan: Melindungi token sesi dari pencurian berbasis script.

11) Session Timeout & Auto Logout
* Mekanisme: Sistem menerapkan idle timeout (misal 15 menit) dan sesi berakhir saat browser ditutup.
* Tujuan: Mengurangi risiko akun tetap terbuka pada perangkat publik atau dipakai bergantian.

12) Proteksi Halaman (Authentication Gate)
* Mekanisme: Halaman sensitif (dashboard, download, delete) dilindungi @login_required/pemeriksaan autentikasi sehingga user yang belum login tidak bisa mengakses.
* Tujuan: Memastikan data hanya bisa diakses setelah autentikasi.

13) Audit Log
* Mekanisme: Aktivitas penting seperti login sukses/gagal, akses file, dan penghapusan dicatat pada log server.
* Tujuan: Mendukung monitoring, troubleshooting, dan kebutuhan forensik jika terjadi insiden.

14) Prinsip Least Privilege pada Akses Data
* Mekanisme: Query dan operasi file selalu “dibatasi konteks user” (scope per-user). Sistem tidak menyediakan endpoint yang mengambil semua data tanpa filter kepemilikan.
* Tujuan: Meminimalkan dampak jika terjadi kesalahan akses atau percobaan enumerasi data.