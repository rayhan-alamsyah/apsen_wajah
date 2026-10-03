# ==========================================================
# WAJAH.PY
#
# Tugas:
# 1. Menjalankan YOLO
# 2. Mendeteksi wajah
# 3. Menambahkan karyawan baru
# 4. Mengambil 2 foto untuk karyawan baru
# 5. Mengubah foto menjadi data/pola angka menggunakan LBPH
# 6. Mengenali wajah saat absensi
# ==========================================================


# ==========================================================
# IMPORT LIBRARY
# ==========================================================

import cv2
import os
import json
import time

from ultralytics import YOLO


# ==========================================================
# MENENTUKAN LOKASI FOLDER
# ==========================================================

# Mengambil lokasi folder Face_id
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Folder tempat menyimpan foto karyawan
FOLDER_KARYAWAN = os.path.join(
    BASE_DIR,
    "db_karyawan"
)


# Folder untuk menyimpan model hasil training
FOLDER_MODEL = os.path.join(
    BASE_DIR,
    "model"
)


# File model LBPH
FILE_MODEL = os.path.join(
    FOLDER_MODEL,
    "wajah.yml"
)


# File yang menyimpan ID dan nama karyawan
FILE_NAMA = os.path.join(
    FOLDER_MODEL,
    "nama.json"
)


# File model YOLO
FILE_YOLO = os.path.join(
    BASE_DIR,
    "best.pt"
)


# ==========================================================
# MEMBUAT FOLDER JIKA BELUM ADA
# ==========================================================

os.makedirs(
    FOLDER_KARYAWAN,
    exist_ok=True
)

os.makedirs(
    FOLDER_MODEL,
    exist_ok=True
)


# ==========================================================
# MEMUAT MODEL YOLO
# ==========================================================

print()
print("======================================")
print("       MEMUAT MODEL YOLO")
print("======================================")

model_yolo = YOLO(FILE_YOLO)

print("Model YOLO berhasil dimuat.")


# ==========================================================
# MEMBUAT LBPH FACE RECOGNIZER
# ==========================================================

# LBPH digunakan untuk mengenali wajah.
#
# Foto wajah akan diubah menjadi pola/data
# yang dapat dibandingkan dengan wajah kamera.
#
# Jadi kita tidak perlu menyimpan ratusan foto
# untuk mengenali satu karyawan.

recognizer = cv2.face.LBPHFaceRecognizer_create()


# ==========================================================
# DATA NAMA KARYAWAN
# ==========================================================

# Contoh:
#
# {
#     "1": "rayhan",
#     "2": "budi"
# }

nama_data = {}


# ==========================================================
# FUNGSI MENGAMBIL WAJAH
# ==========================================================

def ambil_wajah(frame):

    # YOLO mendeteksi wajah
    hasil = model_yolo(
        frame,
        verbose=False
    )


    # Memeriksa hasil YOLO
    for result in hasil:

        # Memeriksa semua kotak wajah
        for box in result.boxes:

            # Mengambil koordinat wajah
            x1, y1, x2, y2 = box.xyxy[0]

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)


            # Membatasi koordinat
            # agar tidak keluar dari gambar

            x1 = max(
                0,
                x1
            )

            y1 = max(
                0,
                y1
            )

            x2 = min(
                frame.shape[1],
                x2
            )

            y2 = min(
                frame.shape[0],
                y2
            )


            # Memotong bagian wajah
            wajah = frame[
                y1:y2,
                x1:x2
            ]


            # Jika hasil crop kosong
            if wajah.size == 0:

                continue


            # Mengembalikan wajah pertama
            return wajah


    # Tidak ada wajah
    return None


# ==========================================================
# FUNGSI DETEKSI YOLO
# ==========================================================

def deteksi_yolo(frame):

    # Membuat salinan gambar
    hasil_frame = frame.copy()


    # Menjalankan YOLO
    hasil = model_yolo(
        hasil_frame,
        verbose=False
    )


    # Membaca hasil YOLO
    for result in hasil:

        for box in result.boxes:

            # Koordinat wajah
            x1, y1, x2, y2 = box.xyxy[0]

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)


            # Membuat kotak wajah
            cv2.rectangle(
                hasil_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 255),
                2
            )


            # Menampilkan tulisan WAJAH
            cv2.putText(
                hasil_frame,
                "WAJAH",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )


    # Mengembalikan gambar
    return hasil_frame


