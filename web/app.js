/* ═══ BA Prep — mirrors the Code Clash SQL practice UI exactly ═══ */

const state = {
  modules: [],
  currentModule: null,
  lessons: [],
  lesson: null,
  selectedLessonId: "",
  selectedTaskId: "",
  query: "",           // formula editor text
  selectedAnswer: null, // quiz MCQ index
  check: null,
  showSolution: false,
  loading: false,
  error: "",
  solved: loadJson("baPrepSolved"),
  savedDrafts: loadJson("baPrepDrafts"),
  savedAnswers: loadJson("baPrepAnswers"),
  taskTimes: loadJson("baPrepTaskTimes"),
  chapterStartTime: null,
  chapterStoppedMs: null,
  questionStartTime: null,
  timerId: null,
  autoCheckTimer: null,
  autoCheckSeq: 0,
  queryEditSeq: 0,
};

const app = document.querySelector("#app");
const MODULE_IDS = ["excel","powerbi","tableau","aptitude","case-study","leadership","data-interp"];

/* ═══ ROUTING ═══ */
function getRoute() {
  const p = window.location.pathname;
  if (p === "/" || p === "") return { page: "home" };
  for (const m of MODULE_IDS) {
    const re = new RegExp(`^/${m.replace("-","\\-")}(\\/([^/]+))?`);
    const match = p.match(re);
    if (match) return { page: "practice", module: m, lessonId: match[2] ? decodeURIComponent(match[2]) : "" };
  }
  return { page: "home" };
}

function navigate(path) { window.history.pushState({}, "", path); handleRoute(); }
window.addEventListener("popstate", handleRoute);

async function handleRoute() {
  const r = getRoute();
  if (r.page === "home") {
    state.currentModule = null; state.lesson = null; state.lessons = [];
    if (!state.modules.length) await loadModules();
    render();
  } else {
    state.currentModule = r.module;
    await loadLessons(r.module);
    if (r.lessonId) { 
      await loadLesson(r.module, r.lessonId, false); 
    } else if (state.lessons.length) {
      const last = loadJson("baPrepPosition")[r.module];
      const defaultLessonId = last?.lessonId || state.lessons[0]?.id || "";
      window.history.replaceState({}, "", `/${r.module}/${defaultLessonId}`);
      await loadLesson(r.module, defaultLessonId, false);
    }
  }
}

/* ═══ PERSISTENCE ═══ */
function loadJson(k) { try { return JSON.parse(localStorage.getItem(k) || "{}"); } catch { return {}; } }
function saveJson(k, v) { localStorage.setItem(k, JSON.stringify(v)); }
function saveSolved() { saveJson("baPrepSolved", state.solved); }
function saveDrafts() { saveJson("baPrepDrafts", state.savedDrafts); }
function saveAnswers() { saveJson("baPrepAnswers", state.savedAnswers); }
function saveTaskTimes() { saveJson("baPrepTaskTimes", state.taskTimes); }

function savePosition() {
  const pos = loadJson("baPrepPosition");
  pos[state.currentModule] = { lessonId: state.selectedLessonId, taskId: state.selectedTaskId };
  saveJson("baPrepPosition", pos);
}

function stateKey() { return `${state.currentModule}:${state.selectedLessonId}`; }

function saveDraftForTask() {
  const k = stateKey(), t = currentTask(); if (!t || !k) return;
  if (t.kind === "formula") {
    const q = state.query.trim(), starter = (t.starter || "").trim();
    state.savedDrafts[k] = state.savedDrafts[k] || {};
    if (q && q !== starter) state.savedDrafts[k][t.id] = state.query;
    else delete state.savedDrafts[k]?.[t.id];
    saveDrafts();
  } else {
    state.savedAnswers[k] = state.savedAnswers[k] || {};
    if (state.selectedAnswer != null) state.savedAnswers[k][t.id] = state.selectedAnswer;
    else delete state.savedAnswers[k]?.[t.id];
    saveAnswers();
  }
}

/* ═══ DATA LOADING ═══ */
async function loadModules() {
  try { const r = await fetch("/api/modules"); state.modules = (await r.json()).modules || []; }
  catch (e) { state.error = e.message; }
}

