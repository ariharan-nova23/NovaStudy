document.addEventListener("DOMContentLoaded", () => {
  const subjectId = getSelectedSubject();
  loadAnalysisData(subjectId);

  const sel = document.getElementById("globalSubjectSelect");
  if (sel) {
    sel.value = subjectId;
    sel.addEventListener("change", (e) => {
      setSelectedSubject(e.target.value);
      loadAnalysisData(e.target.value);
    });
  }

  const uploadForm = document.getElementById("paperUploadForm");
  if (uploadForm) {
    uploadForm.addEventListener("submit", handlePaperUpload);
  }
});

async function loadAnalysisData(subjectId) {
  const [patterns, repeated, questionsData] = await Promise.all([
    APIClient.get(`/api/analysis/patterns/${subjectId}`),
    APIClient.get(`/api/analysis/repeated/${subjectId}`),
    APIClient.get(`/api/analysis/questions/${subjectId}`)
  ]);

  if (patterns) renderPatternCharts(patterns);
  if (repeated) renderRepeatedQuestionsTable(repeated.repeated_groups);
  if (questionsData) renderExtractedQuestions(questionsData.questions);
}

async function handlePaperUpload(e) {
  e.preventDefault();
  const fileInput = document.getElementById("paperFileInput");
  const yearInput = document.getElementById("paperYearInput");
  const statusEl = document.getElementById("uploadStatusMessage");

  if (!fileInput.files || fileInput.files.length === 0) {
    alert("Please select a question paper PDF or image file.");
    return;
  }

  statusEl.style.display = "block";
  statusEl.innerHTML = `<span style="color: var(--accent-cyan);">⏳ Processing document & running question extraction engine...</span>`;

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("subject_id", getSelectedSubject());
  formData.append("year", yearInput.value || 2025);

  try {
  const res = await APIClient.upload("/api/upload/paper", formData);

  if (res && res.status === "success") {
    statusEl.innerHTML =
      `<span style="color: var(--accent-emerald);">
        ✓ Successfully extracted ${res.extracted_questions_count} questions!
      </span>`;

    loadAnalysisData(getSelectedSubject());
  }
} catch (error) {
  console.error(error);

  statusEl.innerHTML =
    `<span style="color: var(--accent-rose);">
      ❌ ${error.message}
    </span>`;
}

  if (res && res.status === "success") {
    statusEl.innerHTML = `<span style="color: var(--accent-emerald);">✓ Successfully extracted ${res.extracted_questions_count} structured questions from ${res.title}!</span>`;
    loadAnalysisData(getSelectedSubject());
  } else {
    statusEl.innerHTML = `<span style="color: var(--accent-rose);">❌ Failed to process paper. Please check file format.</span>`;
  }
}

function renderPatternCharts(patterns) {
  // Unit Distribution Bar Chart
  const unitCtx = document.getElementById("unitDistChart");
  if (unitCtx && window.Chart) {
    if (window.myUnitChart) window.myUnitChart.destroy();
    window.myUnitChart = new Chart(unitCtx, {
      type: 'bar',
      data: {
        labels: Object.keys(patterns.unit_distribution),
        datasets: [{
          label: 'Unit Distribution (%)',
          data: Object.values(patterns.unit_distribution),
          backgroundColor: ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
        }
      }
    });
  }

  // Question Types Doughnut Chart
  const typeCtx = document.getElementById("typeDistChart");
  if (typeCtx && window.Chart) {
    if (window.myTypeChart) window.myTypeChart.destroy();
    window.myTypeChart = new Chart(typeCtx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(patterns.question_type_distribution),
        datasets: [{
          data: Object.values(patterns.question_type_distribution),
          backgroundColor: ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6']
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: 'right', labels: { color: '#94a3b8' } } }
      }
    });
  }
}

function renderRepeatedQuestionsTable(groups) {
  const tableBody = document.getElementById("repeatedQuestionsTableBody");
  if (!tableBody || !groups) return;

  tableBody.innerHTML = groups.map(g => `
    <tr>
      <td>
        <strong style="color: var(--text-main); font-size: 0.95rem;">${g.concept}</strong>
        <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.2rem;">${g.unit} • ${g.topic}</div>
      </td>
      <td>${g.appeared_in_years.map(y => `<span class="badge badge-medium" style="margin-right: 4px;">${y}</span>`).join('')}</td>
      <td><strong style="color: var(--accent-amber);">${g.frequency}/${g.total_papers} Papers</strong> (${g.total_marks} Marks)</td>
      <td><span style="font-size: 0.85rem; font-weight: 600;">${g.trend}</span></td>
      <td><span class="badge ${g.priority.includes('Very High') ? 'badge-critical' : 'badge-high'}">${g.priority}</span></td>
    </tr>
  `).join('');
}

function renderExtractedQuestions(questions) {
  const listEl = document.getElementById("extractedQuestionsList");
  if (!listEl || !questions) return;

  listEl.innerHTML = questions.map((q, idx) => `
    <div style="padding: 1rem; background: rgba(255,255,255,0.02); border: 1px solid var(--border-color); border-radius: 12px; margin-bottom: 0.75rem;">
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
        <span style="font-size: 0.8rem; font-weight: 700; color: var(--accent-cyan);">Q${idx + 1} (${q.year}) • ${q.marks} Marks</span>
        <div>
          <span class="badge badge-medium" style="margin-right: 4px;">${q.unit}</span>
          <span class="badge badge-low">${q.question_type}</span>
          ${q.needs_review ? `<span class="badge badge-critical">Needs Review</span>` : ''}
        </div>
      </div>
      <div style="font-size: 0.95rem; font-weight: 500; color: var(--text-main);">${q.question}</div>
      <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 0.4rem;">Topic: ${q.topic} › ${q.subtopic}</div>
    </div>
  `).join('');
}
