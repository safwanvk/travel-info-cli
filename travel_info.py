import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

# -----------------------------
# Initialize Gemini Client
# -----------------------------
client = genai.Client()