document.addEventListener("DOMContentLoaded", async () => {
  const subjectId = getSelectedSubject();
  loadStudyPlan(subjectId);

  const sel = document.getElementById("globalSubjectSelect");
  if (sel) {
    sel.value = subjectId;
    sel.addEventListener("change", (e) => {
      setSelectedSubject(e.target.value);
      loadStudyPlan(e.target.value);
    });
  }

  const hoursSlider = document.getElementById("dailyHoursSlider");
  if (hoursSlider) {
    hoursSlider.addEventListener("input", (e) => {
      document.getElementById("hoursDisplayValue").textContent = `${e.target.value} Hours/Day`;
      loadStudyPlan(getSelectedSubject(), 7, parseFloat(e.target.value));
    });
  }
});

async function loadStudyPlan(subjectId, daysLeft = 7, dailyHours = 3.0) {
  const plan = await APIClient.get(`/api/study-plan/${subjectId}?days_left=${daysLeft}&daily_hours=${dailyHours}`);
  if (!plan) return;

  const container = document.getElementById("studyPlanScheduleContainer");
  if (!container) return;

  container.innerHTML = plan.schedule.map(d => `
    <div class="card" style="margin-bottom: 1.25rem;">
      <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem; margin-bottom: 1rem;">
        <div>
          <span class="badge badge-high" style="margin-right: 8px;">Day ${d.day}</span>
          <strong style="font-size: 1.05rem;">${d.focus_topic}</strong>
          <span style="font-size: 0.8rem; color: var(--text-dim); margin-left: 8px;">(${d.date_str})</span>
        </div>
        <span class="badge badge-medium">${d.estimated_hours} Hours</span>
      </div>

      <div style="display: flex; flex-direction: column; gap: 0.65rem;">
        ${d.tasks.map((t, idx) => `
          <label style="display: flex; align-items: center; gap: 0.75rem; font-size: 0.9rem; cursor: pointer; padding: 0.4rem; border-radius: 6px; transition: background 0.2s;">
            <input type="checkbox" ${d.completed_tasks.includes(t) ? 'checked' : ''} onchange="toggleTaskState(this)" style="width: 18px; height: 18px; accent-color: var(--accent-primary);">
            <span style="${d.completed_tasks.includes(t) ? 'text-decoration: line-through; color: var(--text-dim);' : ''}">${t}</span>
          </label>
        `).join('')}
      </div>
    </div>
  `).join('');
}

function toggleTaskState(checkbox) {
  const span = checkbox.nextElementSibling;
  if (checkbox.checked) {
    span.style.textDecoration = "line-through";
    span.style.color = "var(--text-dim)";
  } else {
    span.style.textDecoration = "none";
    span.style.color = "var(--text-main)";
  }
}
