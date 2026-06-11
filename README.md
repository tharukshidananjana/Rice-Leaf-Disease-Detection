🌾 Rice Leaf Disease Smart Diagnostic Hub
This project is an advanced AI-powered platform designed to assist paddy farmers in identifying rice leaf diseases accurately. By leveraging deep learning and image processing, it provides instant diagnosis, severity analysis, and localized agricultural support.

Live Link : [https://rice-leaf-disease-detection1.streamlit.app/](url)

🌟 Key Features
AI-Powered Diagnosis: Instantly detects 11 different rice leaf diseases using a trained TensorFlow model.

Severity Analysis: Calculates and displays the infection percentage using image processing techniques.

Multilingual Support: Fully supports English, Sinhala, and Tamil for a user-friendly experience.

Localized Assistance: Integrated map showing nearby agricultural support hubs and fertilizer stores.

Audio Instructions: Converts diagnostic results into audio for easy accessibility.

🛠 Tech Stack & Tools
Frontend: Streamlit

AI/ML: TensorFlow, Keras (CNN Model)

Image Processing: OpenCV, NumPy

Geospatial: Folium, Streamlit-Folium

Audio Synthesis: gTTS (Google Text-to-Speech)

Programming Language: Python

🚀 How It Works
Upload: The user uploads a photo of a rice leaf through the interface.

Process: The model analyzes the image to classify the disease.

Severity: OpenCV calculates the severity of the infection.

Actionable Advice: The system provides chemical and organic treatment methods based on the identified disease.

Support: Displays the nearest service centers via an interactive map.

📂 Project Structure
Plaintext


├── app.py                 # Main Streamlit application

├── rice_leaf_disease_model.keras  # Trained AI model

├── requirements.txt       # Project dependencies

└── README.md              # Project documentation
