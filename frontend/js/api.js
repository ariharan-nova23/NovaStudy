/* Centralized API Client for SmartExam AI */
const API_BASE_URL = window.location.origin;

class APIClient {
  static async get(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
      return await response.json();
    } catch (error) {
      console.warn(`GET ${endpoint} failed:`, error);
      return null;
    }
  }

  static async post(endpoint, body) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
      return await response.json();
    } catch (error) {
      console.warn(`POST ${endpoint} failed:`, error);
      return null;
    }
  }

 static async upload(endpoint, formData) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      body: formData
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(
        data.detail || data.message || `HTTP Error ${response.status}`
      );
    }

    return data;
  } catch (error) {
    console.error(`UPLOAD ${endpoint} failed:`, error);
    throw error;
  }
}
}

// Active subject helper
function getSelectedSubject() {
  const sel = document.getElementById("globalSubjectSelect");
  return sel ? sel.value : (localStorage.getItem("smart_exam_subject") || "dsa");
}

function setSelectedSubject(subjectId) {
  localStorage.setItem("smart_exam_subject", subjectId);
}
