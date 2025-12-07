# Troubleshooting Guide

## Common Issues and Solutions

### 1. "GEMINI_API_KEY not configured" Error

**Symptoms:**
- Error message appears when clicking "Compare & Analyze"
- Console shows "GEMINI_API_KEY not configured"

**Solutions:**

**Option A: Using .env file (Recommended)**
```bash
# Create .env file in project root
touch .env

# Add this line to .env file:
GEMINI_API_KEY=your_actual_api_key_here

# Restart the Flask server
```

**Option B: Set environment variable directly**

Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
python app.py
```

Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
python app.py
```

Mac/Linux:
```bash
export GEMINI_API_KEY=your_actual_api_key_here
python app.py
```

**Verify it's working:**
```python
# Test in Python terminal
import os
print(os.environ.get('GEMINI_API_KEY'))
# Should print your API key
```

---

### 2. "Failed to parse AI response" Error

**Symptoms:**
- Analysis starts but fails midway
- Error mentions JSON parsing

**Solutions:**
1. **Try again** - Gemini's responses can vary, rerunning often works
2. **Check resume/job length** - Very long documents (>10,000 words) might cause issues
3. **Simplify inputs** - Try with shorter, cleaner text first
4. **Check API quota** - You might have hit rate limits

---

### 3. Server Won't Start

**Symptoms:**
- `python app.py` fails
- Port already in use error

**Solutions:**

**Check if port 5000 is in use:**
```bash
# Windows
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :5000
```

**Kill the process using the port:**
```bash
# Windows (replace PID with actual process ID)
taskkill /PID <PID> /F

# Mac/Linux
kill -9 <PID>
```

**Or use a different port:**
```python
# In app.py, change last line to:
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

---

### 4. Dependencies Installation Failed

**Symptoms:**
- `pip install -r requirements.txt` fails
- Missing package errors

**Solutions:**

**Update pip first:**
```bash
python -m pip install --upgrade pip
```

**Install packages one by one:**
```bash
pip install flask
pip install flask-cors
pip install PyMuPDF
pip install google-generativeai
pip install python-dotenv
```

**Use Python 3 explicitly:**
```bash
pip3 install -r requirements.txt
python3 app.py
```

**Check Python version:**
```bash
python --version
# Should be 3.8 or higher
```

---

### 5. PDF Not Reading Correctly

**Symptoms:**
- "Resume appears empty" error
- Missing text from PDF

**Solutions:**

1. **Check if PDF is image-based:**
   - If the PDF is a scanned document, PyMuPDF can't extract text
   - Use OCR software first or convert to text manually
   
2. **Use the text input option:**
   - Click "Paste Text" tab
   - Copy-paste resume content directly

3. **Try a different PDF:**
   - Export from Word/Google Docs as PDF
   - Use "Save as PDF" with text preservation

4. **Test PDF extraction:**
```python
import fitz
doc = fitz.open("your_resume.pdf")
print(doc[0].get_text())
# Should print text from first page
```

---

### 6. Analysis Takes Too Long / Times Out

**Symptoms:**
- Stuck on "AI is analyzing..."
- Request times out after 60+ seconds

**Solutions:**

1. **Check internet connection** - Gemini API requires internet

2. **Reduce document length:**
   - Keep resume under 2-3 pages
   - Keep job description under 1000 words

3. **Verify API key is valid:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Check if key is still active

4. **Check Gemini API status:**
   - Visit [Google Cloud Status](https://status.cloud.google.com/)
   - Check for any service outages

---

### 7. API Rate Limit Exceeded

**Symptoms:**
- Error: "Resource has been exhausted"
- "Quota exceeded" message

**Solutions:**

**Free Tier Limits:**
- gemini-1.5-flash: 15 requests/minute, 1,500/day

**What to do:**
1. **Wait a minute** and try again
2. **Upgrade to paid tier** for higher limits
3. **Use sparingly** - analyze only when needed
4. **Check quota usage:**
   - Visit Google Cloud Console
   - Check API usage statistics

---

### 8. CORS Errors in Browser

**Symptoms:**
- Browser console shows CORS errors
- "Access-Control-Allow-Origin" errors

**Solutions:**

1. **Ensure Flask-CORS is installed:**
```bash
pip install flask-cors
```

2. **Verify CORS is enabled in app.py:**
```python
from flask_cors import CORS
CORS(app)
```

3. **Use correct URL:**
   - Access via `http://localhost:5000`
   - Not `file:///` or `127.0.0.1`

---

### 9. Frontend Not Loading / 404 Errors

**Symptoms:**
- Blank page when opening localhost:5000
- 404 errors for CSS/JS files

**Solutions:**

1. **Verify file structure:**
```
project-folder/
├── app.py
├── index.html
├── styles.css
├── script.js
├── requirements.txt
└── .env
```

2. **All files must be in same directory**

3. **Check Flask routes in app.py:**
```python
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
```

4. **Clear browser cache:** Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

---

### 10. Analysis Results Don't Make Sense

**Symptoms:**
- Match score seems wrong
- Feedback doesn't match resume

**Solutions:**

1. **Ensure clean text input:**
   - Remove special characters
   - Use plain text format
   - Avoid tables/columns in resume

2. **Provide complete job description:**
   - Include all requirements
   - Add technical skills section
   - Mention specific tools/technologies

3. **Try different format:**
   - Upload PDF instead of text
   - Or paste text instead of upload

4. **Run analysis again:**
   - AI responses can vary slightly
   - Second run might give better results

---

## Getting More Help

### Check Logs
```bash
# Run Flask with debug output
python app.py

# Check console for detailed errors
```

### Test API Key Separately
```python
import google.generativeai as genai
import os

# Test your API key
genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Say hello!")
print(response.text)
```

### Verify Installation
```bash
# Check installed packages
pip list | grep -E "flask|google|PyMuPDF"

# Should show all required packages
```

### Contact Support

1. **Gemini API Issues:** [Google AI Studio Support](https://ai.google.dev/)
2. **Python/Flask Issues:** Check official documentation
3. **PDF Extraction:** PyMuPDF documentation

---

## Prevention Tips

1. **Always use .env file** - Don't hardcode API keys
2. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`
3. **Test with simple inputs first** - Use short resume/JD for testing
4. **Monitor API usage** - Keep track of your quota
5. **Backup your .env file** - But never commit to git!

---

## Still Having Issues?

1. Delete everything and start fresh
2. Follow README.md step by step
3. Run the setup script: `bash setup.sh` or `setup.bat`
4. Test with example resume/job description
5. Check all error messages carefully

**Most issues are related to:**
- ❌ API key not set properly
- ❌ Dependencies not installed
- ❌ Wrong Python version
- ❌ Files in wrong directory
- ❌ Port already in use