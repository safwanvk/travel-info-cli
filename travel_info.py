import os
import sys
import json
import time
import re
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
client = genai.Client(api_key=API_KEY)

# -----------------------------
# CLI argument handling
# -----------------------------
if len(sys.argv) != 3:
    print('Usage: python travel_info.py "Place Name" leisure|business')
    sys.exit(1)

place = sys.argv[1]
purpose = sys.argv[2].lower()

if purpose not in {"leisure", "business"}:
    print("Purpose must be either 'leisure' or 'business'")
    sys.exit(1)

# -----------------------------
# Prompt template
# -----------------------------
PROMPT_TEMPLATE = """
You are a travel information generator.

Return ONLY valid JSON.
Do NOT include explanations, markdown, or extra text.

Generate a structured travel overview for:
Place: "{place}"
Purpose: "{purpose}" (leisure or business)

Rules:
- Overview: 3–5 concise bullet points, tailored to the purpose.
- Use clear, factual language. Keep bullets concise (max 15 words each).
- Avoid repetitive phrasing.
- Ensure valid JSON only.
- No emojis.
- No trailing commas.

JSON format:
{{
  "place": "{place}",
  "purpose": "{purpose}",
  "overview": [],
  "things_to_know": [],
  "nearby_transport": [],
  "how_to_get_there": "",
  "best_time_to_travel": ""
}}
"""

prompt = PROMPT_TEMPLATE.format(place=place, purpose=purpose)

# -----------------------------
# Model priority (fallback)
# -----------------------------
MODEL_PRIORITY = [
    "gemini-2.5-flash",  # Free-tier compatible
    # "gemini-2.5-pro"   # Paid / higher quality (optional fallback)
]

# -----------------------------
# JSON helpers
# -----------------------------
def extract_json(text: str) -> dict:
    """Safely extract first JSON object from model output using regex."""
    match = re.search(r"{.*}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model output")
    return json.loads(match.group())

def normalize_text(data: dict) -> dict:
    """Trim whitespace in lists."""
    for key in ["overview", "things_to_know", "nearby_transport"]:
        if key in data and isinstance(data[key], list):
            data[key] = [item.strip() for item in data[key]]
    return data

# -----------------------------
# Generate JSON with retries and quota handling
# -----------------------------
def generate_json_with_retry(prompt: str, retries: int = 3, wait: int = 30) -> dict:
    last_error = None
    for model_name in MODEL_PRIORITY:
        for attempt in range(1, retries + 1):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=800,
                    ),
                )
                text = response.text.strip()
                # Remove markdown code fences if present
                text = text.lstrip("```json").rstrip("```").strip()
                return extract_json(text)

            except Exception as e:
                last_error = e
                # Check for quota errors and wait if necessary
                if "RESOURCE_EXHAUSTED" in str(e):
                    print(f"Quota exceeded. Retrying in {wait} seconds...")
                    time.sleep(wait)
                    continue
                # Minor pause between retries
                time.sleep(2)
    raise RuntimeError(f"Failed to generate valid JSON after retries: {last_error}")

# -----------------------------
# Run
# -----------------------------
try:
    parsed = generate_json_with_retry(prompt)
    parsed = normalize_text(parsed)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
except Exception as e:
    print("Error:", str(e))
    sys.exit(1)