# ==========================================================
# FUNGSI MELATIH DATABASE WAJAH
# ==========================================================

def latih_database():

    global nama_data


    # Tempat menyimpan gambar
    gambar_training = []


    # Tempat menyimpan ID gambar
    label_training = []


    # Mengosongkan data nama
    nama_data = {}


    # Menyimpan hubungan:
    #
    # nama -> ID
    #
    # Contoh:
    #
    # rayhan -> 1
    # budi   -> 2

    id_nama = {}


    # ID pertama
    nomor_id = 1


    # ======================================================
    # MEMBACA FOTO DATABASE
    # ======================================================

    for nama_file in sorted(
        os.listdir(FOLDER_KARYAWAN)
    ):


        # Hanya membaca file gambar
        if not nama_file.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png"
            )
        ):

            continue


        # Lokasi foto
        lokasi = os.path.join(
            FOLDER_KARYAWAN,
            nama_file
        )


        # Membaca foto
        gambar = cv2.imread(
            lokasi
        )


        # Jika foto tidak bisa dibaca
        if gambar is None:

            print(
                f"Foto tidak dapat dibaca: {nama_file}"
            )

            continue


        # ==================================================
        # MENGAMBIL NAMA KARYAWAN
        #
        # Contoh:
        #
        # rayhan_1.jpg
        # rayhan_2.jpg
        #
        # menjadi:
        #
        # rayhan
        # ==================================================

        nama_tanpa_ext = os.path.splitext(
            nama_file
        )[0]


        nama = nama_tanpa_ext.rsplit(
            "_",
            1
        )[0]


        # ==================================================
        # MENENTUKAN ID KARYAWAN
        # ==================================================

        # Jika nama belum memiliki ID
        if nama not in id_nama:

            # Berikan ID baru
            id_nama[nama] = nomor_id


            # Simpan ID dan nama
            nama_data[
                str(nomor_id)
            ] = nama


            # ID berikutnya
            nomor_id += 1


        # Ambil ID karyawan
        id_karyawan = id_nama[nama]


        # ==================================================
        # MENGUBAH GAMBAR MENJADI GRAYSCALE
        # ==================================================

        gambar_gray = cv2.cvtColor(
            gambar,
            cv2.COLOR_BGR2GRAY
        )


        # Menyamakan ukuran semua wajah
        gambar_gray = cv2.resize(
            gambar_gray,
            (200, 200)
        )


        # Masukkan gambar ke training
        gambar_training.append(
            gambar_gray
        )


        # Masukkan ID karyawan
        label_training.append(
            id_karyawan
        )


    # ======================================================
    # CEK DATA
    # ======================================================

    if len(gambar_training) == 0:

        print()
        print(
            "Belum ada foto karyawan."
        )

        return False


    # ======================================================
    # TRAINING LBPH
    # ======================================================

    print()
    print(
        "Mengubah foto menjadi data/pola angka..."
    )


    recognizer.train(
        gambar_training,
        __import__("numpy").array(
            label_training
        )
    )


    # ======================================================
    # MENYIMPAN MODEL
    # ======================================================

    recognizer.write(
        FILE_MODEL
    )


    # ======================================================
    # MENYIMPAN NAMA
    # ======================================================

    with open(
        FILE_NAMA,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            nama_data,
            file,
            ensure_ascii=False,
            indent=4
        )


    # ======================================================
    # INFORMASI
    # ======================================================

    print()
    print(
        "======================================"
    )

    print(
        "Database wajah berhasil dilatih."
    )

    print(
        f"Jumlah foto      : {len(gambar_training)}"
    )

    print(
        f"Jumlah karyawan  : {len(nama_data)}"
    )

    print(
        "======================================"
    )


    return True


# ==========================================================
# FUNGSI MEMUAT DATABASE
# ==========================================================

def muat_database():

    global nama_data


    # Jika model belum ada
    if not os.path.exists(
        FILE_MODEL
    ):

        print()
        print(
            "Model wajah belum tersedia."
        )

        # Coba membuat model
        return latih_database()


    # Membaca model LBPH
    recognizer.read(
        FILE_MODEL
    )


    # Membaca daftar nama
    if os.path.exists(
        FILE_NAMA
    ):

        with open(
            FILE_NAMA,
            "r",
            encoding="utf-8"
        ) as file:

            nama_data = json.load(
                file
            )


    print(
        "Database wajah siap digunakan."
    )


    return True


# ==========================================================
# FUNGSI TAMBAH KARYAWAN
# ==========================================================

