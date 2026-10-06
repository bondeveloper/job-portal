# Job Portal Backend

A Django REST API for the Job Portal application.

## Tech Stack

- **Django 4.2** - Web framework
- **Django REST Framework** - API toolkit
- **PostgreSQL** - Database
- **Gunicorn** - Production WSGI server
- **pytest** - Testing

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 13+

### Local Development

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

4. Update `.env` with your PostgreSQL credentials.

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server (http://localhost:8000):
```bash
python manage.py runserver
```

### Docker

Build and run with Docker:
```bash
docker-compose up --build
```

## Project Structure

```
backend/
├── config/              # Django settings and configuration
├── accounts/            # Authentication app
│   ├── models.py        # User models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   └── tests.py         # Tests
├── employers/           # Employer management
├── jobs/                # Job listings
├── profiles/            # Candidate profiles
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## API Endpoints

### Authentication

- **POST** `/api/auth/signup` - Create new user account
- **POST** `/api/auth/login` - Login and get session token
- **POST** `/api/auth/logout` - Logout
- **POST** `/api/auth/verify-email` - Verify email address
- **POST** `/api/auth/forgot-password` - Request password reset
- **POST** `/api/auth/reset-password` - Reset password with token

### Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=accounts --cov-report=html
```

Run specific test file:
```bash
pytest accounts/tests.py
```

## Development

1. Update models in app `models.py`
2. Create serializers in `serializers.py`
3. Implement views in `views.py`
4. Add routes in `urls.py`
5. Write tests in `tests.py`
6. Run tests: `pytest`
7. Commit with descriptive messages

## Email Configuration

For development, emails are printed to console. To use a real email service:

1. Set `EMAIL_BACKEND` in `.env` to `django.core.mail.backends.smtp.EmailBackend`
2. Configure SMTP settings (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
