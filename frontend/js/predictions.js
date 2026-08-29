document.addEventListener("DOMContentLoaded", async () => {
  const subjectId = getSelectedSubject();
  loadPredictions(subjectId);

  const sel = document.getElementById("globalSubjectSelect");
  if (sel) {
    sel.value = subjectId;
    sel.addEventListener("change", (e) => {
      setSelectedSubject(e.target.value);
      loadPredictions(e.target.value);
    });
  }
});

async function loadPredictions(subjectId) {
  const data = await APIClient.get(`/api/predictions/${subjectId}`);
  if (!data) return;

  // Render Disclaimer Box
  const discEl = document.getElementById("predictionsDisclaimer");
  if (discEl) {
    discEl.textContent = data.disclaimer;
  }

  // Render High Priority Topics Grid
  const topicsGrid = document.getElementById("importantTopicsGrid");
  if (topicsGrid) {
    topicsGrid.innerHTML = data.important_topics.map(t => `
      <div class="card" style="position: relative; overflow: hidden;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
          <span class="badge ${t.priority_label === 'Critical' ? 'badge-critical' : (t.priority_label === 'High' ? 'badge-high' : 'badge-medium')}">${t.priority_label}</span>
          <span style="font-size: 1.5rem; font-weight: 800; color: var(--accent-primary);">${t.priority_score}%</span>
        </div>
        <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.25rem;">${t.topic}</h3>
        <div style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 1rem;">${t.unit} • Trend: ${t.trend}</div>
        <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">${t.rationale}</p>
      </div>
    `).join('');
  }

  // Render Likely Question Types
  const typesEl = document.getElementById("likelyTypesContainer");
  if (typesEl) {
    typesEl.innerHTML = Object.entries(data.likely_question_types).map(([type, prob]) => `
      <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1rem; background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 10px; margin-bottom: 0.5rem;">
        <span style="font-weight: 600; font-size: 0.95rem;">${type}</span>
        <span class="badge badge-high">${prob}</span>
      </div>
    `).join('');
  }
}
