let currentQuizQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};
let quizSubjectId = "dsa";

document.addEventListener("DOMContentLoaded", () => {
  quizSubjectId = getSelectedSubject();
  
  const startBtn = document.getElementById("startQuizBtn");
  if (startBtn) {
    startBtn.addEventListener("click", initQuiz);
  }
});

async function initQuiz() {
  const modeSel = document.getElementById("quizModeSelect")?.value || "Quick Quiz";
  const numQs = parseInt(document.getElementById("quizNumInput")?.value || 5);
  const diff = document.getElementById("quizDiffSelect")?.value || "Adaptive";

  const config = {
    subject_id: quizSubjectId,
    quiz_mode: modeSel,
    num_questions: numQs,
    difficulty: diff
  };

  const quiz = await APIClient.post("/api/quiz/generate", config);
  if (!quiz || !quiz.questions || quiz.questions.length === 0) {
    alert("Could not load quiz questions.");
    return;
  }

  currentQuizQuestions = quiz.questions;
  currentQuestionIndex = 0;
  userAnswers = {};

  document.getElementById("quizConfigBox").style.display = "none";
  document.getElementById("quizPlayerContainer").style.display = "block";
  document.getElementById("quizResultSummaryBox").style.display = "none";

  renderQuestion();
}

function renderQuestion() {
  const q = currentQuizQuestions[currentQuestionIndex];
  const total = currentQuizQuestions.length;

  document.getElementById("quizProgressHeader").textContent = `Question ${currentQuestionIndex + 1} of ${total}`;
  document.getElementById("quizProgressBarFill").style.width = `${((currentQuestionIndex + 1) / total) * 100}%`;

  const questionCard = document.getElementById("quizQuestionCard");
  questionCard.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
      <span class="badge badge-medium">${q.unit} • ${q.topic}</span>
      <span class="badge ${q.difficulty === 'Hard' ? 'badge-critical' : 'badge-high'}">${q.difficulty}</span>
    </div>
    <div class="question-text">${q.question}</div>

    <div class="options-grid">
      ${q.options.map((opt, idx) => `
        <button class="option-btn ${userAnswers[q.id] === idx ? 'selected' : ''}" onclick="selectOption('${q.id}', ${idx})">
          <div class="option-prefix">${String.fromCharCode(65 + idx)}</div>
          <div>${opt}</div>
        </button>
      `).join('')}
    </div>

    ${q.hint ? `
      <div style="margin-top: 1rem;">
        <button class="btn btn-secondary" style="font-size: 0.8rem; padding: 0.4rem 0.8rem;" onclick="toggleHint()">💡 Need a Hint?</button>
        <div id="quizHintBox" class="hint-drawer" style="display: none;">${q.hint}</div>
      </div>
    ` : ''}

    <div id="explanationBox" class="explanation-panel" style="display: none;"></div>

    <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
      <button class="btn btn-secondary" ${currentQuestionIndex === 0 ? 'disabled' : ''} onclick="prevQuestion()">← Previous</button>
      <button id="quizSubmitNextBtn" class="btn btn-primary" onclick="submitOrNextQuestion()">
        ${currentQuestionIndex === total - 1 ? 'Finish & Submit Quiz' : 'Check Answer & Next →'}
      </button>
    </div>
  `;
}

function selectOption(qId, optionIdx) {
  userAnswers[qId] = optionIdx;
  const buttons = document.querySelectorAll(".option-btn");
  buttons.forEach((btn, idx) => {
    if (idx === optionIdx) btn.classList.add("selected");
    else btn.classList.remove("selected");
  });
}

function toggleHint() {
  const box = document.getElementById("quizHintBox");
  if (box) box.style.display = box.style.display === "none" ? "block" : "none";
}

function submitOrNextQuestion() {
  const q = currentQuizQuestions[currentQuestionIndex];
  const selectedIdx = userAnswers[q.id];

  if (selectedIdx === undefined) {
    alert("Please select an answer option.");
    return;
  }

  // Show correct / incorrect styling
  const buttons = document.querySelectorAll(".option-btn");
  buttons.forEach((btn, idx) => {
    btn.disabled = true;
    if (idx === q.correct_answer_index) {
      btn.classList.add("correct");
    } else if (idx === selectedIdx && selectedIdx !== q.correct_answer_index) {
      btn.classList.add("incorrect");
    }
  });

  const expBox = document.getElementById("explanationBox");
  if (expBox) {
    expBox.style.display = "block";
    expBox.innerHTML = `<strong>${selectedIdx === q.correct_answer_index ? '✓ Correct!' : '❌ Incorrect.'}</strong> ${q.explanation}`;
  }

  const nextBtn = document.getElementById("quizSubmitNextBtn");
  nextBtn.textContent = (currentQuestionIndex === currentQuizQuestions.length - 1) ? 'View Final Results 🏆' : 'Next Question →';
  nextBtn.onclick = () => {
    if (currentQuestionIndex < currentQuizQuestions.length - 1) {
      currentQuestionIndex++;
      renderQuestion();
    } else {
      finishQuiz();
    }
  };
}

function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    renderQuestion();
  }
}

async function finishQuiz() {
  const payload = {
    quiz_id: "quiz_completed",
    subject_id: quizSubjectId,
    answers: userAnswers
  };

  const result = await APIClient.post("/api/quiz/submit", payload);

  document.getElementById("quizPlayerContainer").style.display = "none";
  const summaryBox = document.getElementById("quizResultSummaryBox");
  summaryBox.style.display = "block";

  summaryBox.innerHTML = `
    <div class="card" style="text-align: center; padding: 2.5rem;">
      <h2 style="font-size: 1.8rem; font-weight: 800; margin-bottom: 0.5rem;">Quiz Evaluation Complete!</h2>
      <div style="font-size: 3rem; font-weight: 800; color: var(--accent-cyan); font-family: var(--font-mono); margin: 1rem 0;">
        ${result.score} / ${result.total_questions} (${result.percentage}%)
      </div>

      <div class="grid-2" style="margin: 2rem 0; text-align: left;">
        <div style="padding: 1.25rem; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px;">
          <h4 style="color: #a7f3d0; font-weight: 700; margin-bottom: 0.5rem;">💪 Strong Topics</h4>
          <ul style="margin-left: 1.25rem; font-size: 0.9rem;">
            ${result.strong_areas.map(a => `<li>${a}</li>`).join('')}
          </ul>
        </div>

        <div style="padding: 1.25rem; background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 12px;">
          <h4 style="color: #fecdd3; font-weight: 700; margin-bottom: 0.5rem;">⚠ Weak Topics to Revise</h4>
          <ul style="margin-left: 1.25rem; font-size: 0.9rem;">
            ${result.weak_areas.map(a => `<li>${a}</li>`).join('')}
          </ul>
        </div>
      </div>

      <div style="display: flex; gap: 1rem; justify-content: center;">
        <button class="btn btn-secondary" onclick="location.reload()">🔄 Retake Quiz</button>
        <a href="study-plan.html" class="btn btn-primary">📅 Update Study Plan</a>
      </div>
    </div>
  `;
}
