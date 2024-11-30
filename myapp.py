#Designed by Joshua Igbinedion
#Intern ID : IN9240822

import streamlit as st
from PIL import Image
import pyttsx3
import os
import pytesseract  
import google.generativeai as genai

# Configure Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set up Google Generative AI with API Key
GEMINI_API_KEY = "Your API Key"  # Insert your valid API key here
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# Initialize Text-to-Speech engine
tts_engine = pyttsx3.init()

# Streamlit page configuration
st.markdown(
    """
    <style>
     .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #0662f6;
        margin-top: -20px;
     }
    .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-header {
        font-size: 24px;
        color: #333;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">VisionAid</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI for Scene Understanding, Text Extraction & Speech for the Visually Impaired 🗣️</div>', unsafe_allow_html=True)

# Sidebar Features
st.sidebar.image(
    r"C:\Users\hp\Desktop\INNOMATICS\GenAi\Python code reviewer\image.png",
    width=250
)

# About Section in Sidebar
st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
    📌 **Features**
    - 🔍 **Scene Description**: AI insights about the image, including objects and suggestions.
    - 📝 **Text Extraction**: Use OCR to extract visible text.
    - 🔊 **Text-to-Speech**: Listen to the extracted text.

    💡 **Benefits**:
    Aids visually impaired users by providing scene descriptions, extracting text, and offering speech output.

    🤖 **Technology Used**:
    - **Google Gemini API** for scene analysis.
    - **Tesseract OCR** for text recognition.
    - **pyttsx3** for voice output.
    """
)

# Instructions Text Area in Sidebar
st.sidebar.text_area("📜 Instructions", "Upload an image to begin. Select a feature to use: 1 Describe Scene, 2 Extract Text, 3 Listen")

# Function Definitions
def extract_text(image):
    """Extracts text from an image using OCR."""
    return pytesseract.image_to_string(image)

def speak_text(text):
    """Converts the provided text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def describe_scene(prompt, image_data):
    """Generates a description of the scene using Google Generative AI."""
    
    # Initialize GenerativeModel without model argument if not needed
    model = genai.GenerativeModel(api_key=GEMINI_API_KEY)  # Adjust as per documentation
    
    response = model.generate_content([prompt, image_data[0]])
    
    return response.text

def prepare_uploaded_image(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    
    raise FileNotFoundError("No file uploaded.")

# Image Upload Section
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or select an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

# Feature Buttons Section
st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

describe_button = col1.button("🔍 Describe Scene")
extract_button = col2.button("📝 Extract Text")
speak_button = col3.button("🔊 Text-to-Speech")

# Input Prompt for Scene Understanding
scene_prompt = """
You are an AI assistant aiding visually impaired individuals by describing the scene in the image. Provide:
1. A list of detected items and their purposes.
2. A general description of the image.
3. Suggestions for actions or precautions for visually impaired users.
"""

# Process User Interactions
if uploaded_file:
    image_data = prepare_uploaded_image(uploaded_file)

    if describe_button:
        with st.spinner("Generating scene description..."):
            description = describe_scene(scene_prompt, image_data)
            st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
            st.write(description)

    if extract_button:
        with st.spinner("Extracting text from the image..."):
            extracted_text = extract_text(img)
            st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", extracted_text, height=150)

    if speak_button:
        with st.spinner("Converting text to speech..."):
            extracted_text = extract_text(img)
            if extracted_text.strip():
                speak_text(extracted_text)
                st.success("✅ Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text found to convert.")

# Footer Section
st.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Google Gemini API</strong> | Built and designed by Joshua Igbinedion with Streamlit</p>
    </footer>
    """,
   unsafe_allow_html=True,
)

st.sidebar.markdown(
   """
   <hr>
   <footer style="text-align:center;">
       <p>Powered by <strong>Google Gemini API</strong> | Built and designed by Joshua Igbinedion with Streamlit</p>
   </footer>
   """,
   unsafe_allow_html=True,
)