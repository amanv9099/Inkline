const API_BASE = 'http://localhost:8000/api';

/* ---------- low-level fetch wrapper ---------- */
async function api(path, { method = 'GET', body, auth = false } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (auth) {
    const token = localStorage.getItem('inkline_token');
    if (token) headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    // token expired/invalid on a protected route -> bounce to login
    if (res.status === 401 && auth) {
      clearSession();
      window.location.href = 'login.html';
    }
    throw new Error(data.error || 'Something went wrong. Please try again.');
  }
  return data;
}

/* ---------- session (token + cached user for instant UI) ---------- */
function saveSession(token, user) {
  localStorage.setItem('inkline_token', token);
  localStorage.setItem('inkline_user', JSON.stringify(user));
}
function clearSession() {
  localStorage.removeItem('inkline_token');
  localStorage.removeItem('inkline_user');
}
function currentUser() {
  const raw = localStorage.getItem('inkline_user');
  return raw ? JSON.parse(raw) : null;
}
function requireAuth() {
  if (!localStorage.getItem('inkline_token')) {
    window.location.href = 'login.html';
  }
}

/* ---------- auth actions ---------- */
async function registerUser(name, email, password) {
  const data = await api('/auth/register/', { method: 'POST', body: { name, email, password } });
  saveSession(data.token, data.user);
}
async function loginUser(email, password) {
  const data = await api('/auth/login/', { method: 'POST', body: { email, password } });
  saveSession(data.token, data.user);
}

/* ---------- blog actions ---------- */
function getPosts(params = {})  {
  const qs = new URLSearchParams(params).toString();
  return api(`/blogs/${qs ? '?' + qs : ''}`);
}
function getPost(id)         { return api(`/blogs/${id}/`); }
function getMyPosts()        { return api('/blogs/mine/', { auth: true }); }
function createPost(post)    { return api('/blogs/', { method: 'POST', body: post, auth: true }); }
function updatePost(id, post){ return api(`/blogs/${id}/`, { method: 'PUT', body: post, auth: true }); }
function deletePost(id)      { return api(`/blogs/${id}/`, { method: 'DELETE', auth: true }); }

/* ---------- profile (Module 5) ---------- */
function getProfile()        { return api('/auth/me/', { auth: true }); }

/* ---------- small helpers (unchanged from Module 1) ---------- */
function timeAgo(ts) {
  const s = Math.floor((Date.now() - ts) / 1000);
  const units = [[31536000, 'y'], [2592000, 'mo'], [86400, 'd'], [3600, 'h'], [60, 'm']];
  for (const [sec, label] of units) {
    const v = Math.floor(s / sec);
    if (v >= 1) return `${v}${label} ago`;
  }
  return 'just now';
}
function excerpt(text, len = 130) {
  const clean = text.replace(/\s+/g, ' ').trim();
  return clean.length > len ? clean.slice(0, len).trim() + '…' : clean;
}
function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}
function toast(msg) {
  let el = document.querySelector('.toast');
  if (!el) {
    el = document.createElement('div');
    el.className = 'toast';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 2200);
}

/* ---------- nav (top-right slot) ---------- */
function renderNavAuth() {
  const slot = document.getElementById('nav-auth-slot');
  if (!slot) return;
  const user = currentUser();
  if (user) {
    slot.innerHTML = `
      <a href="dashboard.html">Dashboard</a>
      <button class="btn ghost" id="logout-btn">Log out</button>
    `;
    document.getElementById('logout-btn').addEventListener('click', () => {
      clearSession();
      window.location.href = 'index.html';
    });
  } else {
    slot.innerHTML = `
      <a href="login.html">Log in</a>
      <a href="register.html" class="btn">Write a post</a>
    `;
  }
}

document.addEventListener('DOMContentLoaded', renderNavAuth);
