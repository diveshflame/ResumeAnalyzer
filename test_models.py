#!/usr/bin/env python3
"""
Quick script to find which Gemini model works with your API key
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

client = genai.Client(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash-002",
    "gemini-1.5-flash",
    "gemini-1.5-pro-002", 
    "gemini-1.5-pro",
    "gemini-pro",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
]

print("Testing available models...\n")

working_model = None
for model in models_to_test:
    try:
        print(f"Testing: {model}...", end=" ")
        response = client.models.generate_content(
            model=model,
            contents="Hello"
        )
        print(f"✅ WORKS!")
        working_model = model
        break
    except Exception as e:
        print(f"❌ Failed")

if working_model:
    print(f"\n✅ Use this model in app.py: {working_model}")
else:
    print("\n❌ No working models found. Check your API key.")