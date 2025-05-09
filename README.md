yeGuard: AI-Based Shoplifting Detection System
EyeGuard is a smart surveillance solution built to combat retail theft using computer vision and machine learning. It automates the detection of suspicious behavior in real time, helping stores reduce losses and enhance security without the need for constant manual oversight.

🔍 Problem Addressed
Retailers worldwide face substantial financial loss due to shoplifting. Traditional methods—like human monitoring or basic security systems—are often inefficient, costly, and inconsistent. EyeGuard offers a scalable alternative by continuously analyzing surveillance footage and identifying theft-related behavior patterns through AI.

🎯 Key Objectives
Live Detection: Continuously monitors store footage to identify abnormal or suspicious actions.

Smart Behavior Recognition: Detects theft-prone activities using machine-learned patterns.

Instant Alerts: Notifies store personnel or security staff in real-time when suspicious activity occurs.

Incident Tracking: Logs each flagged event for review, analysis, and store audits.

⭐ Key Features
Video Intelligence: Processes video streams and flags risky behavior.

CNN-Powered Detection: Uses Convolutional Neural Networks to learn and identify shoplifting gestures.

Affordable Deployment: Built to be cost-effective and easily integrated into existing systems.

Behavior Awareness: Differentiates between regular browsing and theft-related movements based on context.

🧠 Technology Stack
Programming Language: Python

Libraries: OpenCV, TensorFlow, NumPy

Frameworks: Keras (for model development), Flask (for system integration)

AI Model: Convolutional Neural Networks (CNNs)

⚙️ System Workflow
Input: Receives video feed from store surveillance cameras.

Preprocessing: Frames are processed using OpenCV for motion tracking and behavior analysis.

Prediction: The trained CNN model analyzes movement patterns to detect suspicious activity.

Alert System: Generates real-time alerts for store personnel and logs the event.

⚠️ Current Limitations
May have reduced accuracy in low-resolution or poorly lit environments.

Store-specific adjustments might be needed for different layouts or camera angles.

May not detect well-planned or highly subtle theft attempts.

🚀 Future Improvements
Improve detection in crowded or occluded scenes.

Support integration with a wider network of cameras.

Provide dashboard analytics for prevention and decision-making.

🛠️ How to Set Up
1. Clone the repository:

bash
Copy
Edit
git clone https://github.com/username/EyeGuard.git
2. Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
3. Run the application:

bash
Copy
Edit
python main.py
4. Connect to your store’s camera system and begin live monitoring.

📄 License
This project is licensed under the MIT License. For more information, refer to the LICENSE file included in the repository.
