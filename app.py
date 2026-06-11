import streamlit as st
import tensorflow as tf
import cv2
import numpy as np
import os
import folium
from streamlit_folium import st_folium
from gtts import gTTS
import base64

# Page Configuration
st.set_page_config(page_title="Rice Leaf Disease Intelligence Hub", layout="wide")

# ---- 0. MULTILINGUAL UI LABELS DICTIONARY ----
ui_labels = {
    "en": {
        "main_title": "🌾 Rice Leaf Disease Smart Diagnostic Hub",
        "sub_title": "An Advanced Multilingual AI Platform for Paddy Farmers",
        "upload_text": "📸 Upload Rice Leaf Image...",
        "title": "Info", 
        "symptoms": "Symptoms", 
        "chemical": "Chemical Solution", 
        "organic": "Organic Solution",
        "listen": "Listen to Instructions",
        "map_title": "🗺️ Nearby Agrarian Services & Fertilizer Stores",
        "map_desc": "Showing closest support hubs for input coordinates:"
    },
    "si": {
        "main_title": "🌾 ගොයම් කොළ රෝග හඳුනා ගැනීමේ ස්මාර්ට් මධ්‍යස්ථානය",
        "sub_title": "ගොවීන් සඳහා වූ උසස් බහුභාෂා කෘෂි AI වේදිකාව",
        "upload_text": "📸 ගොයම් කොළයේ පින්තූරයක් උඩුගත කරන්න...",
        "title": "තොරතුරු", 
        "symptoms": "රෝග ලක්ෂණ", 
        "chemical": "රසායනික පිළියම්", 
        "organic": "කාබනික පිළියම්",
        "listen": "උපදෙස්වලට සවන් දෙන්න",
        "map_title": "🗺️ අසල ඇති කෘෂිකර්ම සේවා සහ පොහොර ගබඩා",
        "map_desc": "ඔබේ කුඹුරට ආසන්නතම සේවා මධ්‍යස්ථාන:"
    },
    "ta": {
        "main_title": "🌾 நெல் இலை நோய் கண்டறியும் ஸ்மார்ட் மையம்",
        "sub_title": "விவசாயிகளுக்கான மேம்பட்ட பன்மொழி AI தளம்",
        "upload_text": "📸 நெல் இலை படத்தை பதிவேற்றவும்...",
        "title": "தகவல்", 
        "symptoms": "அறிகுறிகள்", 
        "chemical": "இரசாயன தீர்வு", 
        "organic": "இயற்கை தீர்வு",
        "listen": "வழிமுறைகளைக் கேட்கவும்",
        "map_title": "🗺️ அருகிலுள்ள விவசாய சேவைகள் மற்றும் உரக் கடைகள்",
        "map_desc": "அருகிலுள்ள சேவை மையங்களைக் காண்பிக்கிறது:"
    }
}

