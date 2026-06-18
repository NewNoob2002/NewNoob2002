<!-- ================= HERO ================= -->

<h1 align="center">⚡ Ted Guo</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&pause=1000&color=00F5FF&center=true&vCenter=true&width=650&lines=Embedded+Systems+Engineer;GNSS+%2F+RTK+Developer;ESP32+%2F+STM32+Firmware+Engineer;Low-Level+Debug+%2B+System+Architecture" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Embedded-C%2FC%2B%2B-00F5FF?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/GNSS-RTK%20System-7CFC00?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/MCU-ESP32%20%7C%20STM32-FF6B6B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/RTOS-FreeRTOS%20%7C%20ThreadX-FFD93D?style=for-the-badge"/>
</p>

---

# 🧠 SYSTEM ARCHITECTURE

```mermaid id="sys1"
flowchart TD
A[GNSS Signals] --> B[RF Frontend]
B --> C[Baseband Processing]
C --> D[Tracking Loop]
D --> E[Position Engine]

E --> F[MCU Firmware Layer]
F --> G[RTOS Scheduler]
G --> H[Drivers / Middleware]
H --> I[Application Layer]

I --> J[Debug / Telemetry]
J --> K[Logs / Trace / JTAG]
