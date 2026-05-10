# FinTrack — Personal Finance Dashboard

FinTrack is a full-stack personal finance management web application built using FastAPI, SQLAlchemy, HTML, CSS, and JavaScript.

The application helps users manage their income, expenses, transactions, and category-wise budgets through a clean dashboard interface with JWT-based authentication and REST APIs.

---

# Features

## Authentication & Security
- User Registration & Login
- JWT Token Authentication
- Protected Routes using OAuth2
- Secure Password Hashing

---

## Dashboard
- Financial overview dashboard
- User-specific financial tracking
- Dynamic frontend rendering

---

## Transactions Management
- Add Transactions
- View Transactions
- Update Transactions
- Delete Transactions
- Income & Expense Categorization

---

## Budget Management
- Create Monthly Budgets
- Category-wise Budget Tracking
- Dynamic Budget Rendering
- Budget Progress UI

---

## Categories System
- Custom Categories
- Income & Expense Category Types
- Default Categories Automatically Created

---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- JWT Authentication

## Frontend
- HTML5
- CSS3
- Vanilla JavaScript

## Tools & Technologies
- REST APIs
- Fetch API
- Git & GitHub
- Uvicorn

## Backend
- PostgresSql

---

# Project Structure

FinTrack/
│
├── Backend/
│   ├── routers/
│   │   └── auth.py
│   │
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── oauth2.py
│   ├── database.py
│   ├── hashing.py
│   ├── dependencies.py
│   └── ...
│
├── Frontend/
│   ├── login.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── budget.html
│   │
│   ├── script.js
│   ├── dashboard.js
│   ├── transactions.js
│   ├── budget.js
│   │
│   ├── style.css
│   ├── dashboard-style.css
│   ├── transaction-style.css
│   └── budget-style.css
│
├── requirements.txt
├── README.md
└── .gitignore

---

# REST API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | User Login |

---

## Users

| Method | Endpoint |
|---|---|
| POST | `/users` |
| GET | `/me` |
| DELETE | `/users/{id}` |

---

## Categories

| Method | Endpoint |
|---|---|
| POST | `/categories` |
| GET | `/categories` |
| PUT | `/categories/{id}` |
| DELETE | `/categories/{id}` |

---

## Transactions

| Method | Endpoint |
|---|---|
| POST | `/transactions` |
| GET | `/transactions` |
| PUT | `/transactions/{id}` |
| DELETE | `/transactions/{id}` |

---

## Budgets

| Method | Endpoint |
|---|---|
| POST | `/budgets` |
| GET | `/budgets` |
| PUT | `/budgets/{id}` |
| DELETE | `/budgets/{id}` |

---

# Setup Instructions

## 1. Clone Repository

git clone https://github.com/DevChinmaysamal17/FinTrack---Personal-Finance-Dashboard.git

---

## 2. Navigate Into Project

cd FinTrack

---

## 3. Create Virtual Environment

python -m venv venv

### Activate Virtual Environment

#### Windows

venv\Scripts\activate

#### Mac/Linux

source venv/bin/activate

---

## 4. Install Dependencies

pip install -r requirements.txt

---

## 5. Run FastAPI Server

uvicorn Backend.main:app --reload

---

## 6. Open Application

Visit:

http://127.0.0.1:8000

---

# Key Concepts Used

- REST API Architecture
- JWT Authentication
- CRUD Operations
- ORM Relationships
- Dynamic DOM Rendering
- Frontend & Backend Integration
- Async JavaScript
- Protected Routes
- State Management
- Structured Database

---

# Current Improvements In Progress

- Analytics Dashboard
- Real Budget vs Spending Calculations
- Charts & Visualizations
- Search & Filters
- Mobile Responsiveness
- Deployment

---

# Future Scope

- PostgreSQL Migration
- Docker Support
- Email Verification
- Password Reset
- Export Reports (PDF/Excel)
- AI-powered Expense Insights

---

# Screenshots

- Login Page
screenshots/Login.png

- Dashboard page
screenshots/Dashnoard.png

---

# Learning Outcome

This project helped in understanding:

- Full-stack application architecture
- Backend API development
- Frontend integration
- Authentication systems
- Database relationships
- Dynamic UI rendering
- Real-world CRUD workflows

---

# Author

Chinmay Samal

1st Year Engineering Student | Backend & Full-Stack Development Enthusiast
