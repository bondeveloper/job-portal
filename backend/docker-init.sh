#!/bin/bash

# Job Portal Docker Initialization Script
# This script helps set up and run the Job Portal using Docker

set -e

echo "🚀 Job Portal Docker Setup"
echo "=========================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created. Please review and update if needed."
    else
        echo "⚠️  .env.example not found"
    fi
    echo ""
fi

# Build and start containers
echo "🔨 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for database to be ready..."
sleep 5

echo ""
echo "✅ Containers are running!"
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🔐 Setting up superuser account..."
echo "   Run the following command in a new terminal to create an admin account:"
echo ""
echo "   docker-compose exec web python manage.py createsuperuser"
echo ""
echo "🌐 Access the application at:"
echo "   - Django API: http://localhost:8000"
echo "   - Admin Panel: http://localhost:8000/admin"
echo ""
echo "📚 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop the containers:"
echo "   docker-compose down"
echo ""
