[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/cv71rJiY)
# FINAL-PROJECT

| Nama           | NRP        | Prodi     |
| ---            | ---        | ----------|
|Zaldy Duma Malik|5048251001|Teknik Telekomunikasi|

Clone repo ini lalu isi dengan workspace/pekerjaan kalian. 

## !!! JANGAN UPLOAD FILE LEWAT GITHUB WEB !!! 

Jadikan git bash sebagai temanmu. Jika terlihat melakukan commit upload file (kecuali README.md) akan terkena penalty

PPT dan Video masukkan \docs.

Jika size terlalu besar bisa masukkan ke drive lalu masukkan linknya

---

# Sistem Kendali SITL Fixed Wing Berbasis Gestur Tangan dengan Personalisasi Yandere.
> *Sudahkah kamu mencintai dronemu? atau kamu selama ini hanya menganggap drone sebagai objek transportasi?*
> *ajaklah kencan dronemu dengan program ini!*

Program ini merupakan simulasi fixed wing menggunakan SITL Mission Planner yang telah terintegrasi PyMAVLink sebagai hati pergerakan drone, lalu juga Computer Vision dengan YOLOv8 sebagai mata dan otak untuk memproses gestur pengguna dan hubungannya dengan drone

---
## Daftar Isi
- [Requirements and Dependencies](#requirements-and-dependencies)
- [How to Run](#how-to-run)
- [Known Issues](#known-issues)
- [References](#references)
- [How To Spice Up Your Romance](#how-to-spice-up-your-romance)

---

## Requirements and Dependencies
untuk menjalankan program ini diperlukan beberapa package dan software

### System Requirements
- Python 3.10+
- Mission Planner
- Camera/Webcam

### Python Packages
```bash
pip install pymavlink ultralytics opencv-python numpy
```
---

## How to Run
Berikut langkah langkah yang perlu dilakukan untuk menjalankan program ini

### Setup Mission Planner
1. Buka Mission Planner
2. Masuk ke tab "Simulation" dan mulai SITL Plane
3. Masuk ke tab "Plan" dan  load "initial_takeoff_waypoints"
4. Write dan Read
5. Masuk ke tab Data

### Setup Program
1. Masuk ke directory Final Project Plane
2. Ubah permission file script
```bash
chmod +x yandere_plane.sh
```
3. Jalankan script
```bash
./yandere_plane.sh
```

script ini akan membuat 3 window secara otomatis berupa:
- Distance Tracker
- AI Cognition
- FOV

#### Catatan
FOV akan generate setelah drone memasuki mode guided

---

## Known Issues

---

## References

---

# How To Spice Up Your Romance
