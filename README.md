# Automatic Coin Sorter

A DIY project to build an automated Euro coin sorter. This machine uses 3D-printed mechanical parts to separate coins and is controlled by a Raspberry Pi Pico W running MicroPython.



## 📝 Overview

The goal of this project is to automatically identify Euro coins (from 1 Cent to 2 Euros) and sort them into separate containers. The mechanics are based entirely on 3D-printed parts.

A Pi Pico W controls the entire process. A DC motor drives the coin mechanism, while an ST7735 display provides feedback on the status or counted totals.

---

## ⚙️ Hardware Components

* **Mechanics:** 3D-printed sorting mechanism (STLs are located in the `/stl` folder)
* **Microcontroller:** Raspberry Pi Pico W
* **Motor:** Standard DC Motor
* **Motor Driver:** DRV8833
* **Sensor:** INA219 (Current sensor, e.g., for jam detection)
* **Display:** 160x128 RGB Display (ST7735)

---

## 🐍 Software

This project is written in **MicroPython**.

---

## 🚀 Setup & Installation

1.  **Mechanics:** Print all required parts from the `/stl` folder.
2.  **Electronics:** Connect the components to the Pi Pico W according to the (still to be created) wiring diagram.
3.  **Software:**
    * Flash newest MicroPython firmware onto your Pi Pico W.
    * Upload `main.py`, `config.py` and also `\lib`,`\image`,`\font` folders to the Pico.
4.  **Test:** Start the machine and insert coins.

---

## 🤝 Acknowledgements & Reused Code

The code in this repository reuses and adapts functions from the excellent work of the MicroPython community. Their libraries provided the foundation for implementing the detailed hardware control functions of this project.

Special thanks go to:
* **[AnthonyKNorman](https://github.com/AnthonyKNorman/MicroPython_ST7735)** a simple light weight ST7735 driver.

* **[antirez](https://github.com/antirez/microfont)** and **[peter-l5](https://github.com/peter-l5/framebuf2)** for extending the frambuf class

* **[(https://github.com/robert-hh](https://github.com/robert-hh/INA219)** for the INA219 driver.
