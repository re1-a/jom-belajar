// Configuration for file paths via Vite's /@fs/ or direct relative paths
// Vite handles /@fs/ for absolute paths outside root.
const PATHS = {
  tracker: '/@fs/Users/re1/Documents/antigravity/Pembantu_AI/tracker_ai.md',
  audit: '/@fs/Users/re1/Documents/antigravity/Pembantu_AI/audit_log.md',
  inbox: '/@fs/Users/re1/Documents/antigravity/Pembantu_AI/inbox.md',
  plan: '/@fs/Users/re1/.gemini/antigravity/brain/c0e5d5d4-f531-48fe-8750-6c9bcc5de92a/implementation_plan.md'
};

async function fetchFile(path) {
  try {
    const response = await fetch(`${path}?t=${Date.now()}`);
    if (!response.ok) return null;
    return await response.text();
  } catch (e) {
    console.error(`Fetch gagal untuk ${path}:`, e);
    return null;
  }
}

function parseTracker(text) {
  if (!text) return '<div class="loading">No tracker data found.</div>';
  
  const lines = text.split('\n');
  let html = '';
  
  for (const line of lines) {
    if (line.trim() === '') continue;
    
    // Check for task completion
    let className = 'task-item';
    let content = line;
    
    if (line.includes('[x]') || line.includes('[X]')) {
      className += ' completed';
    } else if (line.includes('[/]')) {
      className += ' active';
    }
    
    // Bold highlight for some parts (simple markdown bold)
    content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    if (line.startsWith('- ') || line.startsWith('* ')) {
      html += `<div class="${className}">${content}</div>`;
    } else if (line.startsWith('#')) {
      const level = Math.min((line.match(/^#+/) || [''])[0].length, 6);
      html += `<h${level} style="color: var(--accent-cyan); margin: 10px 0;">${line.replace(/^#+\s/, '')}</h${level}>`;
    } else {
      html += `<div class="${className}">${content}</div>`;
    }
  }
  
  return html;
}

function parseAudit(text) {
  if (!text) return '<div class="loading">No audit log data found.</div>';
  
  const lines = text.split('\n');
  let html = '';
  
  for (const line of lines) {
    if (line.trim() === '') continue;
    
    // Highlight timestamps or status tags
    let formatted = line
      .replace(/\[(\d{4}-\d{2}-\d{2}.*?)\]/g, '<span style="color: var(--text-dim)">[$1]</span>')
      .replace(/\[LEMAH\]/g, '<span style="color: #ff4757">[LEMAH]</span>')
      .replace(/\[IMPROVING\]/g, '<span style="color: #ffa502">[IMPROVING]</span>')
      .replace(/\[DAH FAHAM\]/g, '<span style="color: #2ed573">[DAH FAHAM]</span>');
      
    html += `<div class="log-line">${formatted}</div>`;
  }
  
  return html;
}

function parseMarkdown(text) {
  if (!text) return '<div class="loading">No content found.</div>';
  if (window.marked) {
    return window.marked.parse(text);
  }
  return `<pre>${text}</pre>`;
}

const lastContent = {};

function renderIfChanged(key, raw, parser) {
  if (lastContent[key] === raw) return;   // takde perubahan → kekalkan scroll
  lastContent[key] = raw;
  const el = document.getElementById(`${key}-content`);
  if (el) el.innerHTML = parser(raw);
}

let busy = false;
async function updateDashboard() {
  if (busy) return;
  busy = true;
  try {
    const [trackerRaw, auditRaw, inboxRaw, planRaw] = await Promise.all([
      fetchFile(PATHS.tracker),
      fetchFile(PATHS.audit),
      fetchFile(PATHS.inbox),
      fetchFile(PATHS.plan)
    ]);
    
    renderIfChanged('tracker', trackerRaw, parseTracker);
    renderIfChanged('audit', auditRaw, parseAudit);
    renderIfChanged('inbox', inboxRaw || '*Inbox is empty.*', parseMarkdown);
    renderIfChanged('plan', planRaw, parseMarkdown);
  } finally {
    busy = false;
  }
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
  updateDashboard();
  
  // Set up refresh buttons
  document.getElementById('refresh-tracker')?.addEventListener('click', updateDashboard);
  document.getElementById('refresh-audit')?.addEventListener('click', updateDashboard);
  document.getElementById('refresh-plan')?.addEventListener('click', updateDashboard);
  
  // Auto-refresh every 5 seconds for a true "mission control" feel
  setInterval(updateDashboard, 5000);

  // Setup Inbox Input
  const submitBtn = document.getElementById('inbox-submit');
  const textArea = document.getElementById('inbox-textarea');
  if (submitBtn && textArea) {
    submitBtn.addEventListener('click', async () => {
      const text = textArea.value;
      if (!text.trim()) return;
      
      submitBtn.innerText = '[...]';
      try {
        const res = await fetch('/api/inbox', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        if (res.ok) {
          textArea.value = '';
          updateDashboard(); // fetch fresh data
        }
      } catch(e) {
        console.error('Failed to save to inbox', e);
      } finally {
        submitBtn.innerText = '[+] APPEND';
      }
    });
  }
});
