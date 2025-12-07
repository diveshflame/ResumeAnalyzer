# Setup Checklist - Quick Start Guide

Follow these steps in order for a smooth setup!

## ☑️ Pre-Setup Checklist

- [ ] Python 3.8 or higher installed
  ```bash
  python --version  # or python3 --version
  ```
- [ ] pip is installed and updated
  ```bash
  python -m pip install --upgrade pip
  ```
- [ ] Internet connection is active
- [ ] All project files downloaded to same folder

---

## 📦 Step 1: Install Dependencies

### Option A: Quick Setup (Recommended)

**Windows:**
```cmd
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option B: Manual Setup
```bash
pip install -r requirements.txt
```

**Verify installation:**
```bash
pip list | grep -E "flask|google|PyMuPDF"
```

✅ **You should see:** flask, flask-cors, PyMuPDF, google-generativeai, python-dotenv

---

## 🔑 Step 2: Get Your Gemini API Key

1. **Visit:** https://makersuite.google.com/app/apikey

2. **Sign in** with your Google account

3. **Click** "Create API Key"

4. **Copy** the API key (starts with "AIza...")

⚠️ **IMPORTANT:** Keep this key private! Never share it or commit to Git.

---

## 📝 Step 3: Configure Environment Variables

### Create .env file:

**Windows (Command Prompt):**
```cmd
copy .env.example .env
notepad .env
```

**Mac/Linux/Windows (PowerShell):**
```bash
cp .env.example .env
nano .env  # or use any text editor
```

### Edit .env file:
```
GEMINI_API_KEY=AIza...your_actual_key_here
```

Replace `your_gemini_api_key_here` with your actual API key!

### Save and close the file

---

## ✅ Step 4: Verify Setup

Run the verification script:

```bash
python test_setup.py
```

**Expected output:**
```
Python Version................... ✅ PASS
Dependencies..................... ✅ PASS
File Structure................... ✅ PASS
Environment Config............... ✅ PASS
Gemini API...................... ✅ PASS

🎉 ALL TESTS PASSED!
```

If any test fails, check TROUBLESHOOTING.md

---

## 🚀 Step 5: Start the Application

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

✅ **Server is running!**

---

## 🌐 Step 6: Open in Browser

1. Open your web browser

2. Navigate to: **http://localhost:5000**

3. You should see the AI Resume Feedback System interface

---

## 🧪 Step 7: Test with Sample Data

### Quick Test:

1. Click **"Paste Text"** tab for resume

2. Copy sample resume from SAMPLE_DATA.md

3. Paste in **Resume text area**

4. Copy sample job description from SAMPLE_DATA.md

5. Paste in **Job Description text area**

6. Click **"Compare & Analyze"**

7. Wait 10-30 seconds

8. Review the AI-generated feedback!

**Expected:**
- Match score: ~75-85%
- Detailed feedback with strengths/weaknesses
- Missing keywords identified
- Actionable recommendations

---

## 📂 Your File Structure Should Look Like:

```
resume-feedback-system/
├── app.py                    ✅ Flask backend
├── index.html                ✅ Frontend HTML
├── styles.css                ✅ Styling
├── script.js                 ✅ Frontend JS
├── requirements.txt          ✅ Dependencies
├── .env                      ✅ Your API key (NEVER commit!)
├── .env.example              ✅ Template
├── .gitignore               ✅ Protect sensitive files
├── README.md                 ✅ Documentation
├── TROUBLESHOOTING.md        ✅ Help guide
├── SAMPLE_DATA.md            ✅ Test data
├── test_setup.py             ✅ Verification script
├── setup.sh                  ✅ Mac/Linux setup
└── setup.bat                 ✅ Windows setup
```

---

## 🎯 Common First-Time Issues

### Issue #1: API Key Not Working
```
❌ Error: GEMINI_API_KEY not configured
```

**Fix:**
1. Check `.env` file exists in project root
2. Open `.env` and verify API key is there
3. No quotes needed: `GEMINI_API_KEY=AIza123...`
4. Restart Flask server after changing `.env`

---

### Issue #2: Dependencies Not Installing
```
❌ Error: No module named 'flask'
```

**Fix:**
```bash
# Use Python 3 explicitly
pip3 install -r requirements.txt

# Or
python3 -m pip install -r requirements.txt
```

---

### Issue #3: Port Already in Use
```
❌ Error: Address already in use
```

**Fix:**
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000

# Mac/Linux:
lsof -i :5000

# Kill the process or use different port
```

---

### Issue #4: PDF Not Reading
```
❌ Error: Resume appears empty
```

**Fix:**
1. Use "Paste Text" option instead
2. Or export PDF with text (not scanned image)
3. Test with .txt file first

---

## 🔄 Stopping the Server

Press **Ctrl + C** in the terminal where Flask is running

---

## 🔄 Restarting After Changes

If you modify code:
1. Press **Ctrl + C** to stop
2. Run `python app.py` again
3. Refresh browser (Ctrl + F5)

Flask auto-reloads in debug mode, but manual restart is safer.

---

## 📊 Usage Tips

### For Best Results:

✅ **DO:**
- Use complete resume (all sections)
- Copy full job description
- Include all technical skills
- Keep formatting clean
- Test with different jobs

❌ **DON'T:**
- Use partial/incomplete documents
- Include only company name without JD
- Upload image-based PDFs
- Exceed 10,000 words total
- Run too many analyses quickly (rate limits)

---

## 🎓 Next Steps

Once everything works:

1. **Test with your actual resume**
   - Upload your real resume
   - Use job descriptions you're interested in
   - Review AI feedback carefully

2. **Iterate based on feedback**
   - Add missing keywords
   - Improve resume sections
   - Rerun analysis to see improvements

3. **Download reports**
   - Click "Download Report as PDF"
   - Keep for your records
   - Compare different job analyses

4. **Customize for your needs**
   - Modify prompts in app.py
   - Adjust frontend styling
   - Add additional features

---

## 🆘 Still Need Help?

1. ✅ Run `python test_setup.py` first
2. ✅ Check TROUBLESHOOTING.md
3. ✅ Review error messages carefully
4. ✅ Check Flask console output
5. ✅ Verify API key at https://makersuite.google.com/app/apikey
6. ✅ Try with sample data from SAMPLE_DATA.md

---

## ✨ You're All Set!

If all checks passed, you now have a working AI-powered resume analyzer!

**Features you can use:**
- ✅ Upload PDF or paste text resume
- ✅ Get AI match score
- ✅ See missing keywords
- ✅ Receive detailed feedback
- ✅ Get actionable recommendations
- ✅ Download PDF reports
- ✅ Test multiple job descriptions

**Happy job hunting! 🚀**

---

## 📝 Quick Reference Commands

```bash
# Start application
python app.py

# Stop application
Ctrl + C

# Verify setup
python test_setup.py

# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version

# List installed packages
pip list

# Update packages
pip install --upgrade -r requirements.txt
```

---

*Remember: Keep your .env file private and never commit it to version control!*