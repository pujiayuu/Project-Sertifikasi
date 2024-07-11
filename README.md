# Project-Sertifikasi
Project Sertifikasi Kompetensi (Programming)

Terdapat 5 Kelas (Class), yaitu class Item sebagai kelas induk, class Book dan class Magazine yang mewarisi sifat dari kelas Item, untuk basis data dirancang pada class LibraryDatabase, dan untuk interaksi pengguna disusun pada class LibraryInterface.

Pada projek ini memiliki akses basis data MySQL, digunakan untuk menyimpan informasi tentang buku dan majalah. Menggunakan Package SQLAlchemy untuk berinteraksi dengan basis data ini secara efisien melalui ORM (Object-Relational Mapping). 

Pada kelas LibraryDatabase terdapat :
Metode add dapat menerima objek Book atau Magazine dan menambahkannya ke database. 
Metode list dapat menerima tipe Book atau Magazine dan mengembalikan daftar item yang sesuai dari database. 
Metode update dapat memperbarui objek Book atau Magazine tergantung pada tipe item yang diberikan. 
Metode delete dapat menghapus objek Book atau Magazine dari database.

Pada kelas LibraryInterface terdapat :
add_item - Metode ini memungkinkan pengguna untuk menambahkan item baru (buku atau majalah) ke dalam sistem.
list_items - Metode ini memungkinkan pengguna untuk melihat daftar item (buku atau majalah) yang ada di dalam sistem.
update_item - Metode ini memungkinkan pengguna untuk memperbarui detail item yang sudah ada.
delete_item - Metode ini memungkinkan pengguna untuk menghapus item dari sistem.
save_to_file - Metode ini memungkinkan pengguna untuk menyimpan data item (buku dan majalah) ke dalam file JSON.
load_from_file - Metode ini memungkinkan pengguna untuk memuat data item dari file JSON.
main_menu - Metode ini menampilkan menu utama dan mengelola input pengguna untuk melakukan operasi yang diinginkan.


