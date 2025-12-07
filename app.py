from flask import Flask, request, jsonify, send_from_directory
import fitz  # PyMuPDF
from flask_cors import CORS
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# === CONFIGURE GOOGLE AI CLIENT ===
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("=" * 60)
    print("WARNING: GEMINI_API_KEY not set!")
    print("=" * 60)
    print("Please follow these steps:")
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Add it to your .env file as: GEMINI_API_KEY=your_key_here")
    print("=" * 60)
    client = None
else:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("✅ Gemini API client initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing Gemini client: {e}")
        client = None


# === UTILITY: Extract text ===

def extract_text(file):
    """Extract text from PDF or TXT file"""
    if file.filename.endswith('.pdf'):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif file.filename.endswith('.txt'):
        return file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file type. Upload PDF or TXT.")


# === GOOGLE AI ANALYSIS ===

def analyze_with_gemini(resume_text, job_text):
    """Use Gemini API to analyze resume vs job description (single model, stable)."""

    if not client:
        raise Exception("Google AI client not initialized. Please set GEMINI_API_KEY in .env file.")

    MODEL_NAME = "gemini-2.5-flash-lite"  # ✅ SAME MODEL AS TEST SETUP
    print(f"Using model: {MODEL_NAME}")

    prompt = f"""You are an expert ATS (Applicant Tracking System) resume analyzer.

Analyze the following resume and job description and return JSON strictly in this format:

{{
  "match_score": <0-100>,
  "matched_keywords": [],
  "missing_keywords": [],
  "technical_skills_present": [],
  "technical_skills_missing": [],
  "soft_skills_present": [],
  "soft_skills_missing": [],
  "detailed_feedback": {{
    "overall_assessment": "",
    "strengths": [],
    "weaknesses": [],
    "recommendations": [],
    "ats_compatibility": "",
    "section_analysis": {{
      "has_contact_info": true,
      "has_experience": true,
      "has_education": true,
      "has_skills_section": true,
      "has_quantifiable_achievements": true
    }}
  }},
  "priority_improvements": []
}}

JOB DESCRIPTION:
{job_text}

RESUME:
{resume_text}
"""

    try:
        # SDK v1beta format
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=prompt)]
            )
        ]

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )

        response_text = response.text.strip()

        # --- Cleanup JSON ---
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        else:
            json_text = response_text

        return json.loads(json_text)

    except json.JSONDecodeError as e:
        raise Exception(f"Gemini returned invalid JSON: {e}\nRaw response:\n{response_text}")

    except Exception as e:
        msg = str(e)

        if "429" in msg:
            raise Exception("❌ Gemini API quota exceeded. Wait or upgrade your plan.")
        if "403" in msg:
            raise Exception("❌ API Key rejected. Check if the key belongs to the correct Cloud Project.")
        if "404" in msg:
            raise Exception("❌ Model name not found. Use gemini-2.0-flash only.")

        raise


# === FORMAT FEEDBACK ===

