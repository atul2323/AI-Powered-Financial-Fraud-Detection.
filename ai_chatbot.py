import streamlit as st
import google.genai as genai
from google.genai import types

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

def chatbot_response(prompt):

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction="You are an AI Fraud Detection Assistant. Help users understand fraud detection, phishing websites, suspicious UPI IDs, QR frauds, transaction fraud, and cybersecurity."
    )
)

return response.text
