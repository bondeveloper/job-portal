# Job Portal

A production-ready recruitment platform connecting candidates with employers in the UK market. Commission-based hiring with mutual confirmation workflows.

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Testing**: pytest + pytest-django (backend), Vitest (frontend)

## Project Structure

```
job-portal/
├── backend/                 # Django REST API
│   ├── config/
│   ├── accounts/
│   ├── employers/
│   ├── jobs/
│   ├── profiles/
│   ├── manage.py
│   └── requirements.txt
├── frontend/                # React + TypeScript
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── docs/
│   └── adr/
├── CONTEXT.md              # Domain model glossary
└── docker-compose.yml
```

## Setup

### Option 1: Docker (Recommended)

For a quick setup with Docker:
```bash
docker-compose up --build
```

Backend available at: `http://localhost:8000`
Frontend available at: `http://localhost:3000`

### Option 2: Local Development

#### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 13+

#### Backend Setup

1. Create a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the backend server (runs on http://localhost:8000):
```bash
python manage.py runserver
```

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Run the development server (runs on http://localhost:3000):
```bash
npm run dev
```

The frontend is configured to proxy API requests to the backend at `http://localhost:8000/api`.

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with coverage:
```bash
pytest --cov=accounts --cov-report=html
```

### Run specific test file:
```bash
pytest accounts/tests.py
```

### Run specific test class:
```bash
pytest accounts/tests.py::TestSignup
```

## API Endpoints

### Authentication

- **POST** `/api/auth/signup` - Create new user account
- **POST** `/api/auth/verify-email` - Verify email address
- **POST** `/api/auth/login` - Login and get session token
- **POST** `/api/auth/logout` - Logout and invalidate session
- **POST** `/api/auth/forgot-password` - Request password reset
- **POST** `/api/auth/reset-password` - Reset password with token

### Request/Response Examples

#### Signup
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

#### Verify Email
```bash
curl -X POST http://localhost:8000/api/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"token": "verification-token"}'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@example.com",
    "password": "securepassword123",
    "remember_me": false
  }'
```

#### Logout
```bash
curl -X POST http://localhost:8000/api/auth/logout \
  -H "Authorization: Bearer session-token"
```

#### Forgot Password
```bash
curl -X POST http://localhost:8000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "candidate@example.com"}'
```

#### Reset Password
```bash
curl -X POST http://localhost:8000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "token": "reset-token",
    "password": "newpassword123",
    "password_confirm": "newpassword123"
  }'
```

## Project Structure

```
job-portal/
├── config/              # Django settings and configuration
├── accounts/            # Authentication app
│   ├── models.py        # User, EmailVerificationToken, PasswordResetToken, SessionToken
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   ├── urls.py          # URL routing
│   ├── authentication.py # Custom token authentication
│   └── tests.py         # Integration tests
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── pytest.ini          # pytest configuration
└── README.md           # This file
```

## Development

### Making changes to the API

1. Update the models in `accounts/models.py`
2. Create serializers in `accounts/serializers.py`
3. Implement views in `accounts/views.py`
4. Add routes in `accounts/urls.py`
5. Write tests in `accounts/tests.py`
6. Run tests: `pytest`
7. Commit changes with descriptive messages

### Email Configuration

For development, emails are printed to console. To use a real email service:

1. Set `EMAIL_BACKEND` in `.env` to `django.core.mail.backends.smtp.EmailBackend`
2. Configure SMTP settings (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

## Deployment

See deployment guide in `/docs/deployment.md` (coming soon)