# ---- 1. KNOWLEDGE BASE ----
rice_disease_knowledge_base = {
    "Leaf Smut": {
        "en": {"disease_name": "Leaf Smut", "symptoms": "Small, black, raised spots.", "chemical_treatment": "Propiconazole.", "organic_treatment": "Neem extract."},
        "si": {"disease_name": "කොළ පුස් රෝගය", "symptoms": "කුඩා කළු ලප.", "chemical_treatment": "ප්‍රොපිකොනසෝල්.", "organic_treatment": "කොහොඹ සාරය."},
        "ta": {"disease_name": "இலைக்கரி நோய்", "symptoms": "கருப்பு புள்ளிகள்.", "chemical_treatment": "புரோபிகோனசோல்.", "organic_treatment": "வேப்பஞ்சாறு."}
    },
    "bacterial_leaf_blight": {
        "en": {"disease_name": "Bacterial Leaf Blight", "symptoms": "Yellow streaks.", "chemical_treatment": "Copper Hydroxide.", "organic_treatment": "Cow dung extract."},
        "si": {"disease_name": "බැක්ටීරියා කොළ අංගමාරය", "symptoms": "කහ පාට ඉරි.", "chemical_treatment": "කොපර් හයිඩ්‍රොක්සයිඩ්.", "organic_treatment": "ගොම දියර."},
        "ta": {"disease_name": "பாக்டீரியா இலை கருகல்", "symptoms": "மஞ்சள் கோடுகள்.", "chemical_treatment": "காப்பர் ஹைட்ராக்சைடு.", "organic_treatment": "மாட்டுச் சாணக் கரைசல்."}
    },
    "brown_spot": {
        "en": {"disease_name": "Brown Spot", "symptoms": "Dark brown spots.", "chemical_treatment": "Mancozeb.", "organic_treatment": "Compost."},
        "si": {"disease_name": "දුඹුරු ලප රෝගය", "symptoms": "දුඹුරු ලප.", "chemical_treatment": "මැන්කොසෙබ්.", "organic_treatment": "කොම්පෝස්ට්."},
        "ta": {"disease_name": "பழப்பு புள்ளி நோய்", "symptoms": "பழுப்பு புள்ளிகள்.", "chemical_treatment": "மன்கோசெப்.", "organic_treatment": "மண்புழு உரம்."}
    },
    "healthy": {
        "en": {"disease_name": "Healthy Plant", "symptoms": "No issues.", "chemical_treatment": "None.", "organic_treatment": "Regular maintenance."},
        "si": {"disease_name": "නිරෝගී වගාව", "symptoms": "කිසිදු රෝගයක් නැත.", "chemical_treatment": "අවශ්‍ය නොවේ.", "organic_treatment": "සාමාන්‍ය පාලනය."},
        "ta": {"disease_name": "ஆரோக்கியமான பயிர்", "symptoms": "பிரச்சனை இல்லை.", "chemical_treatment": "தேவையில்லை.", "organic_treatment": "சாதாரண பராமரிப்பு."}
    },
    "leaf_blast": {
        "en": {"disease_name": "Leaf Blast", "symptoms": "Diamond-shaped lesions.", "chemical_treatment": "Tricyclazole.", "organic_treatment": "Resistant varieties."},
        "si": {"disease_name": "කොළ පාළුව", "symptoms": "දියමන්ති හැඩැති ලප.", "chemical_treatment": "ට්‍රයිසයික්ලසෝල්.", "organic_treatment": "ඔරොත්තු දෙන ප්‍රභේද."},
        "ta": {"disease_name": "இலை குலை நோய்", "symptoms": "வைர வடிவ புள்ளிகள்.", "chemical_treatment": "ட்ரைசைக்ளசோல்.", "organic_treatment": "நோய் எதிர்ப்பு ரகங்கள்."}
    },
    "leaf_scald": {
        "en": {"disease_name": "Leaf Scald", "symptoms": "Wavy patterns.", "chemical_treatment": "Benomyl.", "organic_treatment": "Proper drainage."},
        "si": {"disease_name": "කොළ පිළිස්සීම", "symptoms": "රැලි සහිත රටා.", "chemical_treatment": "බෙනොමිල්.", "organic_treatment": "ජල පාලනය."},
        "ta": {"disease_name": "இலை வெந்த புண் நோய்", "symptoms": "அலை வடிவங்கள்.", "chemical_treatment": "பெனோமில்.", "organic_treatment": "நீர் மேலாண்மை."}
    },
    "narrow_brown_spot": {
        "en": {"disease_name": "Narrow Brown Spot", "symptoms": "Linear brown lesions.", "chemical_treatment": "Propiconazole.", "organic_treatment": "Wood ash."},
        "si": {"disease_name": "පටු දුඹුරු ලප රෝගය", "symptoms": "දික් අතට ලප.", "chemical_treatment": "ප්‍රොපිකොනසෝල්.", "organic_treatment": "දර අළු."},
        "ta": {"disease_name": "குறுகிய பழுப்பு புள்ளி நோய்", "symptoms": "நீளவாக்கிலான புள்ளிகள்.", "chemical_treatment": "புரோபிகோனசோல்.", "organic_treatment": "சாம்பல்."}
    },
    "neck_blast": {
        "en": {"disease_name": "Neck Blast", "symptoms": "Neck rot.", "chemical_treatment": "Tricyclazole.", "organic_treatment": "Pseudomonas."},
        "si": {"disease_name": "කරටි පාළුව", "symptoms": "කරටිය කුණුවීම.", "chemical_treatment": "ට්‍රයිසයික්ලසෝල්.", "organic_treatment": "සියුඩොමොනාස්."},
        "ta": {"disease_name": "கழுத்து குலை நோய்", "symptoms": "கழுத்து அழுகல்.", "chemical_treatment": "ட்ரைசைக்ளசோல்.", "organic_treatment": "சூடோமோனாஸ்."}
    },
    "rice_hispa": {
        "en": {"disease_name": "Rice Hispa", "symptoms": "Scraped white lines.", "chemical_treatment": "Thiamethoxam.", "organic_treatment": "Manual removal."},
        "si": {"disease_name": "ගොයම් හිස්පා", "symptoms": "සුදු ඉරි.", "chemical_treatment": "තියාමෙතොක්සම්.", "organic_treatment": "අතින් ඉවත් කිරීම."},
        "ta": {"disease_name": "நெல் ஹிஸ்பா", "symptoms": "வெள்ளை கோடுகள்.", "chemical_treatment": "தயாமெதோக்சம்.", "organic_treatment": "கையால் அகற்றுதல்."}
    },
    "sheath_blight": {
        "en": {"disease_name": "Sheath Blight", "symptoms": "Oval spots.", "chemical_treatment": "Hexaconazole.", "organic_treatment": "Trichoderma."},
        "si": {"disease_name": "කොපු අංගමාරය", "symptoms": "ඕවලාකාර ලප.", "chemical_treatment": "හෙක්සකොනසෝල්.", "organic_treatment": "ට්‍රයිකොඩර්මා."},
        "ta": {"disease_name": "உறை கருகல் நோய்", "symptoms": "ஓவல் புள்ளிகள்.", "chemical_treatment": "ஹெக்சாகோனசோல்.", "organic_treatment": "ட்ரைக்கோடெர்மா."}
    },
    "tungro": {
        "en": {"disease_name": "Tungro", "symptoms": "Stunted plants.", "chemical_treatment": "Control hoppers.", "organic_treatment": "Burn infected plants."},
        "si": {"disease_name": "ටුංග්‍රෝ", "symptoms": "මිටි වීම.", "chemical_treatment": "කෘමීන් පාලනය.", "organic_treatment": "උදුරා දැමීම."},
        "ta": {"disease_name": "துங்ரோ", "symptoms": "குட்டையாகுதல்.", "chemical_treatment": "பூச்சிக் கட்டுப்பாடு.", "organic_treatment": "பிடுங்கி அழித்தல்."}
    }
}

