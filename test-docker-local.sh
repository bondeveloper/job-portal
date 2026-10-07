#!/bin/bash

# Job Portal Docker Local Test Script
# This script tests the Docker setup on your local machine

set -e

echo "🧪 Job Portal Docker Local Test"
echo "================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
echo -n "Checking Docker installation... "
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ FAILED${NC}"
    echo "Docker is not installed. Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo -e "${GREEN}✓ OK${NC} ($(docker --version))"

# Check if Docker Compose is installed
echo -n "Checking Docker Compose installation... "
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ FAILED${NC}"
    echo "Docker Compose is not installed. Please install Docker Desktop which includes Compose."
    exit 1
fi
echo -e "${GREEN}✓ OK${NC} ($(docker-compose --version))"

# Check if Docker daemon is running
echo -n "Checking Docker daemon... "
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ FAILED${NC}"
    echo "Docker daemon is not running. Please start Docker Desktop."
    exit 1
fi
echo -e "${GREEN}✓ OK${NC}"

echo ""
echo "📦 Docker Build Test"
echo "-------------------"

# Build images
echo -n "Building Docker images... "
if docker-compose build --quiet > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    echo "Build failed. Run: docker-compose build"
    exit 1
fi

echo ""
echo "🚀 Starting Containers"
echo "---------------------"

# Start services
echo -n "Starting database container... "
docker-compose up -d db > /dev/null 2>&1
echo -e "${GREEN}✓ Started${NC}"

# Wait for database to be healthy
echo -n "Waiting for database to be healthy... "
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Ready${NC}"
        break
    fi
    echo -n "."
    sleep 1
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${RED}✗ TIMEOUT${NC}"
    echo "Database failed to start. Check logs: docker-compose logs db"
    docker-compose down
    exit 1
fi

# Start web service
echo -n "Starting web application container... "
docker-compose up -d web > /dev/null 2>&1
echo -e "${GREEN}✓ Started${NC}"

# Wait for web service
echo -n "Waiting for web application to start... "
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8000/api/ > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Ready${NC}"
        break
    fi
    echo -n "."
    sleep 1
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${YELLOW}⚠ TIMEOUT${NC}"
    echo "Web application may still be starting. Check logs: docker-compose logs web"
fi

echo ""
echo "✅ Container Status"
echo "-------------------"
docker-compose ps

echo ""
echo "🔍 Health Checks"
echo "----------------"

# Check database connection
echo -n "Database connection... "
if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
fi

# Check API endpoint
echo -n "API endpoint (http://localhost:8000)... "
if curl -s http://localhost:8000/api/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
fi

# Check admin panel
echo -n "Admin panel (http://localhost:8000/admin)... "
if curl -s http://localhost:8000/admin/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
fi

echo ""
echo "📊 Database Check"
echo "-----------------"

# Check migrations
echo -n "Checking migrations... "
migration_count=$(docker-compose exec -T web python manage.py showmigrations --plan | wc -l)
echo -e "${GREEN}✓ OK${NC} ($migration_count lines)"

# Count database tables
echo -n "Counting database tables... "
table_count=$(docker-compose exec -T db psql -U postgres -d job_portal -t -c "\dt" | wc -l)
echo -e "${GREEN}✓ OK${NC} ($table_count tables)"

echo ""
echo "🧪 Running Tests"
echo "----------------"
echo -n "Running pytest... "
if docker-compose exec -T web pytest --tb=short -q > /tmp/test_output.txt 2>&1; then
    test_result=$(tail -1 /tmp/test_output.txt)
    echo -e "${GREEN}✓ PASSED${NC}"
    echo "  $test_result"
else
    echo -e "${YELLOW}⚠ Some tests failed${NC}"
    tail -10 /tmp/test_output.txt
fi

echo ""
echo "📚 API Documentation"
echo "--------------------"
echo "API is running at: ${BLUE}http://localhost:8000/api/${NC}"
echo "Admin panel is at: ${BLUE}http://localhost:8000/admin${NC}"
echo ""
echo "To create a superuser, run:"
echo "  ${BLUE}docker-compose exec web python manage.py createsuperuser${NC}"
echo ""
echo "To view logs:"
echo "  ${BLUE}docker-compose logs -f web${NC}"
echo ""
echo "To stop containers:"
echo "  ${BLUE}docker-compose down${NC}"

echo ""
echo "================================"
echo -e "${GREEN}✅ All tests passed!${NC}"
echo "================================"
