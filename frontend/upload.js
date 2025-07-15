// Wizard step navigation helpers
function showStep(stepIndex) {
  const steps = document.querySelectorAll('.step-content');
  steps.forEach((el, i) => {
    el.style.display = i === stepIndex ? (el.tagName === 'FORM' ? 'flex' : 'block') : 'none';
  });
  // Update stepper
  const stepperSteps = document.querySelectorAll('#wizard-stepper .step');
  stepperSteps.forEach((el, i) => {
    if (i === stepIndex) el.classList.add('active');
    else el.classList.remove('active');
  });
}

// Step 0: Upload
const uploadBtn = document.getElementById('upload-btn');
const uploadInput = document.getElementById('pdf-input');
const uploadStatus = document.getElementById('upload-status');
const reviewForm = document.getElementById('step-review');
const saveStatus = document.getElementById('save-status');
const regimeSection = document.getElementById('step-regime');
const comparisonStep = document.getElementById('step-compare');
const comparisonCards = document.getElementById('comparison-cards');

showStep(0); // Start at upload step

uploadBtn.onclick = async function() {
  uploadStatus.textContent = '';
  if (!uploadInput.files[0]) {
    uploadStatus.textContent = 'Please select a PDF file.';
    return;
  }
  const file = uploadInput.files[0];
  if (file.type !== 'application/pdf') {
    uploadStatus.textContent = 'Only PDF files are allowed.';
    return;
  }
  uploadStatus.textContent = 'Uploading and extracting...';
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch('http://localhost:8000/api/upload-pdf', {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  if (data.error) {
    uploadStatus.textContent = 'Error: ' + data.error;
    return;
  }
  uploadStatus.textContent = '';
  // Populate review form
  for (const key in data.extracted) {
    if (reviewForm.elements[key]) {
      reviewForm.elements[key].value = data.extracted[key];
    }
  }
  showStep(1); // Go to review step
};

document.getElementById('back-to-upload').onclick = function() {
  showStep(0);
};

// Step 1: Review
let sessionId = null;

reviewForm.onsubmit = async function(e) {
  e.preventDefault();
  saveStatus.textContent = 'Saving...';
  const formData = new FormData(reviewForm);
  const res = await fetch('http://localhost:8000/api/save-financials', {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  if (data.saved) {
    saveStatus.textContent = '';
    sessionId = data.session_id;
    // Show regime selection in step 3
    regimeSection.innerHTML = `
      <h3>Choose Your Preferred Regime</h3>
      <div class="regime-toggle">
        <label><input type="radio" name="regime" value="old" checked> <span>Old Regime 🏛️</span></label>
        <label><input type="radio" name="regime" value="new"> <span>New Regime 🚀</span></label>
      </div>
      <button id="compare-btn">Compare Tax</button>
      <button id="back-to-review" class="review-save-btn" style="margin-top:1.2rem;max-width:300px;">Back</button>
    `;
    showStep(2);
    document.getElementById('compare-btn').onclick = async function() {
      const regime = document.querySelector('input[name="regime"]:checked').value;
      // Gather all form data again
      const payload = {};
      for (const el of reviewForm.elements) {
        if (el.name) payload[el.name] = el.value;
      }
      payload['preferred_regime'] = regime;
      const res2 = await fetch('http://localhost:8000/api/calculate-tax', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await res2.json();
      renderComparisonCards(result);
      showStep(3);
    };
    document.getElementById('back-to-review').onclick = function() {
      showStep(1);
    };
  } else {
    saveStatus.textContent = 'Error saving data.';
  }
};

document.getElementById('back-to-regime').onclick = function() {
  showStep(2);
};

document.getElementById('next-to-gemini').onclick = async function() {
  // Step 1: Get Gemini's question
  document.getElementById('gemini-question').textContent = '';
  document.getElementById('gemini-suggestions').textContent = '';
  document.getElementById('gemini-form').style.display = 'none';
  document.getElementById('gemini-loading').style.display = 'block';
  showStep(4); // Show Gemini step
  const res = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, user_message: "" })
  });
  const data = await res.json();
  document.getElementById('gemini-loading').style.display = 'none';
  document.getElementById('gemini-question').textContent = data.question;
  document.getElementById('gemini-form').style.display = 'flex';
};

document.getElementById('back-to-compare').onclick = function() {
  showStep(3);
};

document.getElementById('gemini-form').onsubmit = async function(e) {
  e.preventDefault();
  document.getElementById('gemini-suggestions').textContent = '';
  document.getElementById('gemini-loading').style.display = 'block';
  const answer = document.getElementById('gemini-answer').value;
  const res = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, user_message: answer })
  });
  const data = await res.json();
  document.getElementById('gemini-loading').style.display = 'none';
  document.getElementById('gemini-suggestions').innerHTML = `<div class="suggestion-block">${data.suggestions.replace(/\n/g, '<br>')}</div>`;
};

function renderComparisonCards(result) {
  comparisonCards.style.display = 'flex';
  const { old_regime, new_regime, preferred_regime, better_regime, savings } = result;
  const highlight = (regime) => regime === better_regime ? 'highlight-card' : '';
  const userPick = (regime) => regime === preferred_regime ? '<span class="user-pick">Your Pick ⭐</span>' : '';
  comparisonCards.innerHTML = `
    <div class="tax-card ${highlight('old')}">
      <div class="card-header"><span class="emoji">🏛️</span> Old Regime ${userPick('old')}</div>
      <div class="tax-amt">₹${old_regime.tax_with_cess.toLocaleString()}</div>
      <div class="tax-breakdown">
        <div>Taxable Income: ₹${old_regime.taxable_income.toLocaleString()}</div>
        <div>Tax: ₹${old_regime.tax.toLocaleString()}</div>
        <div>Cess (4%): Included</div>
      </div>
      <div class="card-footer">${highlight('old') ? 'Best for you! 🎉' : ''}</div>
    </div>
    <div class="tax-card ${highlight('new')}">
      <div class="card-header"><span class="emoji">🚀</span> New Regime ${userPick('new')}</div>
      <div class="tax-amt">₹${new_regime.tax_with_cess.toLocaleString()}</div>
      <div class="tax-breakdown">
        <div>Taxable Income: ₹${new_regime.taxable_income.toLocaleString()}</div>
        <div>Tax: ₹${new_regime.tax.toLocaleString()}</div>
        <div>Cess (4%): Included</div>
      </div>
      <div class="card-footer">${highlight('new') ? 'Best for you! 🎉' : ''}</div>
    </div>
  `;
  if (savings > 0) {
    comparisonCards.innerHTML += `<div class="savings-banner">🎊 You save <b>₹${savings.toLocaleString()}</b> by choosing the <b>${better_regime === 'old' ? 'Old' : 'New'} Regime</b>!</div>`;
  }
} 