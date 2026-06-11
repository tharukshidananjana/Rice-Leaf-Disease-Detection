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
# ---- 1. COMPLETE MULTILINGUAL KNOWLEDGE BASE ----
rice_disease_knowledge_base = {
    "Leaf Smut": {
        "en": {"disease_name": "Leaf Smut", "symptoms": "Small, black, raised spots (pustules) appear on older leaves. Leaves turn yellowish and dry prematurely.", "chemical_treatment": "If severe, spray systemic fungicides like Propiconazole 25% EC or Hexaconazole.", "organic_treatment": "Apply balanced nitrogen fertilizer, use wider crop spacing, and spray Neem seed kernel extract."},
        "si": {"disease_name": "කොළ පුස් රෝගය (Leaf Smut)", "symptoms": "පරණ පත්‍ර මත කුඩා, කළු පැහැති, මතුපිටින් ඉස්සුණු ලප (අඟුරු කුඩු වැනි) හටගනී. පත්‍ර කහ පැහැ වී වේලාසනින් වියළී යයි.", "chemical_treatment": "රෝගය දරුණු නම් ප්‍රොපිකොනසෝල් (Propiconazole 25% EC) හෝ හෙක්සකොනසෝල් වැනි පද්ධතිමය දිලීර නාශකයක් යොදන්න.", "organic_treatment": "නයිට්‍රජන් පොහොර සමබරව යොදන්න, පැළ අතර පරතරය නිවැරදිව තබන්න, සහ කොහොඹ ඇට සාරය ඉසින්න්න."},
        "ta": {"disease_name": "இலைக்கரி நோய் (Leaf Smut)", "symptoms": "முதிர்ந்த இலைகளில் சிறிய, கருப்பு நிற, தடித்த புள்ளிகள் (கரித்தூள் போன்ற) தோன்றும். இலைகள் மஞ்சளாகி உதிர்ந்துவிடும்.", "chemical_treatment": "பாதிப்பு அதிகமாக இருந்தால் புரோபிகோனசோல் 25% EC அல்லது ஹெக்சாகோனசோல் பூஞ்சை நாசகத்தை தெளிக்கவும்.", "organic_treatment": "நைட்ரஜன் உரத்தை சீராக இடவும், பயிர்களுக்கு இடையே போதிய இடைவெளி விடவும், வேப்பங்கொட்டை சாறு தெளிக்கவும்."}
    },
    "bacterial_leaf_blight": {
        "en": {"disease_name": "Bacterial Leaf Blight", "symptoms": "Linear yellow to wavy streaks starting from leaf tips/margins, later turning grayish-white with bacterial ooze droplets.", "chemical_treatment": "Copper Hydroxide or Copper Oxychloride. Avoid excess nitrogen (Urea) application completely during infection.", "organic_treatment": "Spray fresh cow dung extract filtered solution (20g/L) or neem-based spray to naturally suppress bacteria."},
        "si": {"disease_name": "බැක්ටීරියා කොළ අංගමාරය (Bacterial Leaf Blight)", "symptoms": "පත්‍ර අගින් හෝ දාරවලින් ඇරඹී දික් අතට විහිදෙන කහ පාට රැලි සහිත ඉරි මතු වේ. පසුව ඒවා අළු-සුදු පැහැයට හැරී වියළී යයි.", "chemical_treatment": "කොපර් හයිඩ්‍රොක්සයිඩ් හෝ කොපර් ඔක්සික්ලෝරයිඩ් යොදන්න. රෝගය පවතින විට යුරියා (නයිට්‍රජන්) යෙදීම සම්පූර්ණයෙන්ම නවත්වන්න.", "organic_treatment": "නැවුම් ගොම දියකර පෙරාගත් දියරය (ලීටරයකට ග්‍රෑම් 20) හෝ කොහොඹ සාරය මිශ්‍රණය ඉසින්න්න."},
        "ta": {"disease_name": "பாக்டீரியா இலை கருகல் நோய் (Bacterial Leaf Blight)", "symptoms": "இலைகளின் நுனி அல்லது ஓரங்களில் தொடங்கி நீளவாக்கில் மஞ்சள் நிற அலை அலையான கோடுகள் தோன்றி, பின்னர் சாம்பல்-வெள்ளை நிறமாக மாறும்.", "chemical_treatment": "காப்பர் ஹைட்ராக்சைடு அல்லது காப்பர் ஆக்ஸிகுளோரைடு பயன்படுத்தவும். நோய் பரவும் போது யூரியா உரமிடுவதை முற்றிலும் தவிர்க்கவும்.", "organic_treatment": "புதிய மாட்டுச் சாணக் கரைசலை (ஒரு லிட்டருக்கு 20 கிராம்) வடிகட்டி தெளிக்கவும் அல்லது வேப்பஞ்சாறு தெளிக்கவும்."}
    },
    "brown_spot": {
        "en": {"disease_name": "Brown Spot", "symptoms": "Oval, dark brown spots with yellow halos across the leaf blades. Often indicates poor soil nutrients or potassium deficiency.", "chemical_treatment": "Spray Mancozeb, Carbendazim, or Edifenphos. Apply Muriate of Potash (MOP) to correct soil deficiency.", "organic_treatment": "Apply well-decomposed compost or farmyard manure to improve soil fertility and plant immunity."},
        "si": {"disease_name": "දුඹුරු ලප රෝගය (Brown Spot)", "symptoms": "පත්‍ර මත වටේට කහ පැහැති රවුමක් (Halo) ඇති, ඕවලාකාර තද දුඹුරු ලප හටගනී. පසෙහි පොටෑසියම් පෝෂක ඌනතාවය නිසා බහුලව ඇතිවේ.", "chemical_treatment": "මැන්කොසෙබ් (Mancozeb) හෝ කාබන්ඩසිම් යොදන්න. පසෙහි පෝෂණය සකස් කිරීමට මියුරියේට් ඔෆ් පොටෑෂ් (MOP) පොහොර යොදන්න.", "organic_treatment": "පසෙහි තත්ත්වය සකස් කිරීමට සහ ශාකයේ ප්‍රතිශක්තිය වැඩි කිරීමට හොඳින් දිරාපත් වූ කොම්පෝස්ට් හෝ කාබනික පොහොර යොදන්න."},
        "ta": {"disease_name": "பழப்பு புள்ளி நோய் (Brown Spot)", "symptoms": "இலைகளில் மஞ்சள் நிற வட்ட வளையத்துடன் கூடிய ஓவல் வடிவ, அடர் பழுப்பு நிற புள்ளிகள் தோன்றும். இது மண்ணில் பொட்டாசியம் சத்துக்குறைபாட்டைக் குறிக்கும்.", "chemical_treatment": "மன்கோசெப் அல்லது கார்பெண்டாசிம் தெளிக்கவும். படத்தின் குறைபாட்டை நீக்க பொட்டாஷ் (MOP) உரத்தைப் பயன்படுத்தவும்.", "organic_treatment": "மண்ணின் வளம் மற்றும் தாவரத்தின் நோய் எதிர்ப்புச் சக்தியை அதிகரிக்க நன்கு மக்கிய மண்புழு உரம் அல்லது தொழுவுரத்தைப் பயன்படுத்தவும்."}
    },
    "healthy": {
        "en": {"disease_name": "Healthy Plant", "symptoms": "Leaves are vibrant green, clean, and free of any spots, lesions, or insect damage. Standing crop is uniform.", "chemical_treatment": "No chemical application needed. Continue standard fertilizer recommendation based on growth stage.", "organic_treatment": "Maintain regular weeding, water management, and apply organic fertilizer/compost to sustain health."},
        "si": {"disease_name": "නිරෝගී වගාව (Healthy)", "symptoms": "පත්‍ර තද කොළ පැහැතිය, පිරිසිදුය. කිසිදු ලපයක්, තුවාලයක් හෝ කෘමි හානියක් නැත. ගොයම් පීදීම ඒකාකාරීව සිදුවේ.", "chemical_treatment": "කිසිදු රසායනික ද්‍රව්‍යයක් අවශ්‍ය නොවේ. වර්ධන අවධිය අනුව සාමාන්‍ය පොහොර නිර්දේශය දිගටම කරගෙන යන්න.", "organic_treatment": "නිසි පරිදි වල් පැලෑටි පාලනය, ජල පාලනය සිදුකරන්න. නිරෝගී බව රැක ගැනීමට කොම්පෝස්ට් හෝ කාබනික දියර පොහොර දිගටම යොදන්න."},
        "ta": {"disease_name": "ஆரோக்கியமான பயிர் (Healthy)", "symptoms": "இலைகள் நல்ல பச்சை நிறமாகவும், புள்ளிகள் அல்லது பூச்சித் தாக்கங்கள் இல்லாமலும் சுத்தமாகக் காணப்படும். பயிர் வளர்ச்சி சீராக இருக்கும்.", "chemical_treatment": "ரசாயனப் பயன்பாடு தேவையில்லை. வளர்ச்சி நிலைக்கு ஏற்ப வழக்கமான உரப் பரிந்துரைகளைத் தொடரவும்.", "organic_treatment": "முறையான களை மேலாண்மை, நீர் மேலாண்மை செய்து, ஆரோக்கியத்தைத் தக்கவைக்க இயற்கை உரம்/காம்போஸ்ட் பயன்படுத்தவும்."}
    },
    "leaf_blast": {
        "en": {"disease_name": "Leaf Blast", "symptoms": "Spindle-shaped (diamond-shaped) lesions with gray centers and dark brown margins on leaves. Can kill entire leaves.", "chemical_treatment": "Spray Tricyclazole 75% WP, Isoprothiolane, or Kasugamycin. Stop nitrogenous fertilizer immediately.", "organic_treatment": "Use blast-resistant varieties, destroy infected crop residues, and spray diluted baking soda mix."},
        "si": {"disease_name": "කොළ පාළුව (Leaf Blast)", "symptoms": "පත්‍ර මත මැද අළු පාට සහ වටේ තද දුඹුරු පාට ඇති, පතිත හැඩැති (Spindle-shaped / දියමන්ති හැඩැති) ලප හටගනී. මුළු පත්‍රයම මැරී යා හැක.", "chemical_treatment": "ට්‍රයිසයික්ලසෝල් (Tricyclazole 75% WP), අයිසොප්‍රොතියොලේන් හෝ කැසුගාමයිසින් යොදන්න. නයිට්‍රජන් පොහොර යෙදීම වහාම නවත්වන්න.", "organic_treatment": "රෝගයට ඔරොත්තු දෙන ප්‍රභේද වගා කරන්න, ආසාදිත බෝග අවශේෂ විනාශ කරන්න, සහ බේකින් සෝඩා දියර මිශ්‍රණය ඉසින්න්න."},
        "ta": {"disease_name": "இலை குலை நோய் (Leaf Blast)", "symptoms": "இலைகளில் நடுவில் சாம்பல் நிறமும் ஓரங்களில் அடர் பழுப்பு நிறமும் கொண்ட கதிர் வடிவிலான (வைர வடிவ) புள்ளிகள் தோன்றும். இலைகள் முற்றிலும் கருகலாம்.", "chemical_treatment": "ட்ரைசைக்ளசோல் 75% WP, ஐசோப்ரோதியோலேன் பூஞ்சை நாசகத்தை தெளிக்கவும். நைட்ரஜன் உரமிடுவதை உடனடியாக நிறுத்தவும்.", "organic_treatment": "நோய் எதிர்ப்புத் திறன் கொண்ட ரகங்களை பயிரிடவும், பாதிக்கப்பட்ட பயிர் கழிவுகளை அழிக்கவும், பேக்கிங் சோடா கரைசல் தெளிக்கவும்."}
    },
    "leaf_scald": {
        "en": {"disease_name": "Leaf Scald", "symptoms": "Large, oblong, chevron-like wavy patterns of alternating light brown and dark brown bands starting from leaf tips or margins.", "chemical_treatment": "Spray Benomyl, Carbendazim, or Thiophanate-methyl if infection spreads rapidly.", "organic_treatment": "Avoid high plant density, ensure proper field drainage, and use clean certified seeds."},
        "si": {"disease_name": "කොළ පිළිස්සීම (Leaf Scald)", "symptoms": "පත්‍ර අගින් හෝ දාරවලින් ඇරඹී, ලා දුඹුරු සහ තද දුඹුරු පැහැති පටි මාරුවෙන් මාරුවට පිහිටන විශාල රැලි සහිත රටා (Chevron patterns) හටගනී.", "chemical_treatment": "රෝගය වේගයෙන් පැතිරෙන්නේ නම් බෙනොමිල් (Benomyl), කාබන්ඩසිම් හෝ තියෝෆනේට්-මෙතිල් වැනි දිලීර නාශකයක් යොදන්න.", "organic_treatment": "පැළ ඝනත්වය අධික ලෙස තැබීමෙන් වළකින්න, කුඹුරේ ජලය හොඳින් බැසයාමට සලස්වන්න, සහ සහතික කළ පිරිසිදු බිත්තර වී භාවිත කරන්න."},
        "ta": {"disease_name": "இலை வெந்த புண் நோய் (Leaf Scald)", "symptoms": "இலை நுனி அல்லது ஓரங்களில் தொடங்கி, வெளிர் பழுப்பு மற்றும் அடர் பழுப்பு நிறப் பட்டைகளுடன் கூடிய பெரிய அலை வடிவ வடிவங்கள் தோன்றும்.", "chemical_treatment": "நோய் வேகமாகப் பரவினால் பெனோமில், கார்பெண்டாசிம் அல்லது தியோபானேட்-மீத்தைல் பூஞ்சை நாசகத்தைப் பயன்படுத்தவும்.", "organic_treatment": "பயிர்களை நெருக்கமாக நடுப்பதைத் தவிர்க்கவும், வயலில் சரியான வடிகால் அமைப்பை உறுதி செய்யவும், சான்றளிக்கப்பட்ட விதைகளைப் பயன்படுத்தவும்."}
    },
    "narrow_brown_spot": {
        "en": {"disease_name": "Narrow Brown Spot", "symptoms": "Short, linear, narrow brown lesions parallel to the leaf veins. Appears mostly during the later growth stages of rice.", "chemical_treatment": "Apply Propiconazole or Benomyl. Ensure proper potassium nutritional status in the soil.", "organic_treatment": "Ensure timely harvesting, crop rotation, and apply organic potassium sources like wood ash to soil."},
        "si": {"disease_name": "පටු දුඹුරු ලප රෝගය (Narrow Brown Spot)", "symptoms": "පත්‍ර නහර වලට සමාන්තරව විහිදෙන කෙටි, දික් අතට පිහිටන පටු දුඹුරු ලප හටගනී. ගොයම් මේරීමේ අවධියේදී බහුලව දක්නට ලැබේ.", "chemical_treatment": "ප්‍රොපිකොනසෝල් (Propiconazole) හෝ බෙනොමිල් යොදන්න. පසෙහි පොටෑසියම් පෝෂණය නිවැරදි මට්ටමක පවතින බව තහවුරු කරගන්න.", "organic_treatment": "නියමිත වේලාවට අස්වනු නෙලන්න, බෝග මාරුව සිදුකරන්න, සහ පසට දර අළු වැනි කාබනික පොටෑසියම් ප්‍රභවයන් එකතු කරන්න."},
        "ta": {"disease_name": "குறுகிய பழுப்பு புள்ளி நோய் (Narrow Brown Spot)", "symptoms": "இலை நரம்புகளுக்கு இணையாக குறுகிய, நீளவாக்கிலான பழுப்பு நிற புள்ளிகள் தோன்றும். இது பயிரின் முதிர்ச்சி நிலையில் அதிகமாகக் காணப்படும்.", "chemical_treatment": "புரோபிகோனசோல் அல்லது பெனோமில் பயன்படுத்தவும். படத்தில் போதிய பொட்டாசியம் சத்து இருப்பதை உறுதி செய்யவும்.", "organic_treatment": "முறையான காலத்தில் அறுவடை செய்யவும், பயிர் சுழற்சி முறையைப் பின்பற்றவும், சாம்பல் போன்ற இயற்கை பொட்டாசியம் உரங்களை இடவும்."}
    },
    "neck_blast": {
        "en": {"disease_name": "Neck Blast", "symptoms": "The neck of the panicle turns grayish-brown and rots, causing the panicle to break. Grains remain empty (whiteheads).", "chemical_treatment": "Apply Tricyclazole or Isoprothiolane immediately at the booting/heading stage before full damage occurs.", "organic_treatment": "Avoid early planting in high-risk seasons, avoid excess urea, and spray bio-control agents like Pseudomonas fluorescens."},
        "si": {"disease_name": "කරටි පාළුව (Neck Blast)", "symptoms": "කරල හටගන්නා කරටිය (Neck) ප්‍රදේශය අළු-දුඹුරු පැහැ වී කුණුවේ. කරල කඩා වැටෙන අතර වී ඇට බොල් වේ (Whiteheads හටගනී).", "chemical_treatment": "ගොයම් මල්වරා ගෙඩි වදින අවධියේදීම ට්‍රයිසයික්ලසෝල් (Tricyclazole) හෝ අයිසොප්‍රොතියොලේන් යොදන්න. හානිය වූ පසු පාලනය අපහසුය.", "organic_treatment": "අධික අවදානම් කාලවලදී කලින් වගා කිරීමෙන් වළකින්න, යුරියා පාලනය කරන්න, සහ සියුඩොමොනාස් (Pseudomonas) වැනි ජෛව පාලන නාශක ඉසින්න."},
        "ta": {"disease_name": "கழுத்து குலை நோய் (Neck Blast)", "symptoms": "கதிர் உருவாகும் கழுத்துப் பகுதி சாம்பல்-பழுப்பு நிறமாக மாறி அழுகும், இதனால் கதிர் உடைந்து விழும். நெல்மணிகள் பதறாகிவிடும்.", "chemical_treatment": "கதிர் வெளிவரும் பருவத்தில் உடனடியாக ட்ரைசைக்ளசோல் அல்லது ஐசோப்ரோதியோலேன் தெளிக்கவும். முழு சேதத்திற்கு பின் கட்டுப்படுத்துவது கடினம்.", "organic_treatment": "அதிக பாதிப்புள்ள காலங்களில் பயிரிடுவதைத் தவிர்க்கவும், சூடோமோனாஸ் போன்ற உயிர் பூஞ்சை நாசகங்களை தெளிக்கவும்."}
    },
    "rice_hispa": {
        "en": {"disease_name": "Rice Hispa (Insect Damage)", "symptoms": "Scraped white parallel lines along the leaf surface caused by adult beetles feeding. Leaves look bleached and wither.", "chemical_treatment": "Spray recommended insecticides like Thiamethoxam, Imidacloprid, or Etofenprox if economic threshold is breached.", "organic_treatment": "Manually collect and destroy beetles, practice leaf-tip clipping before transplanting, and spray Neem oil mix."},
        "si": {"disease_name": "ගොයම් හිස්පා කුරුමිණි හානිය (Rice Hispa)", "symptoms": "වැඩිහිටි කුරුමිණියන් පත්‍ර මතුපිට සූරා කෑම නිසා පත්‍ර දික් අතට සුදු පැහැති ඉරි මෙන් පෙනේ. පසුව කොළ වේලී සුදු පැහැ වේ.", "chemical_treatment": "හානිය අධික නම් තියාමෙතොක්සම් (Thiamethoxam), ඉමිඩක්ලෝප්‍රිඩ් හෝ එටොෆෙන්ප්‍රොක්ස් වැනි කෘමිනාශක යොදන්න.", "organic_treatment": "කුරුමිණියන් අතින් අල්ලා විනාශ කරන්න, පැළ සිටුවීමට පෙර පත්‍ර අගිස්සි කපා දමන්න (බිත්තර ඉවත් කිරීමට), සහ කොහොඹ තෙල් ඉසින්න්න."},
        "ta": {"disease_name": "நெல் ஹிஸ்பா வண்டுத் தாக்குதல் (Rice Hispa)", "symptoms": "வண்டுகள் இலையை சுரண்டி உண்பதால் இலையின் மேற்பரப்பில் நீளவாக்கில் வெள்ளை கோடுகள் தோன்றும். இலைகள் காய்ந்து வெளுத்து காணப்படும்.", "chemical_treatment": "தாக்கம் அதிகமாக இருந்தால் தயாமெதோக்சம், இமிடாக்குளோபிரிட் அல்லது எட்டோஃபென்பிராக்ஸ் போன்ற பூச்சிக்கொல்லிகளை தெளிக்கவும்.", "organic_treatment": "வண்டுகளை கையால் சேகரித்து அழிக்கவும், நாற்று நடும் முன் இலை நுனிகளை நறுக்கவும், வேப்ப எண்ணெய் கரைசல் தெளிக்கவும்."}
    },
    "sheath_blight": {
        "en": {"disease_name": "Sheath Blight", "symptoms": "Greenish-gray, oval or irregular spots on leaf sheaths near water level. Spots have irregular dark brown borders.", "chemical_treatment": "Spray Hexaconazole, Validamycin, or Pencycuron. Avoid dense canopy and maintain proper spacing.", "organic_treatment": "Keep bunds clean, avoid excessive nitrogen, and apply Trichoderma viride bio-fungicide to the base."},
        "si": {"disease_name": "කොපු අංගමාරය (Sheath Blight)", "symptoms": "ජල මට්ටමට ආසන්නව ඇති පත්‍ර කොපු මත කොළ-අළු පැහැති, ඕවලාකාර ලප හටගනී. ලප වටා තද දුඹුරු පැහැති දාර පවතී.", "chemical_treatment": "හෙක්සකොනසෝල් (Hexaconazole), වැලිඩාමයිසින් හෝ පෙන්සිකියුරෝන් යොදන්න. පඳුරු ඝනත්වය අධික වීම වළක්වන්න.", "organic_treatment": "නියරවල් පිරිසිදුව තබාගන්න, යුරියා භාවිතය සීමා කරන්න, සහ පඳුර පාමුලට ට්‍රයිකොඩර්මා (Trichoderma) ජෛව නාශක යොදන්න."},
        "ta": {"disease_name": "உறை கருகல் நோய் (Sheath Blight)", "symptoms": "நீர்மட்டத்திற்கு அருகில் உள்ள இலை உறைகளில் பச்சை-சாம்பல் நிற ஓவல் வடிவ புள்ளிகள் தோன்றும். புள்ளிகளின் ஓரங்கள் அடர் பழுப்பு நிறத்தில் இருக்கும்.", "chemical_treatment": "ஹெக்சாகோனசோல், வாலிடாமைசின் அல்லது பென்சிகுரான் தெளிக்கவும். பயிர்கள் நெருக்கமாக வளர்வதைத் தவிர்க்கவும்.", "organic_treatment": "வரப்புகளை சுத்தமாக வைத்திருக்கவும், அதிகப்படியான நைட்ரஜன் உரத்தைத் தவிர்க்கவும், ட்ரைக்கோடெர்மா உயிர் உரத்தை வேர்ப்பகுதியில் இடவும்."}
    },
    "tungro": {
        "en": {"disease_name": "Tungro Virus Disease", "symptoms": "Plants are severely stunted. Leaves turn yellow to orange starting from tips. Interveinal chlorosis on young leaves.", "chemical_treatment": "No direct cure for virus. Control the vector (Green Leafhopper) using Imidacloprid or Thiamethoxam.", "organic_treatment": "Uproot and burn infected plants immediately. Use resistant varieties and use yellow sticky traps for leafhoppers."},
        "si": {"disease_name": "ටුංග්‍රෝ වෛරස් රෝගය (Tungro)", "symptoms": "ගොයම් පඳුරු වර්ධනය බාල වී මිටි වේ. පත්‍ර අගින් ඇරඹී මුළු පත්‍රයම කහ හෝ තැඹිලි පාට වේ. ලාබාල පත්‍රවල නහර අතර කහ වීම දක්නට ලැබේ.", "chemical_treatment": "වෛරසයට ඍජු පිළියම් නැත. රෝගය පතුරුවන 'කොළ පැහැති පත්‍ර පැනිකිළියා' (Green Leafhopper) මර්දනයට ඉමිඩක්ලෝප්‍රිඩ් හෝ තියාමෙතොක්සම් යොදන්න.", "organic_treatment": "ආසාදිත පඳුරු වහාම උදුරා පුළුස්සා දමන්න. රෝගයට ඔරොත්තු දෙන ප්‍රභේද වගා කරන්න. පැනිකිළියන් ඇල්ලීමට කහ පාට ඇලෙන සුළු උගුල් පාවිච්චි කරන්න."},
        "ta": {"disease_name": "துங்ரோ வைரஸ் நோய் (Tungro)", "symptoms": "பயிர்கள் கடுமையாக குன்றி குட்டையாகக் காணப்படும். இலை நுனிகள் மஞ்சள் அல்லது ஆரஞ்சு நிறமாக மாறும். இளம் இலைகளின் நரம்புகள் வெளுத்துக் காணப்படும்.", "chemical_treatment": "வைரஸுக்கு நேரடி மருந்து இல்லை. நோயைப் பரப்பும் 'பச்சை இலைத் தத்துப்பூச்சியை' கட்டுப்படுத்த இமிடாக்குளோபிரிட் அல்லது தயாமெதோக்சம் தெளிக்கவும்.", "organic_treatment": "பாதிக்கப்பட்ட பயிர்களை உடனடியாக வேரோடு பிடுங்கி அழிக்கவும். மஞ்சள் ஒட்டும் பொறிகளைப் பயன்படுத்தி தத்துப்பூச்சிகளைக் கட்டுப்படுத்தவும்."}
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