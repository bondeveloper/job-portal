# Job Portal

A recruitment platform connecting candidates with employers in the South African market.

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Vue.js or React (coming soon)
- **Testing**: pytest + pytest-django

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- pip/venv

### Installation

1. Clone the repository and navigate to the project directory:
```bash
cd job-portal
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Update `.env` with your PostgreSQL credentials and other settings.

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

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
