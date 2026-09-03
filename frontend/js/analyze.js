document.addEventListener("DOMContentLoaded", async () => {

  // Load subjects into the existing subject dropdown first
  await loadSubjects();

  const subjectId = getSelectedSubject();


  // Keep the dropdown synchronized with the selected subject
  const sel =
    document.getElementById("globalSubjectSelect");


  if (sel) {

    if (subjectId) {
      sel.value = subjectId;
    }


    sel.addEventListener("change", async (e) => {

      const newSubjectId =
        e.target.value;

      if (!newSubjectId) return;

      setSelectedSubject(newSubjectId);

      await loadAnalysisData(
        newSubjectId
      );

    });

  }


  // Upload form
  const uploadForm =
    document.getElementById(
      "paperUploadForm"
    );


  if (uploadForm) {

    uploadForm.addEventListener(
      "submit",
      handlePaperUpload
    );

  }


  // Load initial analysis
  if (subjectId) {

    await loadAnalysisData(
      subjectId
    );

  }

});



/* =========================================================
   SUBJECTS
   ========================================================= */

async function loadSubjects() {

  const sel =
    document.getElementById(
      "globalSubjectSelect"
    );


  if (!sel) return;


  try {

    const subjects =
      await APIClient.get(
        "/api/subjects"
      );


    /*
     * APIClient.get() returns null
     * when the request fails.
     */

    if (
      !Array.isArray(subjects) ||
      subjects.length === 0
    ) {

      sel.innerHTML = `
        <option value="">
          No subjects available
        </option>
      `;

      return;

    }


    /*
     * Build the dropdown dynamically
     * from the backend.
     */

    sel.innerHTML =
      subjects
        .map(subject => `
          <option value="${escapeHtml(subject.id)}">
            ${escapeHtml(subject.name)}
          </option>
        `)
        .join("");


    /*
     * Try to restore the previously
     * selected subject.
     */

    const savedSubject =
      localStorage.getItem(
        "smart_exam_subject"
      );


    const savedExists =
      subjects.some(
        subject =>
          subject.id === savedSubject
      );


    if (savedExists) {

      sel.value =
        savedSubject;

    } else {

      /*
       * If no saved subject exists,
       * use the first subject.
       */

      sel.value =
        subjects[0].id;


      setSelectedSubject(
        subjects[0].id
      );

    }

  } catch (error) {

    console.error(
      "Failed to load subjects:",
      error
    );


    sel.innerHTML = `
      <option value="">
        Unable to load subjects
      </option>
    `;

  }

}



/* =========================================================
   LOAD ANALYSIS DATA
   ========================================================= */

async function loadAnalysisData(
  subjectId
) {

  if (!subjectId) {

    console.warn(
      "loadAnalysisData called without subjectId"
    );

    return;

  }


  try {

    /*
     * Load all three analysis resources
     * together.
     */

    const [
      patterns,
      repeated,
      questionsData
    ] = await Promise.all([

      APIClient.get(
        `/api/analysis/patterns/${subjectId}`
      ),

      APIClient.get(
        `/api/analysis/repeated/${subjectId}`
      ),

      APIClient.get(
        `/api/analysis/questions/${subjectId}`
      )

    ]);


    if (patterns) {

      renderPatternCharts(
        patterns
      );

    }


    if (repeated) {

      renderRepeatedQuestionsTable(
        repeated.repeated_groups || []
      );

    }


    if (questionsData) {

      renderExtractedQuestions(
        questionsData.questions || []
      );

    }

  } catch (error) {

    console.error(
      "Failed to load analysis data:",
      error
    );

  }

}



/* =========================================================
   PAPER / STUDY MATERIAL UPLOAD
   ========================================================= */

