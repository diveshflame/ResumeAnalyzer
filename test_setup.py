#!/usr/bin/env python3
"""
Minimal Setup Checker
"""

import sys
import os

def test_python_version():
    version = sys.version_info
    return version.major == 3 and version.minor >= 8

def test_dependencies():
    required_packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'fitz': 'PyMuPDF',
        'google.genai': 'google-genai',
        'dotenv': 'python-dotenv'
    }

    all_installed = True

    for package in required_packages.keys():
        try:
            __import__(package)
        except ImportError:
            all_installed = False

    return all_installed

def test_file_structure():
    required_files = [
        "app.py",
        "index.html",
        "styles.css",
        "script.js",
        "requirements.txt"
    ]

    return all(os.path.exists(f) for f in required_files)

def test_env_config():
    if not os.path.exists(".env"):
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        return api_key and api_key.strip() != "" and "your_gemini_api_key_here" not in api_key
    except:
        return False


# NEW: Test if the API key actually works
def test_gemini_api():
    try:
        from dotenv import load_dotenv
        from google import genai
        from google.genai import types

        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            return False

        client = genai.Client(api_key=api_key)

        # Minimal request — fastest and safest
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text="ping")]
            )
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contents
        )

        return bool(response.text.strip())
    
    except:
        return False


def print_result(label, result):
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{label:.<30} {status}")


def main():
    print("=" * 50)

    py_ok = test_python_version()
    dep_ok = test_dependencies()
    files_ok = test_file_structure()
    env_ok = test_env_config()
    api_ok = test_gemini_api()

    print_result("Python Version", py_ok)
    print_result("Dependencies", dep_ok)
    print_result("File Structure", files_ok)
    print_result("Environment Config", env_ok)
    print_result("Gemini API Key Test", api_ok)

    print("=" * 50)


if __name__ == "__main__":
    main()
