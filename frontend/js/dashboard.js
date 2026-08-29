document.addEventListener("DOMContentLoaded", async () => {
  const subjectId = getSelectedSubject();
  loadDashboardData(subjectId);

  const sel = document.getElementById("globalSubjectSelect");
  if (sel) {
    sel.value = subjectId;
    sel.addEventListener("change", (e) => {
      setSelectedSubject(e.target.value);
      loadDashboardData(e.target.value);
    });
  }
});

async function loadDashboardData(subjectId) {
  const data = await APIClient.get(`/api/dashboard/${subjectId}`);
  if (!data) return;

  // Render Metric Values
  document.getElementById("examCountdown").textContent = `${data.exam_days} Days`;
  document.getElementById("prepPercentage").textContent = `${data.preparation_percentage}%`;
  document.getElementById("prepProgressBar").style.width = `${data.preparation_percentage}%`;
  document.getElementById("totalPapers").textContent = data.total_papers_analyzed;
  document.getElementById("totalQuestions").textContent = data.total_questions_analyzed;
  document.getElementById("latestQuizScore").textContent = data.latest_quiz_score;

  // Render Priority Topics List
  const priorityListEl = document.getElementById("priorityTopicsList");
  if (priorityListEl) {
    priorityListEl.innerHTML = data.priority_topics.map(t => `
      <div class="priority-item">
        <div class="name">${t.name}</div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <span style="font-weight: 700; color: var(--accent-cyan);">${t.priority}</span>
          <span class="badge ${t.badge.includes('Critical') ? 'badge-critical' : 'badge-high'}">${t.badge}</span>
        </div>
      </div>
    `).join('');
  }

  // Render Recommendation
  const recEl = document.getElementById("recommendationText");
  if (recEl) {
    recEl.textContent = data.recommendation;
  }

  // Render Chart if Canvas exists
  renderDashboardChart();
}

function renderDashboardChart() {
  const ctx = document.getElementById("dashboardOverviewChart");
  if (!ctx || !window.Chart) return;

  if (window.myDashChart) window.myDashChart.destroy();

  window.myDashChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Graphs', 'Trees', 'Sorting', 'Stacks/Queues', 'Arrays/Memory'],
      datasets: [{
        data: [35, 25, 20, 15, 5],
        backgroundColor: ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans' } } }
      }
    }
  });
}