async function handlePaperUpload(e) {

  e.preventDefault();


  // -----------------------------------------
  // Get form elements
  // -----------------------------------------

  const fileInput =
    document.getElementById(
      "paperFileInput"
    );


  const yearInput =
    document.getElementById(
      "paperYearInput"
    );


  const uploadTypeInput =
    document.getElementById(
      "uploadType"
    );


  const statusEl =
    document.getElementById(
      "uploadStatusMessage"
    );


  // -----------------------------------------
  // Validate file
  // -----------------------------------------

  if (
    !fileInput ||
    !fileInput.files ||
    fileInput.files.length === 0
  ) {

    alert(
      "Please select a PDF or image file."
    );

    return;

  }


  // -----------------------------------------
  // Get selected subject
  // -----------------------------------------

  const subjectId =
    getSelectedSubject();


  if (!subjectId) {

    alert(
      "Please select a subject first."
    );

    return;

  }


  // -----------------------------------------
  // Get upload type
  // -----------------------------------------

  const uploadType =
    uploadTypeInput
      ? uploadTypeInput.value
      : "question_paper";


  // -----------------------------------------
  // Show processing status
  // -----------------------------------------

  if (statusEl) {

    statusEl.style.display =
      "block";


    if (
      uploadType ===
      "study_material"
    ) {

      statusEl.innerHTML = `
        <span style="color: var(--accent-cyan);">
          ⏳ Processing study material
          & extracting useful questions/topics...
        </span>
      `;

    } else {

      statusEl.innerHTML = `
        <span style="color: var(--accent-cyan);">
          ⏳ Processing previous question paper
          & running question extraction engine...
        </span>
      `;

    }

  }


  // -----------------------------------------
  // Build multipart form data
  // -----------------------------------------

  const formData =
    new FormData();


  // File
  formData.append(
    "file",
    fileInput.files[0]
  );


  // Subject
  formData.append(
    "subject_id",
    subjectId
  );


  // Year
  formData.append(
    "year",
    yearInput && yearInput.value
      ? yearInput.value
      : new Date().getFullYear()
  );


  // ⭐ Upload type
  formData.append(
    "upload_type",
    uploadType
  );


  // -----------------------------------------
  // Send to backend
  // -----------------------------------------

  try {

    const res =
      await APIClient.upload(
        "/api/upload/paper",
        formData
      );


    console.log(
      "Document upload response:",
      res
    );


    // -----------------------------------------
    // SUCCESS
    // -----------------------------------------

    if (
      res &&
      res.status === "success"
    ) {

      if (statusEl) {

        const typeMessage =
          uploadType ===
          "study_material"
            ? "study material"
            : "previous question paper";


        statusEl.innerHTML = `
          <span style="color: var(--accent-emerald);">
            ✓ Successfully processed
            ${res.extracted_questions_count || 0}
            questions from
            ${typeMessage}!
          </span>
        `;

      }


      /*
       * Refresh the analysis using
       * the same subject.
       */

      await loadAnalysisData(
        subjectId
      );


      /*
       * Clear selected file.
       */

      fileInput.value = "";

    }


    // -----------------------------------------
    // UNEXPECTED RESPONSE
    // -----------------------------------------

    else {

      if (statusEl) {

        statusEl.innerHTML = `
          <span style="color: var(--accent-rose);">
            ❌ Failed to process document.
            Please check the file format
            and selected subject.
          </span>
        `;

      }


      console.error(
        "Unexpected upload response:",
        res
      );

    }

  } catch (error) {

    console.error(
      "Document upload failed:",
      error
    );


    if (statusEl) {

      statusEl.innerHTML = `
        <span style="color: var(--accent-rose);">
          ❌ ${
            error.message ||
            "Failed to process document."
          }
        </span>
      `;

    }

  }

}



/* =========================================================
   PATTERN CHARTS
   ========================================================= */