def format_feedback(analysis):
    feedback_lines = []

    score = analysis.get("match_score", 0)
    if score >= 80:
        feedback_lines.append("🎯 EXCELLENT MATCH! Your resume aligns very well with this job description.")
    elif score >= 60:
        feedback_lines.append("✅ GOOD MATCH! Your resume shows strong alignment with several key requirements.")
    elif score >= 40:
        feedback_lines.append("⚠️ MODERATE MATCH. Your resume has some relevant qualifications but needs improvement.")
    else:
        feedback_lines.append("❌ LOW MATCH. Significant gaps exist between your resume and job requirements.")

    detailed = analysis.get("detailed_feedback", {})
    if detailed.get("overall_assessment"):
        feedback_lines.append(f"\n{detailed['overall_assessment']}")

    feedback_lines.append(f"\n📊 Match Score: {score}%")

    # Section analysis
    section_analysis = detailed.get("section_analysis", {})
    if section_analysis:
        feedback_lines.append("\n📋 RESUME STRUCTURE ANALYSIS:")
        missing = []

        if not section_analysis.get("has_contact_info"): missing.append("Contact Info")
        if not section_analysis.get("has_experience"): missing.append("Experience")
        if not section_analysis.get("has_education"): missing.append("Education")
        if not section_analysis.get("has_skills_section"): missing.append("Skills")

        if missing:
            feedback_lines.append(f"❌ Missing sections: {', '.join(missing)}")
        else:
            feedback_lines.append("✅ All essential sections present")

        if section_analysis.get("has_quantifiable_achievements"):
            feedback_lines.append("✅ Contains quantifiable achievements")
        else:
            feedback_lines.append("⚠️ Add more quantifiable achievements (numbers, percentages)")

    # Missing keywords
    missing_keywords = analysis.get("missing_keywords", [])
    tech_missing = analysis.get("technical_skills_missing", [])
    soft_missing = analysis.get("soft_skills_missing", [])

    if missing_keywords or tech_missing or soft_missing:
        total_missing = len(missing_keywords) + len(tech_missing) + len(soft_missing)
        feedback_lines.append(f"\n🔍 MISSING KEYWORDS & SKILLS ({total_missing} total):")

        if tech_missing:
            display_tech = tech_missing[:15]
            feedback_lines.append(f"🔧 Technical skills: {', '.join(display_tech)}")
            if len(tech_missing) > 15:
                feedback_lines.append(f"   ... and {len(tech_missing) - 15} more")

        if soft_missing:
            display_soft = soft_missing[:10]
            feedback_lines.append(f"💼 Soft skills: {', '.join(display_soft)}")
            if len(soft_missing) > 10:
                feedback_lines.append(f"   ... and {len(soft_missing) - 10} more")

        if missing_keywords and not tech_missing and not soft_missing:
            display_other = missing_keywords[:20]
            feedback_lines.append(f"📝 Other keywords: {', '.join(display_other)}")
            if len(missing_keywords) > 20:
                feedback_lines.append(f"   ... and {len(missing_keywords) - 20} more")

    # Strengths
    strengths = detailed.get("strengths", [])
    if strengths:
        feedback_lines.append("\n🌟 STRENGTHS:")
        for s in strengths:
            feedback_lines.append(f"• {s}")

    # Weaknesses
    weaknesses = detailed.get("weaknesses", [])
    if weaknesses:
        feedback_lines.append("\n⚠️ AREAS FOR IMPROVEMENT:")
        for w in weaknesses:
            feedback_lines.append(f"• {w}")

    # Priority improvements
    priority = analysis.get("priority_improvements", [])
    if priority:
        feedback_lines.append("\n🎯 PRIORITY ACTIONS:")
        for i, p in enumerate(priority, 1):
            feedback_lines.append(f"{i}. {p}")

    # Recommendations
    recommendations = detailed.get("recommendations", [])
    if recommendations:
        feedback_lines.append("\n💡 DETAILED RECOMMENDATIONS:")
        for r in recommendations:
            feedback_lines.append(f"• {r}")

    # ATS compatibility
    ats_compat = detailed.get("ats_compatibility")
    if ats_compat:
        feedback_lines.append(f"\n🤖 ATS COMPATIBILITY:")
        feedback_lines.append(ats_compat)

    return "\n".join(feedback_lines)


# === API ENDPOINTS ===

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')


@app.route('/compare', methods=['POST'])
def compare_resume_to_job():
    try:
        print("Compare endpoint called")
        
        if 'resume' not in request.files or 'job' not in request.files:
            return jsonify({'error': 'Both resume and job description files are required'}), 400

        resume_file = request.files['resume']
        job_file = request.files['job']

        print(f"Resume file: {resume_file.filename}")
        print(f"Job file: {job_file.filename}")

        # Extract text
        resume_text = extract_text(resume_file)
        job_text = extract_text(job_file)

        print(f"Resume text length: {len(resume_text)}")
        print(f"Job text length: {len(job_text)}")

        if not resume_text.strip():
            return jsonify({'error': 'Resume file is empty or could not be read'}), 400
        if not job_text.strip():
            return jsonify({'error': 'Job description is empty or could not be read'}), 400

        # Analyze with Gemini
        print("Calling Gemini API...")
        analysis = analyze_with_gemini(resume_text, job_text)
        print("Gemini API response received")
        
        # Format feedback
        feedback = format_feedback(analysis)

        response_data = {
            "score": analysis.get("match_score", 0),
            "missing_keywords": analysis.get("missing_keywords", [])[:30],
            "matched_keywords": analysis.get("matched_keywords", [])[:30],
            "technical_skills_missing": analysis.get("technical_skills_missing", []),
            "soft_skills_missing": analysis.get("soft_skills_missing", []),
            "feedback": feedback,
            "total_matched": len(analysis.get("matched_keywords", [])),
            "total_missing": len(analysis.get("missing_keywords", [])),
            "raw_analysis": analysis
        }

        print(f"Returning response with score: {response_data['score']}")

        # Add no-cache headers
        response = jsonify(response_data)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    except Exception as e:
        print(f"Error in /compare endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API configuration"""
    return jsonify({
        "status": "ok" if client else "error",
        "api_configured": GEMINI_API_KEY is not None,
        "client_initialized": client is not None
    })


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting AI Resume Feedback System")
    print("=" * 60)
    if client:
        print("✅ Server ready at: http://localhost:5000")
    else:
        print("⚠️  Server starting but API key not configured")
        print("    Please set GEMINI_API_KEY in .env file")
    print("=" * 60 + "\n")
    
    app.run(debug=True)