import streamlit as st
import os
import requests
import json
from dotenv import load_dotenv
import pyttsx3
from duckduckgo_search import DDGS as DuckDuckGoSearch
from PIL import Image
from io import BytesIO
import speech_recognition as sr

# Load .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Streamlit UI
st.set_page_config(page_title="AI Tutor for Kids", page_icon="🎓")
st.title("👧📚 AI Tutor for Kids")
st.write("Ask me anything! I'll explain it in a fun way and show pictures too!")

question = st.text_input("👶 What do you want to learn about?")

# Get Image
def get_image(query):
    try:
        with DuckDuckGoSearch() as search:
            results = search.images(query, max_results=1)
            if results:
                url = results[0]["image"]
                img_data = requests.get(url).content
                return Image.open(BytesIO(img_data))
    except:
        return None

# Speak Function
engine = pyttsx3.init()

# On question input
if question:
    with st.spinner("Thinking..."):
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "http://localhost:8501",
                "Content-Type": "application/json",
            }

            data = {
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are a fun and friendly AI tutor for a 6-year-old. Explain in a very simple and playful way."},
                    {"role": "user", "content": question}
                ]
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )

            result = response.json()
            answer = result["choices"][0]["message"]["content"]

            st.success("Here's the answer:")
            st.write(answer)

            engine.say(answer)
            engine.runAndWait()

            img = get_image(question)
            if img:
                st.image(img, caption="Here's a picture to help you learn!")
            else:
                st.warning("Couldn't find a picture.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

