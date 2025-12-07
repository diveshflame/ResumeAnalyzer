function compareResumeToJob() {
  const resumeInput = document.getElementById('resumeFile');
  const jobInput = document.getElementById('jobFile');
  const feedbackEl = document.getElementById('feedback');

  if (!resumeInput.files.length || !jobInput.files.length) {
    alert('Please upload both resume and job description.');
    return;
  }

  const formData = new FormData();
  formData.append('resume', resumeInput.files[0]);
  formData.append('job', jobInput.files[0]);

  feedbackEl.textContent = 'Analyzing resume against job description...';

  fetch('http://localhost:5000/compare', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.feedback) {
      feedbackEl.textContent = data.feedback;
    } else {
      feedbackEl.textContent = 'Error: ' + data.error;
    }
  })
  .catch(err => {
    feedbackEl.textContent = 'Error: ' + err.message;
  });
}
