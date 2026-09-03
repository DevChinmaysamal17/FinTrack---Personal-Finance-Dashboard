# FinTrack — Personal Finance Dashboard

Personal finance dashboard built with FastAPI and PostgreSQL. Track income and expenses, organize them by category, set budgets, and view a running summary — with JWT authentication, Docker, and a GitHub Actions CI/CD pipeline.

---

## Live Demo

🌐 Live App: https://fintrack-p2n3.onrender.com

📘 API Docs: https://fintrack-p2n3.onrender.com/docs

📁 GitHub Repository: https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard

---

## Features

- **Accounts** — Register with name, email, and password. Passwords are hashed with bcrypt before they are stored.
- **JWT login** — OAuth2 password flow issues a Bearer token used on every protected request.
- **Per-user data** — Transactions, categories, and budgets are scoped to the logged-in user.
- **Default categories** — New accounts get a starter set of income and expense categories (Salary, Food, Rent, and so on).
- **Dashboard** — Balance, income, expenses, and savings rate, plus recent transactions. Add a transaction from a modal without leaving the page.
- **Transactions** — Create, list, update, and delete income or expense rows. Filter the table by type in the browser.
- **Budgets** — Set an amount per category and date. The budget page compares that cap to actual expense totals and shows usage.
- **Same-origin UI** — FastAPI serves the HTML/CSS/JS and the JSON API from one process, so the frontend calls relative URLs (`/login`, `/transactions`, …).
- **Containerized run** — Dockerfile plus Docker Compose (API + PostgreSQL).
- **CI/CD** — Push to `main` runs pytest, then builds and publishes a Docker image to GHCR.

---

## Architecture

FinTrack is a single FastAPI application with two jobs: serve the static UI and expose a REST API. Production currently runs the API on Render and PostgreSQL on Supabase. Locally you can point `DATABASE_URL` at Compose Postgres or any other Postgres instance.

```text
Browser (login / dashboard / transactions / budget)
        │  GET /  and  GET /static/*
        │  fetch()  →  /users, /login, /me, /transactions, /categories, /budgets
        ▼
FastAPI  (Backend/main.py on Render or uvicorn)
        │  JWT on protected routes
        │  SQLAlchemy Session
        ▼
PostgreSQL  (Supabase in production, or the Compose db service)
```

### How a request moves through the system

1. **Pages** — `GET /` returns `Frontend/login.html`. After login, the app navigates to `/static/dashboard.html` (and the other HTML pages). CSS, JS, and images are mounted at `/static` from the `Frontend/` folder.
2. **Register** — The login page `POST`s JSON to `/users`. The backend hashes the password, inserts the user, then inserts default categories for that `user_id`.
3. **Login** — The same page `POST`s `application/x-www-form-urlencoded` to `/login` (`username` = email, `password` = password). FastAPI checks the hash, then encodes a JWT (`user_id` + expiry) with `SECRET_KEY` / `ALGORITHM`. The browser stores `access_token` in `localStorage`.
4. **Authenticated pages** — `utils.js` calls `GET /me` with `Authorization: Bearer <token>`. If the token is missing or invalid, the user is sent back to `/`.
5. **Protected money APIs** — Each of `/transactions`, `/categories`, and `/budgets` uses `Depends(get_current_user)`. The JWT is decoded, the user row is loaded, and queries filter on `current_user.id`.
6. **Writes** — Create/update/delete handlers open a SQLAlchemy session (`get_db`), mutate rows, `commit`, and return Pydantic response models (or a small `{message}` dict on delete).
7. **Reads the UI actually uses** — Dashboard and transactions `GET /transactions` (default `limit=100`) and compute totals in JavaScript. The budget page `GET`s `/budgets` and `/transactions`, then matches expenses to `category_id` to fill spent / remaining / progress bars. Category dropdowns come from `GET /categories`.
8. **Logout** — Token is removed from `localStorage`; there is no server-side session to revoke.

### Backend layout (inside FastAPI)

| Piece | Role |
|---|---|
| `Backend/main.py` | App instance, `create_all` tables, CORS, routers, `/me`, `/`, static mount |
| `Backend/routers/` | Route handlers (auth, users, transactions, categories, budgets) |
| `Backend/models.py` | SQLAlchemy tables: `users`, `categories`, `transactions`, `budgets` |
| `Backend/schemas.py` | Pydantic request/response shapes |
| `Backend/database.py` | Engine + `SessionLocal` from `DATABASE_URL` |
| `Backend/dependencies.py` | `get_db` session lifecycle |
| `Backend/oauth2.py` | Bearer extraction + `get_current_user` |
| `Backend/jwt_token.py` | Create / verify JWT |
| `Backend/hashing.py` | bcrypt hash and verify |

### Data model

```text
User
 ├── Category     (income | expense, owned by user)
 ├── Transaction  (amount, type, note, date → category)
 └── Budget       (amount, date → category)

Deleting a user cascades related rows through SQLAlchemy relationships.
```

### Frontend ↔ API (typical session)

