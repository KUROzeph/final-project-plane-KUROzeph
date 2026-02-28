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
- [System Structure](#system-structure)
- [AI Trust and Emotion Behavior](#ai-trust-and-emotion-behavior)
- [Requirements and Dependencies](#requirements-and-dependencies)
- [How to Run](#how-to-run)
- [Known Issues](#known-issues)
- [References](#references)
- [How To Spice Up Your Romance](#how-to-spice-up-your-romance)

---
## System Structure

### Perception Layer
-YOLOv8 gesture detection
-Haar Cascade face detection
-Confidence threshold
-Temporal smoothing buffers

### Emotional Engine
-Trust variable (0–100)
-Positive/negative modifiers
-Time-based decay
-Love threshold
-Collapse trigger

### Behavior Layer
-Emotional category → movement magnitude
-Asynchronous execution
-State-based reaction

### Flight Control Layer
-PyMAVLink TCP connection
-GUIDED reposition commands
-Haversine distance tracking
-SITL Plane simulation

---
## AI Trust and Emotion Behavior
**Initial Trust**: 60

### What Affects Trust
|Increase Trust|Decrease Trust|
|Face on screen (+1)|More than 1 face on screen (-5)|
|Heart shaped hand (+10)|No face on screen (-3)|
|Thumbs up (+3)|Thumbs down(-5)|
|-|Did not give praise for too long(-1)|

### Behavior Based On Category
|Category|Trust Amount|Behavior|
|---|---|---|
|Obsessed|80-100|chance to overperform|
|Interested|50-79|no special act|
|Distanced|20-49|chance to underperform|
|Abandoned|1-19|chance to underperform, mess control detection|
|Broken|0(if obsessed has been reached)|force aggresive landing|


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
- jika menggunakan webcam laptop ada kemungkinan akan stutter dan object detection kurang lancar
- model object detection kesulitan ketika membedakan point_east dan point_west
- pesawat tidak akan selalu mengikuti command dengan sangat lurus (ex: point_west => bergerak ke kiri dengan sedikit miring keatas)

---

## References
- https://mavlink.io/en/messages/common.html
- https://ardupilot.org/planner/docs/common-mavlink-mission-command-messages-mav_cmd.html

---

## How To Spice Up Your Romance
![uma](img/uma-musume-still-in-love-uma-musume.gif)
![redf](img/FyeNVAraAAEQQKN.jpg)

1. Maintain healthy relationship, dont ignore but dont get too attached
2. If already head over heels, too late.
3. have fun.
