# 📝 Inkline — Full Stack Blog Application

A minimal, editorial-style blog platform built module by module as part of a
web development internship — from a static frontend to a fully working
full-stack app with authentication, a real database, and CRUD.

**Frontend:** HTML5, CSS3, Vanilla JavaScript
**Backend:** Django · Django REST Framework
**Database:** SQLite
**Auth:** JWT (djangorestframework-simplejwt)

---

## ✨ Features

- 🔐 User registration & login with JWT authentication
- 📊 Personal dashboard — see only your own posts, word count, and stats
- ✍️ Full CRUD — create, read, **edit**, and delete blog posts
- 🔍 Live search and category/tag filtering on the home feed
- 👤 User profile endpoint
- 📱 Responsive, editorial-style UI (no framework — hand-built CSS)
- 🚀 Deploy-ready for Render (backend) + Vercel (frontend)

---

## 📁 Project Structure

```
blogapp/
├── index.html            Home — public blog feed
├── login.html            Log in
├── register.html         Create an account
├── dashboard.html        Logged-in user's posts + stats
├── create-blog.html      Write a new post
├── edit-blog.html        Edit an existing post
├── post.html             Read a single post
├── css/style.css         All styling
├── js/app.js             Talks to the Django REST API
└── backend/              Django project
    ├── manage.py
    ├── requirements.txt
    ├── inkline_backend/   settings, URL routing, WSGI
    ├── accounts/          custom User model, register/login/me
    └── blog/              Blog model, CRUD API, search & tag filter
```

---

## 🚀 Getting Started

### 1. Backend (Django)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then set SECRET_KEY to any random string

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # optional — for /admin/
python manage.py runserver
```
Backend runs at `http://localhost:8000`.

### 2. Frontend

Just open `index.html` in your browser, or serve the folder:

```bash
npx serve .
```

`js/app.js` is already pointed at `http://localhost:8000/api` — update the
`API_BASE` constant there if your backend runs somewhere else.

---

## 🔌 API Reference

| Method | Endpoint               | Auth required | Description                              |
|--------|------------------------|:--------------:|-------------------------------------------|
| POST   | `/api/auth/register/`  | ❌             | Create an account → returns JWT            |
| POST   | `/api/auth/login/`     | ❌             | Log in → returns JWT                       |
| GET    | `/api/auth/me/`        | ✅             | Current user's profile                     |
| GET    | `/api/blogs/`          | ❌             | List posts (`?search=`, `?tag=` supported) |
| GET    | `/api/blogs/mine/`     | ✅             | Logged-in user's own posts                 |
| GET    | `/api/blogs/:id/`      | ❌             | Get a single post                          |
| POST   | `/api/blogs/`          | ✅             | Create a post                              |
| PUT    | `/api/blogs/:id/`      | ✅             | Edit your own post                         |
| DELETE | `/api/blogs/:id/`      | ✅             | Delete your own post                       |

Protected routes require an `Authorization: Bearer <token>` header.

---

## ☁️ Deployment

### Backend → Render
1. Push this repo to GitHub.
2. On [render.com](https://render.com) → **New +** → **Web Service** → connect the repo.
3. **Root Directory:** `backend`
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `python manage.py migrate --noinput && gunicorn inkline_backend.wsgi`
6. Add environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=<your-app>.onrender.com`
7. Deploy — copy the live URL (e.g. `https://inkline-api.onrender.com`).

> ⚠️ Render's free tier has an ephemeral filesystem — the SQLite file resets on
> redeploy or when the instance sleeps from inactivity. Fine for a demo;
> swap to Render's free PostgreSQL add-on if persistence matters later.

### Frontend → Vercel
1. In `js/app.js`, set `API_BASE` to your Render URL + `/api`.
2. Push the change to GitHub.
3. On [vercel.com](https://vercel.com) → **New Project** → import the repo → framework preset **Other**.
4. Deploy — copy the live URL (e.g. `https://inkline.vercel.app`).
5. Back on Render, add `CORS_ALLOWED_ORIGINS=<your-vercel-url>` and redeploy the backend.

---

## 🛠️ Tech Stack

| Layer     | Tech                                             |
|-----------|---------------------------------------------------|
| Frontend  | HTML5, CSS3, Vanilla JavaScript (Fetch API)        |
| Backend   | Django 5, Django REST Framework                    |
| Auth      | JWT via djangorestframework-simplejwt              |
| Database  | SQLite (dev) — swappable to PostgreSQL             |
| Hosting   | Render (backend) · Vercel (frontend)               |

---

## 📌 Roadmap

- [x] Frontend pages (Home, Login, Register, Dashboard, Create Blog)
- [x] Django REST API with JWT auth
- [x] SQLite database integration
- [x] Full CRUD + search/filter
- [x] Deployment-ready config
- [ ] Live deployment (add your links here once deployed)

---

*Built as part of a web development internship — Modules 1 through 6.*