def tambah_karyawan(kamera):

    print()
    print(
        "======================================"
    )

    print(
        "          TAMBAH KARYAWAN"
    )

    print(
        "======================================"
    )


    # Meminta nama
    nama = input(
        "Masukkan nama karyawan: "
    ).strip()


    # Jika nama kosong
    if nama == "":

        print(
            "Nama tidak boleh kosong."
        )

        return


    # Mengubah spasi menjadi _
    nama_file = nama.replace(
        " ",
        "_"
    )


    print()
    print(
        f"Nama: {nama}"
    )

    print(
        "Sistem akan mengambil 2 foto."
    )

    print(
        "Pastikan wajah terlihat jelas."
    )

    print()


    # ======================================================
    # MENGAMBIL 2 FOTO
    # ======================================================

    for nomor in range(
        1,
        3
    ):

        print(
            f"Siapkan foto ke-{nomor}..."
        )


        # Waktu persiapan
        time.sleep(2)


        # Membaca kamera
        berhasil, frame = kamera.read()


        if not berhasil:

            print(
                "Gagal membaca kamera."
            )

            return


        # Mencari wajah dengan YOLO
        wajah = ambil_wajah(
            frame
        )


        # Jika wajah tidak ditemukan
        if wajah is None:

            print(
                "Wajah tidak ditemukan."
            )

            print(
                "Pendaftaran dibatalkan."
            )

            return


        # Nama foto
        nama_foto = (
            f"{nama_file}_{nomor}.jpg"
        )


        # Lokasi foto
        lokasi = os.path.join(
            FOLDER_KARYAWAN,
            nama_foto
        )


        # Menyimpan foto
        berhasil_simpan = cv2.imwrite(
            lokasi,
            wajah
        )


        if berhasil_simpan:

            print(
                f"Foto {nomor} berhasil disimpan."
            )

        else:

            print(
                f"Foto {nomor} gagal disimpan."
            )

            return


    # ======================================================
    # TRAINING SETELAH 2 FOTO
    # ======================================================

    print()
    print(
        "Mengubah foto menjadi data/pola angka..."
    )


    berhasil_training = latih_database()


    if berhasil_training:

        print()
        print(
            f"Karyawan {nama} berhasil ditambahkan."
        )

    else:

        print(
            "Gagal membuat database wajah."
        )


# ==========================================================
# FUNGSI MENGENALI WAJAH
# ==========================================================

def kenali_wajah(frame):

    # Jika database belum ada
    if not nama_data:

        print(
            "Database wajah belum tersedia."
        )

        berhasil = muat_database()


        if not berhasil:

            return None


    # Mengambil wajah dari kamera
    wajah = ambil_wajah(
        frame
    )


    # Jika tidak ada wajah
    if wajah is None:

        print(
            "Wajah tidak ditemukan."
        )

        return None


    # ======================================================
    # GRAYSCALE
    # ======================================================

    wajah_gray = cv2.cvtColor(
        wajah,
        cv2.COLOR_BGR2GRAY
    )


    # Menyamakan ukuran
    wajah_gray = cv2.resize(
        wajah_gray,
        (200, 200)
    )


    # ======================================================
    # PREDIKSI LBPH
    # ======================================================

    label, confidence = recognizer.predict(
        wajah_gray
    )


    # ======================================================
    # BATAS CONFIDENCE
    #
    # Semakin kecil = semakin mirip.
    #
    # Untuk awal kita gunakan 70.
    # Nanti bisa disesuaikan setelah pengujian.
    # ======================================================

    BATAS_CONFIDENCE = 70


    # Jika confidence terlalu besar
    if confidence > BATAS_CONFIDENCE:

        print(
            f"Wajah tidak dikenali "
            f"(confidence: {confidence:.2f})"
        )

        return None


    # ======================================================
    # MENCARI NAMA BERDASARKAN ID
    # ======================================================

    nama = nama_data.get(
        str(label)
    )


    # Jika ID tidak ditemukan
    if nama is None:

        print(
            "Identitas tidak ditemukan."
        )

        return None


    # ======================================================
    # BERHASIL DIKENALI
    # ======================================================

    print()
    print(
        f"Wajah dikenali: {nama}"
    )

    print(
        f"Confidence: {confidence:.2f}"
    )


    return nama


# ==========================================================
# MEMUAT DATABASE SAAT PROGRAM DIMULAI
# ==========================================================

muat_database()