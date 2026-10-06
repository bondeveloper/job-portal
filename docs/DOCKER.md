# Docker Setup Guide

This guide explains how to set up and run the Job Portal using Docker.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 1.29+)

## Quick Start

### 1. Clone the repository and navigate to the project directory

```bash
cd job-portal
```

### 2. Create a `.env` file (optional, for custom configuration)

```bash
cp .env.example .env
```

If you don't create a `.env` file, Docker will use default values:
- Database: `job_portal`
- Database User: `postgres`
- Database Password: `postgres`
- Django Secret Key: `your-secret-key-here` (change this in production!)

### 3. Build and start the containers

```bash
docker-compose up --build
```

This command will:
- Build the Django application image
- Start a PostgreSQL database container
- Run migrations automatically
- Start the Django development server on port 8000

The first build may take a few minutes. Subsequent starts will be faster.

### 4. Create a superuser account

In a new terminal window, run:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 5. Access the application

- **Django API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Common Commands

### Start the containers in the background

```bash
docker-compose up -d
```

### Stop the containers

```bash
docker-compose down
```

### Stop containers and remove volumes (reset database)

```bash
docker-compose down -v
```

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web    # Django app
docker-compose logs -f db     # PostgreSQL
```

### Run Django management commands

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell
```

### Run tests

```bash
docker-compose exec web pytest
```

### Run tests with coverage

```bash
docker-compose exec web pytest --cov=accounts --cov-report=html
```

### Create a new superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Reset the database

```bash
docker-compose down -v
docker-compose up
```

## Environment Variables

You can customize the Docker setup by creating a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-very-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,web
DB_NAME=job_portal
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
FRONTEND_URL=http://localhost:3000
```

## Troubleshooting

### Port already in use

If port 8000 or 5432 are already in use, modify the ports in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Use port 8001 instead of 8000
```

### Database connection errors

1. Check if the database container is running:
   ```bash
   docker-compose ps
   ```

2. View database logs:
   ```bash
   docker-compose logs db
   ```

3. Restart the containers:
   ```bash
   docker-compose restart
   ```

### Permission denied errors

If you see permission errors, make sure the current user can access Docker:

```bash
# Linux only
sudo usermod -aG docker $USER
newgrp docker
```

### Rebuild after code changes

If you've modified dependencies, rebuild the image:

```bash
docker-compose build --no-cache
docker-compose up
```

## Production Deployment

For production deployment:

1. Update `DEBUG=False` in `.env`
2. Set a strong `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Use a production database (not the included PostgreSQL container)
5. Configure proper email backend
6. Use a reverse proxy (nginx) in front of Django
7. Enable HTTPS/SSL
8. Set appropriate resource limits in `docker-compose.yml`

See the Django documentation for more details on production deployment.

## Development Tips

### Hot reload during development

The current setup mounts your code volume, so changes are reflected immediately. However, you may need to restart the container if dependencies change:

```bash
docker-compose restart web
```

### Interactive Python shell

```bash
docker-compose exec web python manage.py shell
```

### Database access

Connect directly to PostgreSQL:

```bash
docker-compose exec db psql -U postgres -d job_portal
```

### View all database tables

```bash
docker-compose exec db psql -U postgres -d job_portal -c "\dt"
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Guide](https://docs.djangoproject.com/en/4.2/howto/deployment/)
