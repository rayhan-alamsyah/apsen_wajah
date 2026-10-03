# ==========================================================
# ABSENSI.PY
#
# Mengatur aturan:
#
# PAGI       = MASUK
# SIANG      = PULANG
#
# Maksimal:
# MASUK  = 2 kali
# PULANG = 2 kali
# ==========================================================

from datetime import datetime

# Mengambil fungsi dari database.py
from database import (
    hitung_absensi,
    simpan_absensi
)


# ==========================================================
# PROSES ABSENSI
# ==========================================================

def proses_absensi(
    nama,
    frame
):

    # Mengambil waktu sekarang
    sekarang = datetime.now()


    # Mengambil tanggal
    tanggal = sekarang.strftime(
        "%Y-%m-%d"
    )


    # Mengambil jam
    jam = sekarang.strftime(
        "%H:%M:%S"
    )


    # ======================================================
    # MENENTUKAN SESI
    # ======================================================

    # Sebelum jam 12 = MASUK
    if sekarang.hour < 12:

        sesi = "MASUK"


    # Jam 12 atau lebih = PULANG
    else:

        sesi = "PULANG"


    print()
    print(
        f"Nama   : {nama}"
    )

    print(
        f"Tanggal: {tanggal}"
    )

    print(
        f"Jam    : {jam}"
    )

    print(
        f"Sesi   : {sesi}"
    )


    # ======================================================
    # CEK JUMLAH ABSEN
    # ======================================================

    jumlah = hitung_absensi(
        nama,
        tanggal,
        sesi
    )


    # Maksimal 2 kali
    if jumlah >= 2:

        print()
        print(
            f"ABSEN DITOLAK"
        )

        print(
            f"{nama} sudah absen "
            f"{sesi} sebanyak 2 kali."
        )

        return


    # ======================================================
    # SIMPAN ABSENSI
    # ======================================================

    nomor_absen = jumlah + 1


    simpan_absensi(
        nama,
        tanggal,
        jam,
        sesi,
        nomor_absen,
        frame
    )


    print()
    print(
        "================================"
    )

    print(
        "       ABSEN BERHASIL"
    )

    print(
        "================================"
    )

    print(
        f"Nama   : {nama}"
    )

    print(
        f"Tanggal: {tanggal}"
    )

    print(
        f"Jam    : {jam}"
    )

    print(
        f"Sesi   : {sesi}"
    )

    print(
        f"Absen ke-{nomor_absen}"
    )

    print(
        "================================"
    )