async function loadLessons(mod) {
  state.loading = true; render();
  try { const r = await fetch(`/api/${mod}/lessons`); state.lessons = (await r.json()).lessons || []; }
  catch (e) { state.error = e.message; }
  state.loading = false;
}

async function loadLesson(mod, lessonId, pushRoute = true) {
  if (!lessonId) return;
  state.loading = true; state.check = null; state.showSolution = false; render();
  try {
    const r = await fetch(`/api/${mod}/lessons/${encodeURIComponent(lessonId)}`);
    const d = await r.json();
    state.lesson = d.lesson; state.selectedLessonId = d.lesson.id;
    if (pushRoute) {
      const route = `/${mod}/${d.lesson.id}`;
      if (window.location.pathname !== route) window.history.pushState({}, "", route);
    }
    const last = loadJson("baPrepPosition")[mod];
    const resumeId = (last?.lessonId === d.lesson.id ? last?.taskId : "") || d.lesson.tasks[0]?.id || "";
    state.selectedTaskId = resumeId;
    state.chapterStartTime = Date.now(); state.chapterStoppedMs = null;
    startTimers(); setEditorFromTask();
  } catch (e) { state.error = e.message; }
  state.loading = false; render();
}

/* ═══ TASK LOGIC ═══ */
function currentTask() { return state.lesson?.tasks?.find(t => t.id === state.selectedTaskId) || null; }

function setEditorFromTask() {
  if (state.autoCheckTimer) { clearTimeout(state.autoCheckTimer); state.autoCheckTimer = null; }
  const t = currentTask(), k = stateKey();
  if (t?.kind === "formula") {
    state.query = state.savedDrafts[k]?.[t.id] ?? t.starter ?? "";
    state.selectedAnswer = null;
  } else {
    state.selectedAnswer = state.savedAnswers[k]?.[t?.id] ?? null;
    state.query = "";
  }
  state.check = null; state.showSolution = false;
  state.questionStartTime = Date.now(); savePosition();
}

function isTaskSolved(taskId) { return Boolean(state.solved[stateKey()]?.[taskId]); }
function markSolved(taskId) {
  const k = stateKey(); state.solved[k] = state.solved[k] || {};
  state.solved[k][taskId] = true; saveSolved();
}
function solvedCount(mod, lessonId) {
  const k = `${mod}:${lessonId}`, s = state.solved[k] || {};
  return Object.keys(s).filter(id => s[id]).length;
}
function totalLessonTime(mod, lessonId) {
  const v = Object.values(state.taskTimes[`${mod}:${lessonId}`] || {});
  return v.length ? v.reduce((a,b) => a+b, 0) : null;
}

function recordTime(taskId) {
  const k = stateKey(); if (!state.questionStartTime) return;
  const elapsed = Math.floor((Date.now() - state.questionStartTime) / 1000);
  state.taskTimes[k] = state.taskTimes[k] || {};
  if (!state.taskTimes[k][taskId]) { state.taskTimes[k][taskId] = elapsed; saveTaskTimes(); }
  if (state.lesson?.tasks?.every(t => isTaskSolved(t.id))) {
    state.chapterStoppedMs = chapterMs(); state.questionStartTime = null;
  }
}

function getTaskTime(taskId) { return state.taskTimes[stateKey()]?.[taskId] || null; }

function nextTaskId() {
  const tasks = state.lesson?.tasks || [];
  const idx = tasks.findIndex(t => t.id === state.selectedTaskId);
  if (idx === -1) return "";
  const later = tasks.slice(idx + 1).find(t => !isTaskSolved(t.id));
  return later?.id || tasks[idx + 1]?.id || "";
}

function advanceTask() {
  const nid = nextTaskId(); if (!nid) return false;
  state.selectedTaskId = nid; setEditorFromTask(); return true;
}

function resetChapter() {
  const k = stateKey();
  delete state.solved[k]; delete state.taskTimes[k];
  delete state.savedDrafts[k]; delete state.savedAnswers[k];
  saveSolved(); saveTaskTimes(); saveDrafts(); saveAnswers();
  state.chapterStartTime = Date.now(); state.chapterStoppedMs = null;
  state.selectedTaskId = state.lesson?.tasks?.[0]?.id || "";
  setEditorFromTask(); startTimers(); render();
}

