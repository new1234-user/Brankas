# Brankas Online
Aplikasi website sederhana untuk menyimpan file pribadi secara aman
## Cara Menjalankan Aplikasi
1. Buka Terminal di dalam folder project.
2. Install Library:
   pip install django python-dotenv argon2-cffi
3. Siapkan Database:
   python manage.py makemigrations
   python manage.py migrate
4. Jalankan Server:
   python manage.py runserver
5. Buka Browser:
   Akses alamat: http://127.0.0.1:8000/login/
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