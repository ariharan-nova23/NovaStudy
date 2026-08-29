document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("modelPaperConfigForm");
  if (form) {
    form.addEventListener("submit", handleGeneratePaper);
  }
});

async function handleGeneratePaper(e) {
  e.preventDefault();

  const valContainer = document.getElementById("validationProgressBox");
  const resultContainer = document.getElementById("generatedPaperResultView");

  valContainer.style.display = "block";
  resultContainer.style.display = "none";

  // Display validation check animation pipeline
  valContainer.innerHTML = `
    <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 1rem; color: var(--accent-cyan);">
      🤖 Running AI Model Question Paper Generation & 6-Step Validation Engine...
    </h3>
    <div id="valStepsList" style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.9rem;">
      <div>⏳ Step 1: Synthesizing concept-based questions...</div>
    </div>
  `;

  const subjectId = getSelectedSubject();
  const config = {
    subject_id: subjectId,
    total_marks: parseInt(document.getElementById("paperMarksInput")?.value || 100),
    duration_minutes: parseInt(document.getElementById("paperDurationInput")?.value || 180),
    difficulty_mode: document.getElementById("paperDifficultySelect")?.value || "Balanced",
    num_previous_papers_considered: 4
  };

  const paper = await APIClient.post("/api/mock-exam/generate", config);

  if (!paper) {
    valContainer.innerHTML = `<span style="color: var(--accent-rose);">❌ Paper generation failed. Please retry.</span>`;
    return;
  }

  // Animate validation steps
  const stepsList = document.getElementById("valStepsList");
  if (stepsList && paper.validation_checks) {
    let delay = 300;
    paper.validation_checks.forEach((chk, i) => {
      setTimeout(() => {
        const div = document.createElement("div");
        div.style.color = chk.passed ? "#a7f3d0" : "#fecdd3";
        div.innerHTML = `✓ ${chk.check_name}: <strong>${chk.details}</strong>`;
        stepsList.appendChild(div);

        if (i === paper.validation_checks.length - 1) {
          setTimeout(() => {
            valContainer.style.display = "none";
            renderModelPaper(paper);
          }, 600);
        }
      }, delay);
      delay += 250;
    });
  } else {
    valContainer.style.display = "none";
    renderModelPaper(paper);
  }
}

function renderModelPaper(paper) {
  const resultContainer = document.getElementById("generatedPaperResultView");
  if (!resultContainer) return;

  resultContainer.style.display = "block";
  resultContainer.scrollIntoView({ behavior: "smooth" });

  resultContainer.innerHTML = `
    <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 20px; padding: 2.5rem; box-shadow: var(--shadow-lg);">
      <div style="text-align: center; border-bottom: 2px solid var(--border-color); padding-bottom: 1.5rem; margin-bottom: 1.5rem;">
        <span class="badge badge-high" style="margin-bottom: 0.5rem;">AI Generated & Validated Model Paper</span>
        <h2 style="font-size: 1.6rem; font-weight: 800; text-transform: uppercase; letter-spacing: -0.01em;">${paper.subject_name}</h2>
        <div style="display: flex; justify-content: center; gap: 2rem; font-size: 0.9rem; color: var(--text-muted); margin-top: 0.75rem;">
          <span><strong>Total Marks:</strong> ${paper.total_marks}</span>
          <span><strong>Duration:</strong> ${paper.duration_minutes} Minutes</span>
          <span><strong>Pattern:</strong> ${paper.difficulty_mode}</span>
        </div>
      </div>

      <div style="margin-bottom: 2rem; padding: 1rem; background: rgba(255,255,255,0.02); border: 1px dashed var(--border-color); border-radius: 10px; font-size: 0.85rem;">
        <strong>Instructions to Candidates:</strong>
        <ol style="margin-left: 1.25rem; margin-top: 0.4rem;">
          ${paper.instructions.map(ins => `<li>${ins}</li>`).join('')}
        </ol>
      </div>

      ${paper.sections.map(sec => `
        <div style="margin-bottom: 2rem;">
          <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--accent-cyan); border-bottom: 1px solid var(--border-color); padding-bottom: 0.4rem; margin-bottom: 1rem;">
            ${sec.section_name}
          </h3>
          <div style="display: flex; flex-direction: column; gap: 1.25rem;">
            ${sec.questions.map((q, idx) => `
              <div style="display: flex; justify-content: space-between; gap: 1rem; font-size: 0.95rem;">
                <div>
                  <strong>Q${idx + 1}.</strong> ${q.question}
                  <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.2rem;">${q.unit} • ${q.topic} • ${q.type}</div>
                </div>
                <strong style="color: var(--accent-amber); font-family: var(--font-mono); font-size: 0.9rem; flex-shrink: 0;">[${q.marks} Marks]</strong>
              </div>
            `).join('')}
          </div>
        </div>
      `).join('')}

      <div style="display: flex; gap: 1rem; margin-top: 2rem; justify-content: flex-end;">
        <button class="btn btn-secondary" onclick="window.print()">🖨️ Print / Download PDF</button>
        <a href="quiz.html" class="btn btn-primary">🧠 Attempt Practice Quiz</a>
      </div>
    </div>
  `;
}