function renderPatternCharts(
  patterns
) {

  if (!patterns) return;


  /* =======================================================
     UNIT DISTRIBUTION
     ======================================================= */

  const unitCtx =
    document.getElementById(
      "unitDistChart"
    );


  if (
    unitCtx &&
    window.Chart
  ) {

    if (window.myUnitChart) {

      window.myUnitChart.destroy();

    }


    const unitDistribution =
      patterns.unit_distribution ||
      {};


    window.myUnitChart =
      new Chart(
        unitCtx,
        {

          type: "bar",

          data: {

            labels:
              Object.keys(
                unitDistribution
              ),

            datasets: [
              {

                label:
                  "Unit Distribution (%)",

                data:
                  Object.values(
                    unitDistribution
                  ),

                backgroundColor: [
                  "#6366f1",
                  "#8b5cf6",
                  "#06b6d4",
                  "#10b981",
                  "#f59e0b"
                ],

                borderRadius: 8

              }

            ]

          },


          options: {

            responsive: true,


            plugins: {

              legend: {
                display: false
              }

            },


            scales: {

              x: {

                ticks: {
                  color: "#94a3b8"
                },

                grid: {
                  color:
                    "rgba(255,255,255,0.05)"
                }

              },


              y: {

                ticks: {
                  color: "#94a3b8"
                },

                grid: {
                  color:
                    "rgba(255,255,255,0.05)"
                }

              }

            }

          }

        }

      );

  }



  /* =======================================================
     QUESTION TYPE DISTRIBUTION
     ======================================================= */

  const typeCtx =
    document.getElementById(
      "typeDistChart"
    );


  if (
    typeCtx &&
    window.Chart
  ) {

    if (window.myTypeChart) {

      window.myTypeChart.destroy();

    }


    const typeDistribution =
      patterns.question_type_distribution ||
      {};


    window.myTypeChart =
      new Chart(
        typeCtx,
        {

          type: "doughnut",

          data: {

            labels:
              Object.keys(
                typeDistribution
              ),

            datasets: [
              {

                data:
                  Object.values(
                    typeDistribution
                  ),

                backgroundColor: [
                  "#6366f1",
                  "#06b6d4",
                  "#10b981",
                  "#f59e0b",
                  "#ec4899",
                  "#8b5cf6"
                ]

              }

            ]

          },


          options: {

            responsive: true,


            plugins: {

              legend: {

                position: "right",

                labels: {
                  color: "#94a3b8"
                }

              }

            }

          }

        }

      );

  }

}



/* =========================================================
   REPEATED QUESTIONS TABLE
   ========================================================= */

function renderRepeatedQuestionsTable(
  groups
) {

  const tableBody =
    document.getElementById(
      "repeatedQuestionsTableBody"
    );


  if (!tableBody) return;


  if (
    !groups ||
    groups.length === 0
  ) {

    tableBody.innerHTML = `
      <tr>

        <td
          colspan="5"
          style="
            text-align:center;
            padding:2rem;
            color:var(--text-dim);
          "
        >
          No repeated questions found yet.
        </td>

      </tr>
    `;

    return;

  }


  tableBody.innerHTML =
    groups
      .map(g => {

        const years =
          Array.isArray(
            g.appeared_in_years
          )
            ? g.appeared_in_years
            : [];


        const priority =
          g.priority ||
          "Normal";


        let priorityClass =
          "badge-high";


        if (
          priority.includes(
            "Very High"
          )
        ) {

          priorityClass =
            "badge-critical";

        }


        return `

          <tr>

            <td>

              <strong
                style="
                  color:var(--text-main);
                  font-size:0.95rem;
                "
              >
                ${escapeHtml(
                  g.concept ||
                  "Unknown"
                )}
              </strong>


              <div
                style="
                  font-size:0.8rem;
                  color:var(--text-dim);
                  margin-top:0.2rem;
                "
              >

                ${escapeHtml(
                  g.unit ||
                  ""
                )}

                •

                ${escapeHtml(
                  g.topic ||
                  ""
                )}

              </div>

            </td>


            <td>

              ${years
                .map(
                  year => `

                    <span
                      class="badge badge-medium"
                      style="
                        margin-right:4px;
                      "
                    >

                      ${escapeHtml(
                        String(year)
                      )}

                    </span>

                  `
                )
                .join("")}

            </td>


            <td>

              <strong
                style="
                  color:var(--accent-amber);
                "
              >

                ${g.frequency || 0}/
                ${g.total_papers || 0}
                Papers

              </strong>

              (${g.total_marks || 0}
              Marks)

            </td>


            <td>

              <span
                style="
                  font-size:0.85rem;
                  font-weight:600;
                "
              >

                ${escapeHtml(
                  g.trend ||
                  "—"
                )}

              </span>

            </td>


            <td>

              <span
                class="badge ${priorityClass}"
              >

                ${escapeHtml(
                  priority
                )}

              </span>

            </td>

          </tr>

        `;

      })
      .join("");

}



