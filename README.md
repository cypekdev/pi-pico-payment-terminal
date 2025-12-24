# 💳Raspberry Pi Pico RFID Payment Terminal
<img width="50%" alt="terminal" src="https://github.com/user-attachments/assets/7ba15377-0681-44e3-a3cf-6d9c9e9d0bd2" align="right"/>

The **Raspberry Pi Pico RFID Payment Terminal** is an educational payment terminal simulator created as part of the [ZS10 Bank – Digital Banking Simulator](https://github.com/cypekdev/zs10bank-frontend).

This module demonstrates how **contactless payments (RFID / NFC)** work in modern banking systems — in a safe, controlled, and fully simulated environment.

---

## 🎯 Project Purpose

The main goal of this project is to:
- introduce students to **cashless payments and RFID technology**,  
- explain how **payment terminals communicate with banking systems**,  
- show the role of **security, authorization, and transaction validation** in everyday payments.

---

## 🧠 Educational Value

This project is designed for workshops and demonstrations aimed at:
- children and teenagers entering the world of digital finance,  
- students learning about **embedded systems**, **IoT**, and **software engineering**,  
- showcasing how hardware and software cooperate in financial technology.

---

## 🎨 Industrial Design – Terminal Housing

As part of the project, the **physical appearance of the RFID payment terminal was fully designed from scratch** using **Autodesk Fusion 360**.

The goal of the design process was to:
- reflect the look and feel of **real-world payment terminals**,  
- ensure **ergonomics and ease of use** for younger users,  
- provide proper space for all electronic components (RFID reader, display, microcontroller),  
- and make the enclosure suitable for **educational workshops and demonstrations**.

The enclosure was designed with practicality in mind, allowing easy assembly, maintenance, and potential 3D printing.  
Special attention was paid to:
- card placement area (RFID reading zone),
- screen visibility angle,
- durability and portability.

This design stage helps students understand that **fintech products are not only software**, but also a combination of **hardware, usability, and industrial design**.

---

## 🖼️ Design Preview

Below are preview images of the terminal enclosure designed in **Fusion 360**.

> These visuals present the conceptual and functional design of the device used in the ZS10 Bank ecosystem.

### 📐 3D Model 

<img width="55%" alt="3d84b075-a52d-41fb-b49c-ca15921b9e3b" src="https://github.com/user-attachments/assets/2a333f9e-ba8f-482e-a4f8-018a8c96d8ba" align="right" />
<img width="40%" alt="Screenshot 2025-12-24 151304" src="https://github.com/user-attachments/assets/40732b98-702a-4846-82ed-a93f355ed9bc" />
<img width="40%" alt="Screenshot 2025-12-24 151454" src="https://github.com/user-attachments/assets/795edab7-ea40-498b-a950-06724da71a78" />

[3D view online](https://a360.co/3XUdAIW)

[TerminalFinal Drawing v3.pdf](https://github.com/user-attachments/files/24330591/TerminalFinal.Drawing.v3.pdf)

The design can be easily adapted or extended for future versions of the terminal.

---

## 🧩 System Overview

The RFID terminal is a **separate component** of the ZS10 Bank ecosystem and works together with:
- the **ZS10 Bank backend API** (transaction validation),
- the [**ZS10 Bank frontend**](https://github.com/cypekdev/zs10bank-frontend) (account balance & transaction history).

### Typical payment flow:

1. User places an RFID card over the LCD screen or inserts card from bottom of terminal
2. Terminal reads the card UID  
3. Transaction request is sent to the backend  
4. Backend validates the account and balance  
5. Terminal displays approval or rejection  

---


## 🧰 Tech Stack


### Hardware
- Microcontroller **Raspberry Pi Pico**  
- RFID reader **MFRC522**
- Display **LCD**
- **Buzzer** and RGB LEDs **ws2812b** for user feedback  

### Software
- **MicroPython** – firmware logic  
- **HTTP** communication  
- JSON-based transaction messages  

---

## ⚙️ Features

| Feature | Status |
|--------|--------|
| RFID card detection | ✅ |
| Simulated payment authorization | ✅ |
| Communication with bank backend | ✅ |
| Visual & sound feedback | ✅ |
| PIN / confirmation step | 🏗️ Planned |



