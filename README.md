# 🛡️ EyeGuard: AI-Powered Shoplifting Detection System

**EyeGuard** is an intelligent surveillance system designed to detect shoplifting activities in real time using computer vision and machine learning. It helps retailers reduce losses, increase security, and automate monitoring by identifying suspicious behaviors from live video feeds.

---

## 📌 Problem Statement

Retailers face billions of dollars in losses every year due to shoplifting. Traditional theft prevention methods rely heavily on manual observation, which is time-consuming, expensive, and prone to human error. **EyeGuard** addresses these challenges by providing an automated, scalable solution to monitor and detect shoplifting behavior as it happens.

---

## 🎯 Objectives

- 🕒 **Real-Time Detection** – Monitor live camera feeds and identify suspicious activity.
- 🧠 **Behavioral Analysis** – Detect theft-related actions based on learned movement patterns.
- 🚨 **Alert System** – Notify store personnel immediately upon detection.
- 🗂️ **Data Logging** – Record incidents for review and auditing purposes.

---

## ✨ Key Features

- 🎥 **Video Stream Analysis** – Processes surveillance footage to highlight suspicious behavior.
- 🤖 **AI-Powered Detection** – Utilizes Convolutional Neural Networks (CNNs) to recognize theft patterns.
- 💰 **Cost-Effective** – Designed for affordability and scalability.
- 🧍‍♂️ **Behavior Context Awareness** – Differentiates between normal and suspicious actions.

---

## 🧰 Technologies Used

- **Programming Language:** Python  
- **Libraries:** OpenCV, TensorFlow, NumPy  
- **Frameworks:** Keras (model training), Flask (backend integration)  
- **Model Architecture:** Convolutional Neural Networks (CNNs)

---

## ⚙️ How It Works

1. **Input:** Live video feeds from store surveillance cameras.
2. **Preprocessing:** Frames are analyzed using OpenCV for motion detection and object tracking.
3. **Model Prediction:** A trained CNN model analyzes behavior to detect potential theft.
4. **Alert System:** Real-time alerts are sent to the store staff or security.
5. **Logging:** Detected events are stored for later review or auditing.

---

## 🧪 Limitations

- Performance may degrade with poor-quality or low-resolution video.
- Store layout may require configuration or model fine-tuning.
- Sophisticated theft techniques may evade detection.

---

## 🚀 Future Enhancements

- Improve accuracy in crowded or obstructed environments.
- Enable multi-camera system support.
- Add detailed dashboards and analytics tools for prevention strategies.

---

## 🛠️ Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/username/EyeGuard.git
