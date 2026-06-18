<!-- ================== HERO DASHBOARD ================== -->

<div align="center">

# ⚡ TED GUO // EMBEDDED SYSTEMS

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&pause=900&color=00F5FF&center=true&vCenter=true&width=700&lines=GNSS+%2F+RTK+System+Engineer;Embedded+Firmware+Architect;ESP32+%2F+STM32+Low-Level+Developer;Debug-first+System+Designer" />

</div>

---

<!-- ================== STATUS PANEL ================== -->

## 📡 LIVE SYSTEM STATUS

<div align="center">

<img src="https://img.shields.io/badge/GNSS-Pipeline%20Active-00F5FF?style=for-the-badge"/>
<img src="https://img.shields.io/badge/RTK-FLOAT%20%2F%20FIX-7CFC00?style=for-the-badge"/>
<img src="https://img.shields.io/badge/MCU-ESP32%20%7C%20STM32-FF6B6B?style=for-the-badge"/>
<img src="https://img.shields.io/badge/DEBUG-JTAG%20READY-FFD93D?style=for-the-badge"/>

</div>

---

<!-- ================== SYSTEM ARCHITECTURE (CORE IDENTITY) ================== -->

## 🧠 SYSTEM ARCHITECTURE OVERVIEW

```mermaid id="hs_arch"
flowchart TD
A[GNSS Signals] --> B[RF Frontend]
B --> C[Baseband Processing]
C --> D[Tracking Loops]
D --> E[Position Engine]

E --> F[Embedded MCU Layer]
F --> G[RTOS Scheduling]
G --> H[Driver Abstraction Layer]
H --> I[Application Layer]

I --> J[Telemetry / Logging]
J --> K[Debug / Trace / Replay System]
