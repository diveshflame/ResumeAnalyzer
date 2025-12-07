function switchResumeInput(type) {
  const fileInput = document.getElementById('resumeFileInput');
  const textInput = document.getElementById('resumeTextInput');
  const fileBtns = document.querySelectorAll('.file-input-group .tab-btn');
  
  // Remove active class from all resume tabs
  fileBtns.forEach(btn => btn.classList.remove('active'));
  
  if (type === 'file') {
    fileInput.classList.add('active');
    textInput.classList.remove('active');
    fileBtns[0].classList.add('active');
  } else {
    textInput.classList.add('active');
    fileInput.classList.remove('active');
    fileBtns[1].classList.add('active');
  }
}

function compareResumeToJob() {
  const resumeFileInput = document.getElementById('resumeFile');
  const resumeTextArea = document.getElementById('resumeText');
  const jobTextArea = document.getElementById('jobText');
  const feedbackEl = document.getElementById('feedback');
  const scoreEl = document.getElementById('matchScore');
  const missingEl = document.getElementById('missingKeywords');
  const progressFill = document.getElementById('progressFill');

  // Check if resume is provided (either file or text)
  const isResumeFileTabActive = document.getElementById('resumeFileInput').classList.contains('active');
  const isResumeTextTabActive = document.getElementById('resumeTextInput').classList.contains('active');
  
  let hasValidResumeInput = false;
  
  if (isResumeFileTabActive && resumeFileInput.files.length > 0) {
    hasValidResumeInput = true;
  } else if (isResumeTextTabActive && resumeTextArea.value.trim().length > 0) {
    hasValidResumeInput = true;
  }
  
  if (!hasValidResumeInput) {
    alert('Please provide a resume (upload a file or paste text).');
    return;
  }

  // Check if job description text is provided
  if (!jobTextArea.value.trim().length) {
    alert('Please paste a job description.');
    return;
  }

  // Clear previous results and show loading state
  feedbackEl.textContent = '🤖 AI is analyzing your resume...\n\nThis may take 10-30 seconds.\n\nThe AI is:\n• Reading your resume\n• Understanding the job requirements\n• Comparing skills and experience\n• Generating personalized feedback';
  scoreEl.textContent = '...';
  missingEl.textContent = 'Analyzing...';
  if (progressFill) {
    progressFill.style.width = '0%';
    progressFill.style.backgroundColor = '#6c757d';
  }

  const formData = new FormData();
  const timestamp = new Date().getTime();
  
  // Handle resume input based on active tab
  if (isResumeTextTabActive && resumeTextArea.value.trim().length > 0) {
    const resumeTextBlob = new Blob([resumeTextArea.value], { type: 'text/plain' });
    const resumeTextFile = new File([resumeTextBlob], `resume_${timestamp}.txt`, { type: 'text/plain' });
    formData.append('resume', resumeTextFile);
  } else if (isResumeFileTabActive && resumeFileInput.files.length > 0) {
    formData.append('resume', resumeFileInput.files[0]);
  }
  
  // Create a text file from the job textarea content
  const jobTextBlob = new Blob([jobTextArea.value], { type: 'text/plain' });
  const jobTextFile = new File([jobTextBlob], `job_description_${timestamp}.txt`, { type: 'text/plain' });
  formData.append('job', jobTextFile);

  // Add timestamp to prevent caching
  const url = `/compare?t=${timestamp}`;

  // Show progress animation
  let progress = 0;
  const progressInterval = setInterval(() => {
    if (progress < 90) {
      progress += Math.random() * 10;
      if (progressFill) {
        progressFill.style.width = Math.min(progress, 90) + '%';
      }
    }
  }, 500);

  fetch(url, {
    method: 'POST',
    body: formData,
    cache: 'no-cache',
    headers: {
      'Cache-Control': 'no-cache',
    }
  })
  .then(response => {
    clearInterval(progressInterval);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Response data:', data);
    
    if (data.error) {
      feedbackEl.textContent = '❌ Error: ' + data.error + '\n\nPlease check:\n• Your Gemini API key is set correctly\n• You have internet connection\n• The API quota is not exceeded';
      scoreEl.textContent = '-';
      missingEl.textContent = '-';
      if (progressFill) {
        progressFill.style.width = '0%';
      }
      return;
    }
    
    if (data.feedback) {
      // Update feedback
      feedbackEl.textContent = data.feedback;
      
      // Update score with animation
      const score = data.score || 0;
      animateScore(scoreEl, score);
      
      // Update progress bar with animation
      if (progressFill) {
        setTimeout(() => {
          progressFill.style.width = score + '%';
          progressFill.style.backgroundColor = getScoreColor(score);
        }, 100);
      }
      
      // Update missing keywords
      if (data.missing_keywords && data.missing_keywords.length > 0) {
        const displayKeywords = data.missing_keywords.slice(0, 15);
        missingEl.textContent = displayKeywords.join(', ');
        if (data.missing_keywords.length > 15) {
          missingEl.textContent += ` ... and ${data.missing_keywords.length - 15} more`;
        }
      } else {
        missingEl.textContent = 'None! 🎉';
      }
      
      // Show success message briefly
      showNotification('✅ Analysis complete!', 'success');
      
    } else {
      feedbackEl.textContent = '❌ Error: No feedback received from AI. Please try again.';
      scoreEl.textContent = '-';
      missingEl.textContent = '-';
    }
  })
  .catch(err => {
    clearInterval(progressInterval);
    console.error('Fetch error:', err);
    feedbackEl.textContent = '❌ Error: ' + err.message + '\n\n🔧 Troubleshooting:\n\n1. Make sure the Flask server is running\n2. Check your GEMINI_API_KEY environment variable\n3. Verify you have internet connection\n4. Check the console for detailed errors\n5. Ensure you haven\'t exceeded API rate limits';
    scoreEl.textContent = '-';
    missingEl.textContent = '-';
    if (progressFill) {
      progressFill.style.width = '0%';
    }
    showNotification('❌ Analysis failed', 'error');
  });
}