/* ═══ TIMERS ═══ */
function chapterMs() { return state.chapterStoppedMs != null ? state.chapterStoppedMs : (state.chapterStartTime ? Date.now() - state.chapterStartTime : 0); }
function questionMs() { return state.questionStartTime ? Date.now() - state.questionStartTime : 0; }
function fmtTime(ms) {
  const s = Math.floor(ms/1000), m = Math.floor(s/60), sec = s%60, h = Math.floor(m/60);
  if (h > 0) return `${h}:${String(m%60).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
  return `${m}:${String(sec).padStart(2,"0")}`;
}
function fmtCompact(sec) { if (sec == null) return ""; const m = Math.floor(sec/60), s = sec%60; return m > 0 ? `${m}m ${s}s` : `${s}s`; }
function startTimers() { stopTimers(); state.timerId = setInterval(tickTimers, 1000); }
function stopTimers() { if (state.timerId) { clearInterval(state.timerId); state.timerId = null; } }
function tickTimers() {
  const ch = document.querySelector("[data-ch-timer]"); if (ch) ch.textContent = fmtTime(chapterMs());
  const q = document.querySelector("[data-q-timer]"); if (q) q.textContent = fmtTime(questionMs());
}

/* ═══ CHECK ═══ */
async function checkCurrentTask() {
  const task = currentTask(); if (!task) return;
  state.error = ""; let advanced = false;
  try {
    const payload = { lessonId: state.selectedLessonId, taskId: task.id };
    payload.answer = task.kind === "quiz" ? state.selectedAnswer : state.query;
    const r = await fetch(`/api/${state.currentModule}/check`, {
      method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload),
    });
    const d = await r.json();
    if (!d.ok) throw new Error(d.error || "Check failed.");
    state.check = d;
    if (d.correct) {
      markSolved(task.id); recordTime(task.id);
      if (task.kind === "formula") { delete state.savedDrafts[stateKey()]?.[task.id]; saveDrafts(); }
      advanced = advanceTask();
    }
  } catch (e) { state.error = e.message; }
  render();
}

function scheduleAutoCheck() {
  if (state.autoCheckTimer) clearTimeout(state.autoCheckTimer);
  const q = state.query.trim(); if (!q || !currentTask()) return;
  const seq = ++state.autoCheckSeq;
  state.autoCheckTimer = setTimeout(async () => {
    const task = currentTask(); if (!task || task.kind !== "formula") return;
    try {
      const r = await fetch(`/api/${state.currentModule}/check`, {
        method: "POST", headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ lessonId: state.selectedLessonId, taskId: task.id, answer: state.query }),
      });
      const d = await r.json(); if (seq !== state.autoCheckSeq) return;
      state.check = d;
      if (d.correct) { markSolved(task.id); recordTime(task.id); advanceTask(); }
      else { state.check = { correct: false, message: "Not solved yet." }; }
    } catch { /* silent */ }
    render();
  }, 850);
}

/* ═══ ESCAPING ═══ */
function esc(s) { return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }

/* ═══ RENDER ═══ */
function render() {
  const editor = document.querySelector("#formulaEditor");
  const hadFocus = editor && document.activeElement === editor;
  const savedSel = hadFocus ? { start: editor.selectionStart, end: editor.selectionEnd } : null;

  app.innerHTML = `
    ${renderTopbar()}
    ${state.error ? `<div class="notice"><span>${esc(state.error)}</span><button data-action="dismiss">Dismiss</button></div>` : ""}
    <main class="shell">${renderMain()}</main>
    <p class="footer-note">${state.currentModule ? "Practice with real data. Write formulas, solve problems, and check your answers." : "Comprehensive BA interview preparation covering 7 skill areas."}</p>
  `;

  if (savedSel) {
    const el = document.querySelector("#formulaEditor");
    if (el) { el.focus(); el.setSelectionRange(Math.min(savedSel.start, el.value.length), Math.min(savedSel.end, el.value.length)); }
  }
}

function renderTopbar() {
  const mod = state.currentModule;
  const modInfo = state.modules.find(m => m.id === mod);
  return `<header class="topbar">
    <div class="brand">
      <div style="width:44px;height:44px;border-radius:8px;background:linear-gradient(135deg,#00a676,#2ec4b6);display:grid;place-items:center;color:#fff;font-weight:900;font-size:1.1rem;flex-shrink:0">BA</div>
      <div>
        <h1>BA Prep</h1>
        <p>${mod ? esc(modInfo?.title || mod) + " Practice" : "Business Analyst Interview Prep"}</p>
      </div>
    </div>
    <div class="top-actions">
      <button class="nav-button ${!mod ? 'active' : ''}" data-action="go-home">Home</button>
      ${mod ? `<div class="nav-dropdown">
        <span class="nav-dropdown-trigger active">Practice</span>
        <div class="nav-dropdown-menu">
          ${state.modules.map(m => `<button class="nav-dropdown-item ${m.id === mod ? 'active' : ''}" data-action="switch-module" data-module="${esc(m.id)}">${m.icon} ${esc(m.title)}</button>`).join("")}
        </div>
      </div>` : ""}
    </div>
  </header>`;
}

function renderMain() {
  if (state.currentModule) return renderPractice();
  return renderHome();
}

function renderHome() {
  return `<section class="home-hero"><h2>BA Prep</h2>
    <p>Excel, Power BI, Tableau, Aptitude, Case Studies, Leadership Principles, and Data Interpretation.</p></section>
    <div class="module-grid">${state.modules.map(m => `
      <button class="module-card" data-action="open-module" data-module="${esc(m.id)}">
        <div class="module-card-head"><span class="module-icon">${m.icon}</span><h3>${esc(m.title)}</h3></div>
        <p>${esc(m.desc)}</p>
      </button>`).join("")}</div>`;
}

/* ═══ PRACTICE (mirrors SQL practice exactly) ═══ */
function renderPractice() {
  if (!state.lesson && state.loading) return `<section class="sql-shell"><div class="sql-workspace"><div class="empty">Loading practice.</div></div></section>`;
  if (!state.lesson) return `<section class="sql-shell"><div class="sql-workspace"><div class="empty">Choose a chapter.</div></div></section>`;
  return `<section class="sql-shell">${renderSidebar()}${renderWorkspace()}</section>`;
}

function renderSidebar() {
  const mod = state.currentModule;
  const modInfo = state.modules.find(m => m.id === mod);
  return `<aside class="sql-sidebar" aria-label="Chapters">
    <div class="sql-sidebar-head">
      <p class="eyebrow">${esc(modInfo?.title || mod)}</p>
      <h2>Chapters</h2>
    </div>
    <div class="sql-chapter-list">
      ${state.lessons.map(l => {
        const sc = solvedCount(mod, l.id);
        const tt = totalLessonTime(mod, l.id);
        return `<button class="sql-chapter ${state.selectedLessonId === l.id ? 'active' : ''}" data-action="open-lesson" data-lesson-id="${esc(l.id)}">
          <span>${l.number}</span>
          <b>${esc(l.title)}</b>
          <small>${sc}/${l.taskCount}${tt != null ? ` · ${fmtCompact(tt)}` : ""}</small>
        </button>`;
      }).join("")}
    </div>
  </aside>`;
}

function renderWorkspace() {
  return `<section class="sql-workspace">
    <div class="sql-lesson-head">
      <div>
        <p class="eyebrow">Chapter ${state.lesson.number}</p>
        <h2>${esc(state.lesson.title)}</h2>
      </div>
      <div class="lesson-tools">
        <div class="sql-chapter-timer-block${state.chapterStoppedMs != null ? ' stopped' : ''}">
          <span class="sql-timer-icon">⏱</span>
          <span class="sql-timer-value" data-ch-timer>${fmtTime(chapterMs())}</span>
          <button class="sql-timer-reset" data-action="reset-chapter" title="Reset chapter">↻</button>
        </div>
        <div class="question-meta">
          ${state.lesson.focus.map(f => `<span class="pill">${esc(f)}</span>`).join("")}
        </div>
      </div>
    </div>
    <div class="sql-grid">
      <div class="sql-left">${renderTables()}</div>
      <div class="sql-right">
        ${renderTaskList()}
        ${renderEditor()}
        ${renderFeedback()}
      </div>
    </div>
  </section>`;
}

function renderTables() {
  const task = currentTask();
  const tables = task?.tables?.length ? task.tables : state.lesson.tables;
  if (!tables?.length) return "";
  return `<section class="sql-panel">
    <div class="sql-panel-head">
      <h3>Data</h3>
      <button class="secondary-button compact" data-action="reset-query">Reset</button>
    </div>
    <div class="sql-table-stack">
      ${tables.map((t, idx) => `<article class="data-table-card">
        <div class="data-table-title">
          <b>${esc(t.name)}</b>
          <div style="display:flex;gap:8px;align-items:center">
            <button class="copy-table-btn" data-action="copy-table" data-idx="${idx}" title="Copy for Excel/Sheets">Copy</button>
            <span>${t.total} rows</span>
          </div>
        </div>
        <div class="data-table-wrap"><table>
          <thead><tr>${t.columns.map(c => `<th>${esc(c)}</th>`).join("")}</tr></thead>
          <tbody>${t.rows.map(r => `<tr>${r.map(v => `<td>${esc(v ?? "NULL")}</td>`).join("")}</tr>`).join("")}</tbody>
        </table></div>
      </article>`).join("")}
    </div>
  </section>`;
}

async function copyTable(idx) {
  const task = currentTask();
  const tables = task?.tables?.length ? task.tables : state.lesson.tables;
  const t = tables[idx];
  if (!t) return;

  // Format as TSV (Tab Separated Values) for perfect pasting in Excel/Sheets
  const header = t.columns.join("\t");
  const body = t.rows.map(r => r.map(v => v ?? "").join("\t")).join("\n");
  const tsv = header + "\n" + body;

  try {
    await navigator.clipboard.writeText(tsv);
    const btn = document.querySelector(`[data-action="copy-table"][data-idx="${idx}"]`);
    if (btn) {
      const old = btn.textContent;
      btn.textContent = "Copied!";
      btn.classList.add("copied");
      setTimeout(() => { 
        btn.textContent = old; 
        btn.classList.remove("copied");
      }, 2000);
    }
  } catch (e) {
    state.error = "Clipboard access denied.";
    render();
  }
}

function renderTaskList() {
  return `<section class="sql-panel task-panel">
    <div class="sql-panel-head">
      <h3>Exercises</h3>
      <span class="pill strong">${solvedCount(state.currentModule, state.lesson.id)}/${state.lesson.tasks.length} solved</span>
    </div>
    <div class="sql-task-list">
      ${state.lesson.tasks.map((t, i) => {
        const time = getTaskTime(t.id);
        return `<button class="sql-task ${t.id === state.selectedTaskId ? 'active' : ''} ${isTaskSolved(t.id) ? 'solved' : ''}" data-action="select-task" data-task-id="${esc(t.id)}">
          <span>${isTaskSolved(t.id) ? "✓" : i + 1}</span>
          <b>${esc(t.prompt)}</b>
          ${time != null ? `<small class="task-time">${fmtCompact(time)}</small>` : ""}
        </button>`;
      }).join("")}
    </div>
  </section>`;
}

function renderEditor() {
  const task = currentTask();
  if (!task) return "";
  if (task.kind === "quiz") return renderQuizEditor(task);
  return renderFormulaEditor(task);
}

function renderFormulaEditor(task) {
  return `<section class="sql-panel editor-panel">
    <div class="sql-panel-head">
      <h3>${esc(task.prompt)}</h3>
      <div class="editor-actions">
        <div class="sql-question-timer-block">
          <span class="sql-timer-icon">⏱</span>
          <span class="sql-timer-value" data-q-timer>${fmtTime(questionMs())}</span>
        </div>
        <button class="secondary-button compact" data-action="show-solution">${state.showSolution ? "Hide Solution" : "Solution"}</button>
        <button class="secondary-button compact" data-action="reset-query">Reset</button>
        <button class="primary-button compact" data-action="check-answer">Check</button>
      </div>
    </div>
    <textarea id="formulaEditor" spellcheck="false">${esc(state.query)}</textarea>
    ${task.hint ? `<p class="sql-hint">${esc(task.hint)}</p>` : ""}
  </section>`;
}

function renderQuizEditor(task) {
  const labels = ["A","B","C","D"];
  const checked = state.check;
  return `<section class="sql-panel">
    <div class="sql-panel-head">
      <h3>${esc(task.prompt)}</h3>
      <div class="editor-actions">
        <div class="sql-question-timer-block">
          <span class="sql-timer-icon">⏱</span>
          <span class="sql-timer-value" data-q-timer>${fmtTime(questionMs())}</span>
        </div>
        <button class="secondary-button compact" data-action="reset-query">Reset</button>
        <button class="primary-button compact" data-action="check-answer">Check</button>
      </div>
    </div>
    ${task.hint ? `<p class="sql-hint">${esc(task.hint)}</p>` : ""}
    <div class="quiz-options">
      ${task.options.map((opt, i) => {
        const selected = state.selectedAnswer === i;
        const isCorrect = checked?.expectedIndex === i;
        const wrongSel = checked && !checked.correct && selected && !isCorrect;
        const cls = ["quiz-option",
          selected && !checked ? "selected" : "",
          checked?.correct && selected ? "correct" : "",
          checked && !checked.correct && isCorrect ? "reveal-correct" : "",
          wrongSel ? "wrong" : "",
        ].filter(Boolean).join(" ");
        return `<button class="${cls}" data-action="pick-option" data-idx="${i}">
          <span class="quiz-option-key">${labels[i]}</span>
          <span>${esc(opt)}</span>
        </button>`;
      }).join("")}
    </div>
  </section>`;
}

function renderFeedback() {
  if (!state.check && !state.showSolution) {
    return `<section class="sql-panel"><div class="empty compact-empty">Write your formula and click Check, or select an answer.</div></section>`;
  }
  const task = currentTask();
  return `<section class="feedback ${state.check?.correct ? 'correct' : state.check ? 'wrong' : ''}">
    ${state.check ? esc(state.check.message) : ""}
    ${state.check?.explanation ? `<br><br>${esc(state.check.explanation)}` : ""}
    ${(state.showSolution || state.check) && state.check?.solution ? `<pre>${esc(state.check.solution)}</pre>` : ""}
    ${state.showSolution && !state.check?.solution && task ? `<pre>Click Check to reveal the solution.</pre>` : ""}
  </section>`;
}

/* ═══ EVENT HANDLING ═══ */
document.addEventListener("click", async (e) => {
  const btn = e.target.closest("[data-action]");
  if (!btn) return;
  const action = btn.dataset.action;
  switch (action) {
    case "go-home": navigate("/"); break;
    case "open-module": navigate(`/${btn.dataset.module}`); break;
    case "switch-module": navigate(`/${btn.dataset.module}`); break;
    case "open-lesson": await loadLesson(state.currentModule, btn.dataset.lessonId); break;
    case "copy-table": await copyTable(parseInt(btn.dataset.idx)); break;
    case "select-task":
      saveDraftForTask();
      state.selectedTaskId = btn.dataset.taskId;
      setEditorFromTask(); render(); break;
    case "pick-option":
      if (!state.check) { state.selectedAnswer = parseInt(btn.dataset.idx); render(); } break;
    case "check-answer": await checkCurrentTask(); break;
    case "reset-query": {
      const t = currentTask();
      if (t?.kind === "formula") { state.query = t.starter || ""; } else { state.selectedAnswer = null; }
      state.check = null; state.showSolution = false; saveDraftForTask(); render(); break;
    }
    case "show-solution": state.showSolution = !state.showSolution; render(); break;
    case "reset-chapter": resetChapter(); break;
    case "dismiss": state.error = ""; render(); break;
  }
});

document.addEventListener("input", (e) => {
  if (e.target.id === "formulaEditor") {
    state.query = e.target.value;
    state.queryEditSeq++;
    saveDraftForTask();
    scheduleAutoCheck();
  }
});

document.addEventListener("keydown", (e) => {
  if (e.target.id === "formulaEditor" && e.key === "Tab") {
    e.preventDefault();
    const el = e.target, start = el.selectionStart;
    el.value = el.value.substring(0, start) + "  " + el.value.substring(el.selectionEnd);
    el.selectionStart = el.selectionEnd = start + 2;
    state.query = el.value;
  }
});

/* ═══ INIT ═══ */
handleRoute();
