import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def load_llm():

    api_key = os.getenv("GOOGLE_API_KEY")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    return model

