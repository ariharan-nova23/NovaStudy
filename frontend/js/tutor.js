document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("tutorChatForm");
  if (form) {
    form.addEventListener("submit", handleTutorSubmit);
  }
});

async function handleTutorSubmit(e) {
  if (e) e.preventDefault();
  const input = document.getElementById("tutorQueryInput");
  const query = input.value.trim();
  if (!query) return;

  appendMessage("user", query);
  input.value = "";

  const botBubble = appendMessage("assistant", "⏳ Thinking and searching syllabus & exam patterns...");

  const payload = {
    subject_id: getSelectedSubject(),
    query: query
  };

  const res = await APIClient.post("/api/tutor/query", payload);
  if (res && res.answer) {
    botBubble.innerHTML = formatMarkdown(res.answer);

    if (res.suggested_questions && res.suggested_questions.length > 0) {
      const pillsDiv = document.createElement("div");
      pillsDiv.style.marginTop = "1rem";
      pillsDiv.style.display = "flex";
      pillsDiv.style.flexWrap = "wrap";
      pillsDiv.style.gap = "0.5rem";

      res.suggested_questions.forEach(prompt => {
        const btn = document.createElement("button");
        btn.className = "btn btn-secondary";
        btn.style.fontSize = "0.8rem";
        btn.style.padding = "0.3rem 0.65rem";
        btn.textContent = `💡 ${prompt}`;
        btn.onclick = () => {
          document.getElementById("tutorQueryInput").value = prompt;
          handleTutorSubmit();
        };
        pillsDiv.appendChild(btn);
      });
      botBubble.appendChild(pillsDiv);
    }
  } else {
    botBubble.textContent = "Sorry, I couldn't process your question right now.";
  }
}

function appendMessage(sender, text) {
  const box = document.getElementById("tutorMessagesBox");
  if (!box) return;

  const msgDiv = document.createElement("div");
  msgDiv.style.display = "flex";
  msgDiv.style.justifyContent = sender === "user" ? "flex-end" : "flex-start";
  msgDiv.style.marginBottom = "1rem";

  const bubble = document.createElement("div");
  bubble.style.maxWidth = "80%";
  bubble.style.padding = "1rem 1.25rem";
  bubble.style.borderRadius = "16px";
  bubble.style.fontSize = "0.95rem";
  bubble.style.lineHeight = "1.6";

  if (sender === "user") {
    bubble.style.background = "linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))";
    bubble.style.color = "#ffffff";
  } else {
    bubble.style.background = "var(--bg-card)";
    bubble.style.border = "1px solid var(--border-color)";
    bubble.style.color = "var(--text-main)";
    bubble.innerHTML = formatMarkdown(text);
  }

  msgDiv.appendChild(bubble);
  box.appendChild(msgDiv);
  box.scrollTop = box.scrollHeight;
  return bubble;
}

function sendQuickPrompt(promptText) {
  document.getElementById("tutorQueryInput").value = promptText;
  handleTutorSubmit();
}

function formatMarkdown(txt) {
  if (!txt) return "";
  return txt
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}