function animateScore(element, targetScore) {
  let currentScore = 0;
  const increment = targetScore / 30;
  const interval = setInterval(() => {
    currentScore += increment;
    if (currentScore >= targetScore) {
      currentScore = targetScore;
      clearInterval(interval);
    }
    element.textContent = Math.round(currentScore);
  }, 30);
}

function getScoreColor(score) {
  if (score >= 80) return '#4CAF50'; // Green
  if (score >= 60) return '#FFC107'; // Yellow
  if (score >= 40) return '#FF9800'; // Orange
  return '#F44336'; // Red
}

function showNotification(message, type) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 25px;
    border-radius: 8px;
    background: ${type === 'success' ? '#4CAF50' : '#F44336'};
    color: white;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    animation: slideIn 0.3s ease-out;
  `;
  
  document.body.appendChild(notification);
  
  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease-out';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

function clearResults() {
  document.getElementById('feedback').textContent = 'Upload a resume and paste job description to get AI-powered feedback...';
  document.getElementById('matchScore').textContent = '-';
  document.getElementById('missingKeywords').textContent = '-';
  const progressFill = document.getElementById('progressFill');
  if (progressFill) {
    progressFill.style.width = '0%';
    progressFill.style.backgroundColor = '#6c757d';
  }
}

// Clear results when inputs change
document.getElementById('resumeFile').addEventListener('change', clearResults);
document.getElementById('resumeText').addEventListener('input', clearResults);
document.getElementById('jobText').addEventListener('input', clearResults);

function downloadPDF() {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  
  // Get feedback content
  const feedback = document.getElementById('feedback').textContent;
  const score = document.getElementById('matchScore').textContent;
  const missing = document.getElementById('missingKeywords').textContent;
  
  // Check if analysis has been done
  if (score === '-' || feedback.includes('get AI-powered feedback')) {
    alert('Please run the analysis first before downloading the report.');
    return;
  }
  
  // Add title
  doc.setFontSize(20);
  doc.setFont(undefined, 'bold');
  doc.text('AI Resume Analysis Report', 20, 20);
  
  // Add generation date
  doc.setFontSize(10);
  doc.setFont(undefined, 'normal');
  doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 30);
  
  // Add score
  doc.setFontSize(16);
  doc.setFont(undefined, 'bold');
  doc.text(`Match Score: ${score}%`, 20, 45);
  
  // Add score interpretation
  doc.setFontSize(11);
  doc.setFont(undefined, 'normal');
  const scoreNum = parseInt(score);
  let interpretation = '';
  if (scoreNum >= 80) interpretation = 'Excellent Match';
  else if (scoreNum >= 60) interpretation = 'Good Match';
  else if (scoreNum >= 40) interpretation = 'Moderate Match';
  else interpretation = 'Needs Improvement';
  doc.text(`(${interpretation})`, 20, 52);
  
  // Add missing keywords section
  doc.setFontSize(12);
  doc.setFont(undefined, 'bold');
  doc.text('Missing Keywords:', 20, 65);
  doc.setFont(undefined, 'normal');
  doc.setFontSize(10);
  const splitMissing = doc.splitTextToSize(missing, 170);
  doc.text(splitMissing, 20, 72);
  
  // Add detailed feedback
  const feedbackStartY = 72 + (splitMissing.length * 5) + 10;
  doc.setFontSize(12);
  doc.setFont(undefined, 'bold');
  doc.text('Detailed Feedback:', 20, feedbackStartY);
  
  doc.setFontSize(9);
  doc.setFont(undefined, 'normal');
  const splitFeedback = doc.splitTextToSize(feedback, 170);
  doc.text(splitFeedback, 20, feedbackStartY + 7);
  
  // Add footer
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFontSize(8);
    doc.text(`Page ${i} of ${pageCount}`, 105, 285, { align: 'center' });
    doc.text('Generated by AI Resume Feedback System', 105, 290, { align: 'center' });
  }
  
  // Save the PDF
  doc.save(`resume-analysis-${new Date().getTime()}.pdf`);
  showNotification('📥 PDF downloaded successfully!', 'success');
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(400px);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);