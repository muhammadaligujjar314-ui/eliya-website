function saveGoalData(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}

function loadGoalData(key, fallback) {
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : fallback;
}

function renderGrid(containerId, days, checkedDays, onToggle) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  for (let i = 1; i <= days; i++) {
    const box = document.createElement("div");
    box.className = "grid-box" + (checkedDays.includes(i) ? " checked" : "");
    box.textContent = i;
    box.onclick = () => onToggle(i);
    container.appendChild(box);
  }
}

// ---------- Progress Gauge (Sui) ----------
function renderGauge(containerId, percent) {
  percent = Math.max(0, Math.min(100, percent));
  const angle = (percent / 100) * 180; // 0 to 180 degrees
  const rad = (angle * Math.PI) / 180;
  const cx = 100, cy = 100, r = 80;
  const needleX = cx - r * Math.cos(rad);
  const needleY = cy - r * Math.sin(rad);

  const svg = `
    <svg viewBox="0 0 200 120" class="gauge-svg">
      <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#E0E0E0" stroke-width="14" stroke-linecap="round"/>
      <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="var(--sage)" stroke-width="14"
            stroke-linecap="round" stroke-dasharray="${(percent/100)*251.2} 251.2"/>
      <line x1="${cx}" y1="${cy}" x2="${needleX}" y2="${needleY}" stroke="var(--dark-sage)" stroke-width="3"/>
      <circle cx="${cx}" cy="${cy}" r="6" fill="var(--dark-sage)"/>
      <text x="100" y="115" text-anchor="middle" font-size="16" fill="var(--dark-sage)" font-weight="bold">${percent.toFixed(0)}%</text>
    </svg>`;
  document.getElementById(containerId).innerHTML = svg;
}

// ---------- Notifications / Reminders ----------
function requestNotifyPermission() {
  if (!("Notification" in window)) {
    alert("Ye browser notifications support nahi karta.");
    return;
  }
  Notification.requestPermission();
}

function checkReminders(storageKey) {
  const list = loadGoalData(storageKey, []);
  const now = new Date();
  const nowStr = now.getHours().toString().padStart(2, "0") + ":" + now.getMinutes().toString().padStart(2, "0");

  list.forEach(r => {
    if (r.time === nowStr && r.lastFired !== now.toDateString()) {
      r.lastFired = now.toDateString();
      if (Notification.permission === "granted") {
        new Notification("Eliya Reminder", { body: r.label });
      }
    }
  });
  saveGoalData(storageKey, list);
}

function startReminderWatcher(storageKey) {
  setInterval(() => checkReminders(storageKey), 30000); // check every 30 sec
}

