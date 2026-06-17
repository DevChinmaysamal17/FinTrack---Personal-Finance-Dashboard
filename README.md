# FinTrack — Personal Finance Dashboard

A full-stack deployed personal finance management application built with FastAPI and PostgreSQL that helps users track expenses, manage category-wise budgets, and monitor financial activity through a secure dashboard.

---

## 🚀 Live Demo

🌐 Live App: https://fintrack-p2n3.onrender.com
📘 API Docs: https://fintrack-p2n3.onrender.com/docs
📁 GitHub Repository: https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard

---

# ✨ Features

## 🔐 Authentication & Security
- JWT Authentication using OAuth2
- Secure password hashing with Bcrypt
- Protected API routes
- User-specific data isolation

## 📊 Dashboard
- Income vs Expense overview
- Real-time financial summary
- Dynamic frontend rendering using Fetch API

## 💸 Transactions
- Add, update, delete transactions
- Income & expense tracking
- Category-based organization

## 📁 Budget Management
- Monthly category-wise budgets
- Budget vs spending tracking
- Visual budget progress indicators

## 🗂️ Categories
- Create custom categories
- Separate income & expense types
- Auto-generated default categories for new users

---

# 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL (Supabase) |
| Authentication | JWT, OAuth2, Passlib/Bcrypt |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Containerization | Docker, Docker Compose |
| Deployment | Render |
| Tools | Git, GitHub, REST APIs, Fetch API |

---

# 🏗️ Architecture

```text
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend (Render)
        ↓
PostgreSQL Database (Supabase)
```

---

# 📸 Screenshots

## Login Page
![Login](Frontend/screenshots/Login.png)

---

## Dashboard
![Dashboard](Frontend/screenshots/Dashboard.png)

---

## Transactions
![Transactions](Frontend/screenshots/Transaction.png)

---

## Budget Management
![Budget](Frontend/screenshots/Budget.png)

---

# 📁 Project Structure

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
├── Dockerfile
├── docker-compose.yaml
├── .dockerignore
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# 🔌 API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | User login & JWT token generation |

---

## Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Register user |
| GET | `/me` | Current user profile |
| DELETE | `/users/{id}` | Delete account |

---

## Transactions

| Method | Endpoint | Description |
|---|---|---|
| POST | `/transactions` | Create transaction |
| GET | `/transactions` | Get all transactions |
| PUT | `/transactions/{id}` | Update transaction |
| DELETE | `/transactions/{id}` | Delete transaction |

---

## Categories

| Method | Endpoint | Description |
|---|---|---|
| POST | `/categories` | Create category |
| GET | `/categories` | Get categories |
| PUT | `/categories/{id}` | Update category |
| DELETE | `/categories/{id}` | Delete category |

---

## Budgets

| Method | Endpoint | Description |
|---|---|---|
| POST | `/budgets` | Create budget |
| GET | `/budgets` | Get budgets |
| PUT | `/budgets/{id}` | Update budget |
| DELETE | `/budgets/{id}` | Delete budget |

---

# ⚙️ Local Setup

## Option 1 — Run with Docker (Recommended) 🐳

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed

### Steps

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

App will be live at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

To stop:
```bash
docker compose down
```

---

## Option 2 — Run Manually (without Docker)

### 1. Clone Repository

```bash
git clone https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard.git
cd FinTrack---Personal-Finance-Dashboard
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

#### Activate Environment

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=your_supabase_postgresql_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> 💡 Get your `DATABASE_URL` from [Supabase](https://supabase.com) → Project → Connect → Session Pooler → URI

---

### 5. Run Application

```bash
uvicorn Backend.main:app --reload
```

---

### 6. Open Application

```
http://127.0.0.1:8000
```

---

# 🚀 Deployment

The application is deployed on Render using:
- FastAPI backend service on Render (free tier)
- PostgreSQL cloud database on Supabase (free tier, permanent)
- Automatic GitHub-based CI/CD deployment

---

# 🗺️ Future Improvements

- [ ] Charts & financial analytics
- [ ] Transaction search & filters
- [ ] Mobile responsiveness
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Export reports as PDF/Excel
- [ ] Recurring transaction support

---

# 👨‍💻 Author

## Chinmay Samal

First-Year Engineering Student focused on Backend Development, Cloud & DevOps.

- GitHub: https://github.com/DevChinmaysamal17
- LinkedIn: https://www.linkedin.com/in/chinmay-samal-492a72387/

---