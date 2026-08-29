let examTimeSeconds = 180 * 60; // 3 hours
let examTimerInterval = null;
let currentExamQuestions = [];
let activeExamQuestionIdx = 0;
let examAnswers = {};
let examMarkedForReview = new Set();

document.addEventListener("DOMContentLoaded", () => {
  const startExamBtn = document.getElementById("startMockExamBtn");
  if (startExamBtn) {
    startExamBtn.addEventListener("click", launchMockExam);
  }
});

async function launchMockExam() {
  const config = {
    subject_id: getSelectedSubject(),
    total_marks: 100,
    duration_minutes: 180,
    difficulty_mode: "Balanced"
  };

  const paper = await APIClient.post("/api/mock-exam/generate", config);
  if (!paper || !paper.sections) return;

  // Flatten questions for exam environment
  currentExamQuestions = [];
  paper.sections.forEach(sec => {
    sec.questions.forEach(q => currentExamQuestions.push(q));
  });

  document.getElementById("mockExamConfigContainer").style.display = "none";
  document.getElementById("mockExamActiveContainer").style.display = "block";

  startExamTimer();
  renderExamPalette();
  renderExamQuestion(0);
}

function startExamTimer() {
  clearInterval(examTimerInterval);
  examTimerInterval = setInterval(() => {
    if (examTimeSeconds <= 0) {
      clearInterval(examTimerInterval);
      submitMockExam();
      return;
    }
    examTimeSeconds--;
    const hrs = Math.floor(examTimeSeconds / 3600);
    const mins = Math.floor((examTimeSeconds % 3600) / 60);
    const secs = examTimeSeconds % 60;
    
    const timerEl = document.getElementById("examTimerDisplay");
    if (timerEl) {
      timerEl.textContent = `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
  }, 1000);
}

function renderExamPalette() {
  const paletteContainer = document.getElementById("examQuestionPalette");
  if (!paletteContainer) return;

  paletteContainer.innerHTML = currentExamQuestions.map((q, idx) => {
    let statusClass = "";
    if (idx === activeExamQuestionIdx) statusClass += " active";
    if (examAnswers[q.id]) statusClass += " answered";
    if (examMarkedForReview.has(q.id)) statusClass += " marked";

    return `
      <button class="palette-btn ${statusClass}" onclick="renderExamQuestion(${idx})">
        ${idx + 1}
      </button>
    `;
  }).join('');
}

function renderExamQuestion(idx) {
  activeExamQuestionIdx = idx;
  renderExamPalette();

  const q = currentExamQuestions[idx];
  const qContainer = document.getElementById("examActiveQuestionBox");
  if (!qContainer) return;

  const currentVal = examAnswers[q.id] || "";

  qContainer.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
      <span class="badge badge-medium">Question ${idx + 1} of ${currentExamQuestions.length} • [${q.marks} Marks]</span>
      <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.35rem 0.75rem;" onclick="toggleMarkForReview('${q.id}')">
        ${examMarkedForReview.has(q.id) ? '⭐ Marked for Review' : '☆ Mark for Review'}
      </button>
    </div>

    <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 1.5rem;">${q.question}</h3>

    <div style="margin-top: 1rem;">
      <label style="display: block; font-size: 0.85rem; font-weight: 600; color: var(--text-dim); margin-bottom: 0.5rem;">Your Descriptive / Algorithmic Answer:</label>
      <textarea id="examAnswerTextArea" style="width: 100%; height: 180px; background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem; color: var(--text-main); font-family: inherit; font-size: 0.95rem; resize: vertical;" placeholder="Type your structured answer, step-by-step logic, or code here...">${currentVal}</textarea>
    </div>

    <div class="exam-footer-nav">
      <button class="btn btn-secondary" ${idx === 0 ? 'disabled' : ''} onclick="renderExamQuestion(${idx - 1})">← Previous Question</button>
      <button class="btn btn-primary" onclick="saveAnswerAndNext(${idx})">
        ${idx === currentExamQuestions.length - 1 ? 'Save & Finish Exam' : 'Save Answer & Next →'}
      </button>
    </div>
  `;

  // Attach auto-save listener
  const txt = document.getElementById("examAnswerTextArea");
  if (txt) {
    txt.addEventListener("input", (e) => {
      examAnswers[q.id] = e.target.value;
      renderExamPalette();
    });
  }
}

function toggleMarkForReview(qId) {
  if (examMarkedForReview.has(qId)) examMarkedForReview.delete(qId);
  else examMarkedForReview.add(qId);
  renderExamQuestion(activeExamQuestionIdx);
}

function saveAnswerAndNext(idx) {
  const txt = document.getElementById("examAnswerTextArea");
  if (txt && currentExamQuestions[idx]) {
    examAnswers[currentExamQuestions[idx].id] = txt.value;
  }

  if (idx < currentExamQuestions.length - 1) {
    renderExamQuestion(idx + 1);
  } else {
    if (confirm("Are you sure you want to submit your Mock Examination?")) {
      submitMockExam();
    }
  }
}

async function submitMockExam() {
  clearInterval(examTimerInterval);
  const payload = {
    exam_id: "mock_exam_101",
    subject_id: getSelectedSubject(),
    answers: examAnswers,
    time_taken_seconds: 10800 - examTimeSeconds
  };

  const report = await APIClient.post("/api/mock-exam/submit", payload);

  document.getElementById("mockExamActiveContainer").style.display = "none";
  const resultBox = document.getElementById("mockExamResultBox");
  resultBox.style.display = "block";

  resultBox.innerHTML = `
    <div class="card" style="padding: 2.5rem;">
      <h2 style="font-size: 1.8rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem;">Exam Performance Report</h2>
      <div style="text-align: center; font-size: 3rem; font-weight: 800; color: var(--accent-emerald); font-family: var(--font-mono);">
        ${report.score} / ${report.total_marks} Marks (${report.accuracy})
      </div>

      <h3 style="font-size: 1.1rem; font-weight: 700; margin-top: 2rem; margin-bottom: 1rem;">Rubric-Based AI Evaluation</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>Evaluation Criterion</th>
            <th>Points Awarded</th>
            <th>Feedback Rationale</th>
          </tr>
        </thead>
        <tbody>
          ${report.rubric_breakdown.map(r => `
            <tr>
              <td><strong>${r.criterion}</strong></td>
              <td><span style="color: var(--accent-cyan); font-weight: 700;">${r.points}</span></td>
              <td>${r.feedback}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem;">
        <button class="btn btn-secondary" onclick="location.reload()">🔄 Return to Mock Exam Hub</button>
        <a href="progress.html" class="btn btn-primary">📈 View Progress Analytics</a>
      </div>
    </div>
  `;
}
