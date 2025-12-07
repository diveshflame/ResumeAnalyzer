# AI Resume Feedback System with Gemini API

An intelligent resume analyzer that uses Google's Gemini AI to provide detailed feedback on how well your resume matches a job description.

## Features

- 🤖 **AI-Powered Analysis**: Uses Gemini 1.5 Flash for intelligent resume evaluation
- 📊 **Match Score**: Get a percentage score showing resume-job alignment
- 🔍 **Keyword Analysis**: Identifies matched and missing keywords
- 💡 **Actionable Feedback**: Detailed recommendations for improvement
- 📋 **ATS Compatibility**: Checks if your resume is ATS-friendly
- 📥 **PDF Export**: Download your analysis report as PDF

## Prerequisites

- Check requirements.txt file
- Google Gemini API Key (free tier available)

## Installation

### 1. Clone or Download the Project

```bash
# Navigate to your project directory
cd resume-feedback-system
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 4. Set Up Environment Variable

**Option A: Using .env file (Recommended)**

1. Create a `.env` file in the project root:
```bash
# Create .env file
touch .env
```

2. Add your API key to `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

4. Add this to the top of `app.py` (after imports):
```python
from dotenv import load_dotenv
load_dotenv()
```

**Option B: Set environment variable directly**

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
```

**On Mac/Linux:**
```bash
export GEMINI_API_KEY=your_actual_api_key_here
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload your resume (PDF or TXT) or paste the text
4. Paste the job description
5. Click "Compare & Analyze"
6. View your detailed feedback!

## Project Structure

```
resume-feedback-system/
├── app.py              # Flask backend with Gemini integration
├── index.html          # Frontend HTML
├── styles.css          # Styling
├── script.js           # Frontend JavaScript
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md          # This file
```

## How It Works

1. **Upload/Paste**: You provide your resume and job description
2. **Text Extraction**: The system extracts text from PDF or uses pasted text
3. **AI Analysis**: Gemini AI analyzes the resume against job requirements
4. **Smart Feedback**: Receive detailed insights including:
   - Match percentage score
   - Matched and missing keywords
   - Technical and soft skills analysis
   - Resume structure evaluation
   - ATS compatibility assessment
   - Priority improvements
   - Actionable recommendations

## API Rate Limits

Gemini Free Tier Limits:
- **gemini-1.5-flash**: 15 requests per minute, 1,500 per day
- This should be sufficient for personal use

## Troubleshooting

### "GEMINI_API_KEY not configured" Error
- Make sure you've set the environment variable correctly
- Restart your terminal/command prompt after setting the variable
- Verify the API key is valid

### "Failed to parse AI response" Error
- This is rare but can happen with complex resumes
- Try again - Gemini's responses can vary slightly
- Ensure your resume and job description are not too long

### PDF Not Reading Correctly
- Make sure the PDF is not image-based (scanned document)
- Try converting to text format first
- Use the "Paste Text" option instead

### Server Won't Start
- Check if port 5000 is already in use
- Try: `python app.py` or `python3 app.py`
- Verify all dependencies are installed: `pip list`

## Features Explained

### Match Score
A percentage (0-100%) indicating how well your resume aligns with the job description.

### Missing Keywords
Important terms from the job description that aren't in your resume.

### Detailed Feedback
Comprehensive analysis including:
- Overall assessment
- Strengths and weaknesses
- Structure analysis
- Priority improvements
- Specific recommendations
- ATS compatibility tips

## Tips for Best Results

1. **Use Complete Documents**: Provide full resume and job description
2. **Clean Text**: Ensure text is readable (not images)
3. **Specific Jobs**: More detailed job descriptions = better analysis
4. **Update Resume**: Make changes based on feedback and reanalyze

## Security Notes

- Never commit your `.env` file to version control
- Keep your API key private
- The `.gitignore` file should include `.env`

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify your API key is valid and active
3. Check Gemini API status: [Google Cloud Status](https://status.cloud.google.com/)

## License

This project is for personal use. Modify and distribute as needed.

---

Made with ❤️ using Google Gemini AI