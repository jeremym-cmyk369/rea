'use strict';

const samples = [
  { id: 'E-1048', label: 'Brake service estimate', detail: 'Last contact: 4 days ago', action: 'Prepare check-in', state: 'pending' },
  { id: 'E-1053', label: 'Fleet service inquiry', detail: 'Last contact: 3 days ago', action: 'Review priority', state: 'pending' },
  { id: 'E-1061', label: 'Maintenance quote', detail: 'Last contact: 5 days ago', action: 'Prepare follow-up', state: 'pending' }
];
let records = samples.map((item) => ({ ...item }));
const rows = document.querySelector('#estimate-rows');
const counts = { total: document.querySelector('#stat-total'), pending: document.querySelector('#stat-pending'), reviewed: document.querySelector('#stat-reviewed') };
const two = (num) => String(num).padStart(2, '0');
function renderQueue() {
  if (!rows) return;
  rows.innerHTML = '';
  for (const record of records) {
    const row = document.createElement('div');
    row.className = `estimate-row${record.state !== 'pending' ? ' is-reviewed' : ''}`;
    const info = document.createElement('div'); info.className = 'estimate-info';
    const name = document.createElement('strong'); name.textContent = record.label;
    const sub = document.createElement('small'); sub.textContent = `${record.id} · ${record.detail}`;
    info.append(name, sub);
    const next = document.createElement('div'); next.className = 'estimate-next'; next.textContent = record.action;
    const status = document.createElement('div'); status.className = 'estimate-status'; status.textContent = record.state === 'pending' ? 'Pending review' : record.state === 'approved' ? 'Approved in demo' : 'Needs manual review';
    const action = document.createElement('div'); action.className = 'estimate-buttons';
    if (record.state === 'pending') {
      for (const [label, newState, cls] of [['Approve', 'approved', 'approve-btn'], ['Flag', 'flagged', 'flag-btn']]) {
        const btn = document.createElement('button'); btn.type = 'button'; btn.className = cls; btn.textContent = label;
        btn.setAttribute('aria-label', `${label} fictional estimate ${record.id}`);
        btn.addEventListener('click', () => { record.state = newState; renderQueue(); });
        action.append(btn);
      }
    } else { const check = document.createElement('span'); check.className='action-complete'; check.textContent = '✓ Reviewed'; action.append(check); }
    row.append(info, next, status, action);
    rows.append(row);
  }
  counts.total.textContent = two(records.length);
  counts.pending.textContent = two(records.filter((r) => r.state === 'pending').length);
  counts.reviewed.textContent = two(records.filter((r) => r.state !== 'pending').length);
}
renderQueue();
document.querySelector('#reset-demo')?.addEventListener('click', () => { records = samples.map((item) => ({ ...item })); renderQueue(); });
document.querySelector('#year').textContent = String(new Date().getFullYear());

const menu = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() { if (!menu || !mobileNav) return; menu.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-label', 'Open navigation menu'); mobileNav.hidden = true; }
menu?.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') === 'true'; menu.setAttribute('aria-expanded', String(!open)); menu.setAttribute('aria-label', open ? 'Open navigation menu' : 'Close navigation menu'); mobileNav.hidden = open; });
mobileNav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
window.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });
window.addEventListener('resize', () => { if (window.innerWidth > 860) closeMenu(); });

const form = document.querySelector('#contact-form');
const formStatus = document.querySelector('#form-status');
const started = document.querySelector('#contact-started');
if (started) started.value = String(Date.now());
form?.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const button = form.querySelector('button[type="submit"]');
  const data = new FormData(form);
  const get = (name) => String(data.get(name) || '').trim();
  button.disabled = true;
  formStatus.textContent = 'Sending your inquiry…';
  try {
    const res = await fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
    const out = await res.json().catch(() => ({}));
    if (!res.ok || !out.ok) throw new Error(out.message || 'Send failed');
    form.reset();
    if (started) started.value = String(Date.now());
    formStatus.textContent = out.message;
  } catch (err) {
    const subject = `AI Business Harness inquiry — ${get('company') || get('name')}`;
    const body = [`Name: ${get('name')}`, `Work email: ${get('email')}`, `Company: ${get('company') || 'Not provided'}`, '', 'Repetitive task or workflow:', get('task')].join('\n');
    formStatus.innerHTML = '';
    formStatus.append(`${err.message && err.message !== 'Send failed' ? err.message + ' ' : 'We couldn’t send that right now. '}`);
    const link = document.createElement('a');
    link.href = `mailto:jeremy@aibusinessharness.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    link.textContent = 'Email it to us instead';
    formStatus.append(link, '.');
  } finally {
    button.disabled = false;
  }
});