/* =========================================================
   EXTRACTED QUESTIONS
   ========================================================= */

function renderExtractedQuestions(
  questions
) {

  const listEl =
    document.getElementById(
      "extractedQuestionsList"
    );


  if (!listEl) return;


  if (
    !questions ||
    questions.length === 0
  ) {

    listEl.innerHTML = `
      <div
        style="
          padding:2rem;
          text-align:center;
          color:var(--text-dim);
        "
      >
        No extracted questions found.
      </div>
    `;

    return;

  }


  listEl.innerHTML =
    questions
      .map(
        (q, idx) => {

          const year =
            q.year ||
            "—";


          const marks =
            q.marks ||
            "—";


          const unit =
            q.unit ||
            "Unknown Unit";


          const topic =
            q.topic ||
            "Unknown Topic";


          const subtopic =
            q.subtopic ||
            "Unknown Subtopic";


          const questionType =
            q.question_type ||
            "Unknown";


          return `

            <div
              style="
                padding:1rem;
                background:
                  rgba(255,255,255,0.02);
                border:
                  1px solid
                  var(--border-color);
                border-radius:12px;
                margin-bottom:0.75rem;
              "
            >

              <div
                style="
                  display:flex;
                  align-items:center;
                  justify-content:space-between;
                  margin-bottom:0.5rem;
                  gap:1rem;
                "
              >

                <span
                  style="
                    font-size:0.8rem;
                    font-weight:700;
                    color:
                      var(--accent-cyan);
                  "
                >

                  Q${idx + 1}

                  (${escapeHtml(
                    String(year)
                  )})

                  •

                  ${escapeHtml(
                    String(marks)
                  )}

                  Marks

                </span>


                <div>

                  <span
                    class="badge badge-medium"
                    style="
                      margin-right:4px;
                    "
                  >

                    ${escapeHtml(
                      unit
                    )}

                  </span>


                  <span
                    class="badge badge-low"
                  >

                    ${escapeHtml(
                      questionType
                    )}

                  </span>


                  ${
                    q.needs_review
                      ? `
                        <span
                          class="
                            badge
                            badge-critical
                          "
                        >
                          Needs Review
                        </span>
                      `
                      : ""
                  }

                </div>

              </div>


              <div
                style="
                  font-size:0.95rem;
                  font-weight:500;
                  color:var(--text-main);
                "
              >

                ${escapeHtml(
                  q.question ||
                  ""
                )}

              </div>


              <div
                style="
                  font-size:0.8rem;
                  color:var(--text-dim);
                  margin-top:0.4rem;
                "
              >

                Topic:

                ${escapeHtml(
                  topic
                )}

                ›

                ${escapeHtml(
                  subtopic
                )}

              </div>

            </div>

          `;

        }
      )
      .join("");

}



/* =========================================================
   HTML ESCAPING
   ========================================================= */

function escapeHtml(
  value
) {

  return String(
    value ?? ""
  )

    .replace(
      /&/g,
      "&amp;"
    )

    .replace(
      /</g,
      "&lt;"
    )

    .replace(
      />/g,
      "&gt;"
    )

    .replace(
      /"/g,
      "&quot;"
    )

    .replace(
      /'/g,
      "&#039;"
    );

}