class_mapping = {
    0: "bacterial_leaf_blight", 1: "brown_spot", 2: "healthy", 3: "Leaf Smut",
    4: "leaf_blast", 5: "leaf_scald", 6: "narrow_brown_spot", 7: "neck_blast",
    8: "rice_hispa", 9: "sheath_blight", 10: "tungro"
}

# ---- 2. LOAD MODEL ----
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('rice_leaf_disease_model.keras')

model = load_model()

# ---- 3. SEVERITY & AUDIO LOGIC ----
def calculate_severity(img_bytes):
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    infected_mask = cv2.inRange(hsv, np.array([10, 40, 40]), np.array([30, 255, 255]))
    severity = (cv2.countNonZero(infected_mask) / (img.shape[0] * img.shape[1])) * 100
    return round(severity, 2)

def play_audio_text(text, lang_code):
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)

# ---- 4. UI DISPLAY ----
lang_choice = st.sidebar.selectbox("🌐 Select Language / භාෂාව තෝරන්න / மொழி தேர்வு", ["English", "සිංහල", "தமிழ்"])
selected_lang = {"English": "en", "සිංහල": "si", "தமிழ்": "ta"}[lang_choice]
labels = ui_labels[selected_lang]

st.title(labels["main_title"])
st.write(labels["sub_title"])

uploaded_file = st.file_uploader(labels["upload_text"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    st.image(uploaded_file, width=300)
    
    img = cv2.resize(cv2.imdecode(np.frombuffer(file_bytes, np.uint8), 1), (224, 224)) / 255.0
    pred = class_mapping[np.argmax(model.predict(np.expand_dims(img, axis=0)))]
    info = rice_disease_knowledge_base[pred][selected_lang]
    
    st.subheader(f"🔍 {labels['title']}: {info['disease_name']}")
    st.write(f"**{labels['symptoms']}:** {info['symptoms']}")
    st.write(f"**{labels['chemical']}:** {info['chemical_treatment']}")
    st.write(f"**{labels['organic']}:** {info['organic_treatment']}")
    
    if st.button(f"🔊 {labels['listen']}"):
        play_audio_text(f"{info['disease_name']}. {info['symptoms']}", selected_lang)

    st.write("---")
    st.subheader(labels["map_title"])
    st.write(labels["map_desc"])
    
    m = folium.Map(location=[8.7542, 80.4982], zoom_start=12)
    st_folium(m, width=800, height=300)