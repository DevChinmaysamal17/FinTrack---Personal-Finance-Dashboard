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
| Database | PostgreSQL |
| Authentication | JWT, OAuth2, Passlib/Bcrypt |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Deployment | Render |
| Tools | Git, GitHub, REST APIs, Fetch API |

---

# 🏗️ Architecture

```text
Frontend (HTML/CSS/JS)
        ↓
FastAPI Backend
        ↓
PostgreSQL Database
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

## 1. Clone Repository

```bash
git clone https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard.git
cd FinTrack---Personal-Finance-Dashboard
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create `.env` file:

```env
DATABASE_URL=your_postgresql_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 5. Run Application

```bash
uvicorn Backend.main:app --reload
```

---

## 6. Open Application

```text
http://127.0.0.1:8000
```

---

# 🚀 Deployment

The application is deployed on Render using:
- FastAPI backend service
- PostgreSQL cloud database
- Automatic GitHub-based CI/CD deployment

---

# 🗺️ Future Improvements

- [ ] Charts & financial analytics
- [ ] Transaction search & filters
- [ ] Mobile responsiveness
- [ ] Docker containerization
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Export reports as PDF/Excel
- [ ] Recurring transaction support

---

# 👨‍💻 Author

## Chinmay Samal

First-Year Engineering Student focused on Backend & Full-Stack Development.

- GitHub: https://github.com/DevChinmaysamal17
- LinkedIn: Add your LinkedIn profile here

---
