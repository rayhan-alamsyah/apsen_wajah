# ==========================================================
# KAMERA.PY
# Mengatur kamera dan tombol keyboard
#
# A      = Tambah karyawan
# SPASI  = Absensi
# Q      = Keluar
# ==========================================================

import cv2

# Mengambil fungsi dari wajah.py
from wajah import (
    deteksi_yolo,
    tambah_karyawan,
    kenali_wajah
)

# Mengambil fungsi absensi dari absensi.py
from absensi import proses_absensi


# ==========================================================
# PENGATURAN KAMERA
# ==========================================================

# Kamera yang ingin diprioritaskan
#
# 0 = biasanya kamera laptop
# 1 = biasanya webcam USB / external
#
# Jika webcam external kamu terbaca sebagai kamera 1,
# program akan menggunakan kamera 1 terlebih dahulu.

CAMERA_EXTERNAL = 1
CAMERA_LAPTOP = 0


# ==========================================================
# FUNGSI MEMBUKA KAMERA
# ==========================================================

def buka_kamera():

    print()
    print("Mencari kamera...")

    # ------------------------------------------------------
    # COBA WEBCAM EXTERNAL TERLEBIH DAHULU
    # ------------------------------------------------------

    print(f"Mencoba kamera external (index {CAMERA_EXTERNAL})...")

    kamera = cv2.VideoCapture(CAMERA_EXTERNAL)

    if kamera.isOpened():

        print("Webcam external berhasil dibuka.")

        return kamera


    # Jika kamera external gagal
    kamera.release()


    # ------------------------------------------------------
    # COBA KAMERA LAPTOP
    # ------------------------------------------------------

    print("Webcam external tidak ditemukan.")
    print(f"Mencoba kamera laptop (index {CAMERA_LAPTOP})...")

    kamera = cv2.VideoCapture(CAMERA_LAPTOP)

    if kamera.isOpened():

        print("Kamera laptop berhasil dibuka.")

        return kamera


    # ------------------------------------------------------
    # TIDAK ADA KAMERA
    # ------------------------------------------------------

    kamera.release()

    print()
    print("ERROR: Tidak ada kamera yang dapat dibuka.")

    return None


# ==========================================================
# FUNGSI MENJALANKAN KAMERA
# ==========================================================

def jalankan_kamera():

    print()
    print("======================================")
    print("       SISTEM ABSENSI WAJAH")
    print("======================================")
    print("A      = Tambah karyawan")
    print("SPASI  = Absen")
    print("Q      = Keluar")
    print("======================================")
    print()


    # ------------------------------------------------------
    # MEMBUKA KAMERA
    # ------------------------------------------------------

    kamera = buka_kamera()

    # Jika kamera tidak ditemukan
    if kamera is None:

        return


    # ======================================================
    # LOOP KAMERA
    # ======================================================

    while True:

        # Mengambil gambar dari kamera
        berhasil, frame = kamera.read()


        # Jika gagal membaca kamera
        if not berhasil:

            print("Gagal membaca gambar dari kamera.")

            break


        # --------------------------------------------------
        # DETEKSI WAJAH DENGAN YOLO
        # --------------------------------------------------

        frame_tampilan = deteksi_yolo(frame)


        # --------------------------------------------------
        # MENAMPILKAN PETUNJUK
        # --------------------------------------------------

        cv2.putText(
            frame_tampilan,
            "A = Tambah | SPACE = Absen | Q = Keluar",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        # --------------------------------------------------
        # MENAMPILKAN KAMERA
        # --------------------------------------------------

        cv2.imshow(
            "Kamera Absensi",
            frame_tampilan
        )


        # --------------------------------------------------
        # MEMBACA TOMBOL KEYBOARD
        # --------------------------------------------------

        tombol = cv2.waitKey(1) & 0xFF


        # ==================================================
        # TOMBOL A
        # TAMBAH KARYAWAN
        # ==================================================

        if tombol == ord("a"):

            print()
            print("======================================")
            print("         TAMBAH KARYAWAN")
            print("======================================")

            # Mengambil 2 foto untuk konfirmasi
            # identitas karyawan baru
            tambah_karyawan(kamera)


        # ==================================================
        # TOMBOL SPASI
        # ABSENSI
        # ==================================================

        elif tombol == ord(" "):

            print()
            print("======================================")
            print("             ABSENSI")
            print("======================================")

            # ------------------------------------------------
            # MENGENALI WAJAH
            # ------------------------------------------------
            #
            # Foto dari kamera akan diproses menjadi
            # angka/encoding wajah.
            #
            # Kemudian dibandingkan dengan database
            # karyawan.
            # ------------------------------------------------

            nama = kenali_wajah(frame)


            # ------------------------------------------------
            # JIKA WAJAH DIKENALI
            # ------------------------------------------------

            if nama is not None:

                print(f"Wajah dikenali sebagai: {nama}")

                # Menyimpan data absensi
                proses_absensi(
                    nama,
                    frame
                )


            else:

                print("Wajah tidak dikenali.")


        # ==================================================
        # TOMBOL Q
        # KELUAR
        # ==================================================

        elif tombol == ord("q"):

            print()
            print("Menutup sistem kamera...")

            break


    # ======================================================
    # MENUTUP KAMERA
    # ======================================================

    kamera.release()

    cv2.destroyAllWindows()

    print("Sistem kamera ditutup.")