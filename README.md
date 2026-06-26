# FinTrack — Personal Finance Dashboard

Production-ready personal finance dashboard built with FastAPI and PostgreSQL, featuring JWT authentication, Docker containerization, and an automated CI/CD pipeline via GitHub Actions.

---

## 🚀 Live Demo

🌐 Live App: https://fintrack-p2n3.onrender.com

📘 API Docs: https://fintrack-p2n3.onrender.com/docs

📁 GitHub Repository: https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard

---

## ✨ Features

### 🔐 Authentication & Security
- JWT Authentication using OAuth2
- Secure password hashing with Bcrypt
- Protected API routes
- User-specific data isolation

### 📊 Dashboard
- Income vs Expense overview
- Real-time financial summary
- Dynamic frontend rendering using Fetch API

### 💸 Transactions
- Add, update, delete transactions
- Income & expense tracking
- Category-based organization

### 📁 Budget Management
- Monthly category-wise budgets
- Budget vs spending tracking
- Visual budget progress indicators

### 🗂️ Categories
- Create custom categories
- Separate income & expense types
- Auto-generated default categories for new users

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL (Supabase) |
| Authentication | JWT, OAuth2, Passlib/Bcrypt |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Container Registry | GitHub Container Registry (GHCR) |
| Deployment | Render |
| Tools | Git, GitHub, REST APIs, Fetch API |

---

## ⚙️ CI/CD Pipeline

This project uses **GitHub Actions** for automated testing and Docker image publishing.

### Pipeline flow:
```
Push to main → Run pytest → Build Docker image → Push to GHCR
```

### Jobs:
- **test** — Sets up Python 3.12, installs dependencies, runs pytest
- **docker** — Builds Docker image and pushes to `ghcr.io/devchinmaysamal17/fintrack:latest` (only on `main` after tests pass)

### Pull the latest image:
```bash
docker pull ghcr.io/devchinmaysamal17/fintrack:latest
```

---

## 🏗️ Architecture

```text
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend (Render)
        ↓
PostgreSQL Database (Supabase)
```

---

## 📸 Screenshots

### Login Page
![Login](Frontend/screenshots/Login.png)

### Dashboard
![Dashboard](Frontend/screenshots/Dashboard.png)

### Transactions
![Transactions](Frontend/screenshots/Transaction.png)

### Budget Management
![Budget](Frontend/screenshots/Budget.png)

---

## 📁 Project Structure

```text
FinTrack/
│
├── Backend/
│   ├── routers/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── oauth2.py
│   └── dependencies.py
│
├── Frontend/
│   ├── screenshots/
│   ├── dashboard.html
│   ├── transactions.html
│   ├── budget.html
│   ├── *.js
│   └── *.css
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── tests/
│   └── test_basic.py
│
├── Dockerfile
├── docker-compose.yaml
├── .dockerignore
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | User login & JWT token generation |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Register user |
| GET | `/me` | Current user profile |
| DELETE | `/users/{id}` | Delete account |

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| POST | `/transactions` | Create transaction |
| GET | `/transactions` | Get all transactions |
| PUT | `/transactions/{id}` | Update transaction |
| DELETE | `/transactions/{id}` | Delete transaction |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| POST | `/categories` | Create category |
| GET | `/categories` | Get categories |
| PUT | `/categories/{id}` | Update category |
| DELETE | `/categories/{id}` | Delete category |

### Budgets

| Method | Endpoint | Description |
|---|---|---|
| POST | `/budgets` | Create budget |
| GET | `/budgets` | Get budgets |
| PUT | `/budgets/{id}` | Update budget |
| DELETE | `/budgets/{id}` | Delete budget |

---

## ⚙️ Local Setup

### Option 1 — Run with Docker (Recommended) 🐳

```bash
# 1. Clone the repository
git clone https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard.git
cd FinTrack---Personal-Finance-Dashboard

# 2. Create your .env file
cp .env.example .env
# Edit .env with your values

# 3. Start the app
docker compose up
```

App: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

```bash
# Stop without losing data
docker compose down
```

---

### Option 2 — Run Manually

```bash
git clone https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard.git
cd FinTrack---Personal-Finance-Dashboard

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`:
```env
DATABASE_URL=your_supabase_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```bash
uvicorn Backend.main:app --reload
```

Open: `http://127.0.0.1:8000`

---

## 🚀 Deployment

- FastAPI backend on Render (free tier)
- PostgreSQL on Supabase (free tier, permanent)
- Docker image on GHCR (`ghcr.io/devchinmaysamal17/fintrack:latest`)
- GitHub Actions CI/CD on every push to `main`

---

## 🗺️ Future Improvements

- [ ] Charts & financial analytics
- [ ] Transaction search & filters
- [ ] Mobile responsiveness
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Export reports as PDF/Excel
- [ ] Recurring transaction support

---

## 👨‍💻 Author

**Chinmay Samal** — First-Year Engineering Student focused on Backend Development, Cloud & DevOps.

- GitHub: https://github.com/DevChinmaysamal17
- LinkedIn: https://www.linkedin.com/in/chinmay-samal-492a72387/
