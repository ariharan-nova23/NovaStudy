document.addEventListener("DOMContentLoaded", async () => {
  const subjectId = getSelectedSubject();
  loadProgressData(subjectId);

  const sel = document.getElementById("globalSubjectSelect");
  if (sel) {
    sel.value = subjectId;
    sel.addEventListener("change", (e) => {
      setSelectedSubject(e.target.value);
      loadProgressData(e.target.value);
    });
  }
});

async function loadProgressData(subjectId) {
  const data = await APIClient.get(`/api/progress/${subjectId}`);
  if (!data) return;

  // Render Overall Readiness
  const readinessEl = document.getElementById("overallReadinessScore");
  if (readinessEl) readinessEl.textContent = `${data.overall_readiness}%`;

  // Render Topic Mastery Table
  const masteryBody = document.getElementById("topicMasteryTableBody");
  if (masteryBody && data.topic_mastery) {
    masteryBody.innerHTML = data.topic_mastery.map(m => `
      <tr>
        <td><strong>${m.topic}</strong></td>
        <td><span style="color: var(--text-dim);">${m.mastery_before}%</span></td>
        <td><strong style="color: var(--accent-emerald);">${m.mastery_now}%</strong></td>
        <td><span class="badge badge-medium" style="color: #a7f3d0; background: rgba(16, 185, 129, 0.2);">${m.delta}</span></td>
      </tr>
    `).join('');
  }

  // Render Chart
  renderProgressChart(data.recent_scores);
}

function renderProgressChart(scores) {
  const ctx = document.getElementById("progressTrendChart");
  if (!ctx || !window.Chart) return;

  if (window.myProgressChart) window.myProgressChart.destroy();

  const labels = (scores || []).map(s => s.date);
  const values = (scores || []).map(s => Math.round((s.score / Math.max(1, s.total)) * 100));

  window.myProgressChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Quiz & Mock Score Trend (%)',
        data: values,
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99, 102, 241, 0.15)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#8b5cf6',
        pointRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: '#94a3b8' } } },
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
        y: { min: 0, max: 100, ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });
}