```text
POST /users          → create account
POST /login          → access_token
GET  /me             → name + email in the sidebar
GET  /categories     → <select> options
POST /transactions   → add income/expense
GET  /transactions   → tables + dashboard cards
POST /budgets        → set a cap
GET  /budgets        → budget table (spent computed client-side)
DELETE /…/{id}       → remove a row you own
```

Interactive OpenAPI docs: `/docs` on the running server.

---

## API Endpoints

Unauthenticated: `POST /users`, `POST /login`, `GET /`, static files. Everything else below requires `Authorization: Bearer <token>` except where noted.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | Verify email/password (OAuth2 form). Returns `{access_token, token_type}` |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Register. Body: `{name, email, password}`. Returns `{id, name, email}` |
| GET | `/me` | Current user from the JWT |
| DELETE | `/users/{id}` | Delete own account (`403` if `id` is not the caller) |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| POST | `/transactions` | Create. Body: `{amount, type, note?, date, category_id}` |
| GET | `/transactions` | List for the current user (`skip`, `limit`; default limit 100) |
| PUT | `/transactions/{id}` | Update own transaction |
| DELETE | `/transactions/{id}` | Delete own transaction |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| POST | `/categories` | Create. Body: `{name, category_type}` |
| GET | `/categories` | List own categories |
| PUT | `/categories/{id}` | Update own category |
| DELETE | `/categories/{id}` | Delete own category |

### Budgets

| Method | Endpoint | Description |
|---|---|---|
| POST | `/budgets` | Create. Body: `{amount, date, category_id}` |
| GET | `/budgets` | List own budgets (includes nested category) |
| PUT | `/budgets/{id}` | Update own budget |
| DELETE | `/budgets/{id}` | Delete own budget |

---

## Project Structure

```text
FinTrack/
├── Backend/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── transactions.py
│   │   ├── categories.py
│   │   └── budgets.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── oauth2.py
│   ├── jwt_token.py
│   ├── hashing.py
│   └── dependencies.py
│
├── Frontend/
│   ├── screenshots/
│   ├── login.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── budget.html
│   ├── *.js
│   └── *.css
│
├── tests/                          # pytest (route coverage)
├── .github/workflows/
│   └── ci-cd-pipeline.yaml
├── Dockerfile
├── docker-compose.yaml
├── .dockerignore
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Database | PostgreSQL (Supabase in production) |
| Authentication | JWT (python-jose), OAuth2 password bearer, Passlib / Bcrypt |
| Frontend | HTML5, CSS3, vanilla JavaScript, Fetch API |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Container registry | GitHub Container Registry (GHCR) |
| Deployment | Render (API + UI), Supabase (Postgres) |
| Tests | pytest |

---

## CI/CD Pipeline

GitHub Actions workflow: `.github/workflows/ci-cd-pipeline.yaml`.

```text
Push to main → pytest (tests/) → build Docker image → push to GHCR
```

| Job | What it does |
|---|---|
| **test** | Ubuntu + Python 3.12, `pip install -r requirements.txt`, `pytest tests/` (needs `DATABASE_URL` and `SECRET_KEY` repo secrets) |
| **docker** | Runs only after tests pass on `main`. Logs into GHCR and pushes `ghcr.io/DevChinmaysamal17/fintrack:latest` |

Pull the latest image:

```bash
docker pull ghcr.io/devchinmaysamal17/fintrack:latest
```

---

## Screenshots

### Login Page
![Login](Frontend/screenshots/Login.png)

### Dashboard
![Dashboard](Frontend/screenshots/Dashboard.png)

### Transactions
![Transactions](Frontend/screenshots/Transaction.png)

### Budget Management
![Budget](Frontend/screenshots/Budget.png)

---

## Local Setup

Copy `.env.example` to `.env` and set at least:

```env
DATABASE_URL=postgresql://user:password@host:5432/finance_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Option 1 — Uvicorn

```bash
git clone https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard.git
cd FinTrack---Personal-Finance-Dashboard

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env              # then edit DATABASE_URL and SECRET_KEY

uvicorn Backend.main:app --reload
```

App: `http://127.0.0.1:8000`  
API docs: `http://127.0.0.1:8000/docs`

Point `DATABASE_URL` at a running Postgres (local, Docker-only database, or Supabase).

### Option 2 — Docker Compose

```bash
git clone https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard.git
cd FinTrack---Personal-Finance-Dashboard

cp .env.example .env

docker compose up
```

App: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

```bash
docker compose down               # keeps the postgres_data volume
```

---

## Future Improvements

- [ ] Charts and financial analytics
- [ ] Transaction search and richer filters
- [ ] Mobile-responsive layout
- [ ] Email verification
- [ ] Password reset
- [ ] Export reports as PDF / Excel
- [ ] Recurring transactions
- [ ] Database migrations (Alembic) instead of `create_all` only

---

## Author

**Chinmay Samal** — First-Year Engineering Student focused on Backend Development, Cloud & DevOps.

- GitHub: https://github.com/DevChinmaysamal17
- LinkedIn: https://www.linkedin.com/in/chinmaysamal
