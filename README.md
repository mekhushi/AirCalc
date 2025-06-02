# 🖐️ AirCalc — Touchless Virtual Calculator

---

## 🚀 Problem Statement

In a world increasingly aware of hygiene and the need for **contactless interactions**, physical devices like calculators still require touch, which can spread germs—especially in **public spaces, hospitals, classrooms**, and **shared offices**. Traditional calculators are not optimized for this new normal, creating a need for a clean, intuitive, and accessible way to perform calculations without physical contact.

**AirCalc** addresses this by leveraging **real-time hand tracking** to detect natural **pinch gestures** in front of a webcam, allowing users to “press” buttons drawn right onto the live video feed. This touchless approach helps reduce contamination risk, enhances accessibility for users with mobility constraints, and introduces a futuristic, gesture-driven way to interact with everyday tools.

---

## ✨ Key Features

- **Real-time hand tracking** using [MediaPipe](https://mediapipe.dev/) for accurate hand landmark detection 🤚  
- **Pinch gesture detection** (thumb + index finger) to emulate button presses 🤏  
- **Debounce timer** to prevent multiple accidental inputs from shaky or held gestures ⏳  
- Fully **custom UI rendered on OpenCV canvas** (the video feed), with neumorphic-style buttons and shadows to create a modern, mobile-calculator feel 🖌️  
- **Dynamic display panel** shows current expression and results clearly 🧮  
- **History sidebar** logs previous calculations for easy reference 📜  
- Lightweight and cross-platform — runs anywhere Python and a webcam are available 🐍💻  
- Designed with **accessibility** and **hygiene** in mind, offering an innovative interaction model 💡  

---

## 🎨 UI Design & Interaction

- The UI is **drawn programmatically on the webcam feed**, blending live video with a graphical calculator interface.  
- Neumorphic buttons feature layered shadows and highlights to mimic soft, tactile surfaces on screen.  
- When the user pinches near a button, it visually “presses” and triggers the corresponding input.  
- The history panel is updated live and neatly aligned on the side for seamless tracking of calculations.  
- Debounce logic ensures smooth, glitch-free user experience.

---

## 📸 Screenshot Preview

![AirCalc Preview](your-screenshot.png)  
*Pinch your fingers near buttons to input numbers and operations.*

---

## 🛠️ Installation & Usage

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/Aircalc.git
   cd Aircalc
   ```
2 . Install dependencies:
   ```bash
  pip install -r requirements.txt
  ``` 
3.Run the application:

```bash
python calculator.py
```
---
## 🤝Contributing
Contributions and feedback are welcome! Please open issues or pull requests to help improve AirCalc. Ideas for enhancement:

Add sound effects 🎵

Improve gesture recognition (multi-hand support) ✋🤚

Add customizable themes 🎨

Deploy on Raspberry Pi or mobile devices 📱

---

## 📄 License
This project is licensed under the MIT License — see the LICENSE file for details.

---
## 🙏 Acknowledgments
Google MediaPipe for state-of-the-art hand tracking technology ✋

OpenCV for powerful real-time computer vision tools 📷

Inspiration from neumorphic UI design trends 🎨
   

   
