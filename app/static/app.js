// Shared helpers for the AI Career Guidance frontend

const SKILLS = [
  "academic_score", "programming", "databases", "problem_solving",
  "communication", "creativity", "teamwork", "analytical",
];

const INTERESTS = ["Technology", "AI/ML", "Data", "Design", "Business", "Cybersecurity"];
const PERSONALITY = ["Analytical", "Creative", "Social", "Independent", "Detail-oriented"];

async function api(path, method = "GET", body) {
  const opt = { method, headers: { "Content-Type": "application/json" } };
  if (body) opt.body = JSON.stringify(body);
  const r = await fetch(path, opt);
  let data = {};
  try { data = await r.json(); } catch (e) {}
  if (!r.ok) {
    const detail = data.detail;
    const msg = (typeof detail === "string") ? detail : (detail ? JSON.stringify(detail) : "Request failed");
    throw new Error(msg);
  }
  return data;
}

const toast = document.getElementById("toast");
let toastTimer;
function showToast(msg, ok = true) {
  if (!toast) return;
  toast.textContent = msg;
  toast.className = "toast " + (ok ? "ok" : "err");
  toast.style.display = "block";
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (toast.style.display = "none"), 3500);
}

function buildNav(active) {
  const pages = [
    ["/", "Home"],
    ["/register", "Register"],
    ["/recommendations", "Recommendations"],
    ["/students", "Students"],
  ];
  const nav = document.getElementById("nav");
  if (!nav) return;
  nav.innerHTML = `
    <div class="inner">
      <div class="brand">
        <span class="team">Hunters Algorithm</span>
        <span class="name">AI Career Guidance</span>
      </div>
      <div class="links">
        ${pages.map(([href, label]) =>
          `<a href="${href}" class="${href === active ? "active" : ""}">${label}</a>`
        ).join("")}
      </div>
    </div>`;
}

function buildChips(containerId, items) {
  const c = document.getElementById(containerId);
  if (!c) return;
  items.forEach((it) => {
    const lab = document.createElement("label");
    lab.innerHTML = `<input type="checkbox" value="${it}"><span>${it}</span>`;
    c.appendChild(lab);
  });
}

function renderRecommendations(list, boxId = "recommendations") {
  const box = document.getElementById(boxId);
  if (!box) return;
  box.innerHTML = "";
  if (!list || !list.length) {
    box.innerHTML = '<div class="empty">No recommendations yet. Generate them first!</div>';
    return;
  }
  list.forEach((r, i) => {
    const div = document.createElement("div");
    div.className = "rec" + (i === 0 ? " toprec" : "");
    div.innerHTML = `
      <div class="head">
        <div class="career"><span class="rank">${i + 1}</span>${r.career}</div>
        <div style="text-align:right">
          ${i === 0 ? '<div class="top-tag">Best Match</div>' : ""}
          <div class="badge">${r.match_percentage}%</div>
        </div>
      </div>
      <div class="bar ${i === 0 ? "top" : ""}"><div data-w="${r.match_percentage}"></div></div>
      <div class="reason">${r.reason}</div>
      <div class="cols">
        <div>
          <div class="col-title">Core Skills</div>
          ${r.skills.map((s) => `<span class="skill">${s}</span>`).join("")}
        </div>
        <div>
          <div class="col-title">Next Steps</div>
          ${r.next_steps.map((s) => `<div class="step">${s}</div>`).join("")}
        </div>
      </div>`;
    box.appendChild(div);
  });
  setTimeout(() => {
    box.querySelectorAll(".bar > div").forEach((b) => (b.style.width = b.dataset.w + "%"));
  }, 60);
}
