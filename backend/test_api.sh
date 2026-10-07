#!/bin/bash

# API Testing Script for Job Portal Backend
# Usage: ./test_api.sh

API="http://localhost:8000/api"
CANDIDATE_EMAIL="test.candidate@example.com"
EMPLOYER_EMAIL="test.employer@example.com"
PASSWORD="testpass123"

echo "🧪 Job Portal Backend API Tests"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper function to test endpoint
test_endpoint() {
  local method=$1
  local endpoint=$2
  local data=$3
  local expected_code=$4

  echo -n "Testing $method $endpoint ... "

  if [ -z "$CANDIDATE_TOKEN" ]; then
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X $method "$API$endpoint" -H "Content-Type: application/json" -d "$data")
  else
    status_code=$(curl -s -o /dev/null -w "%{http_code}" -X $method "$API$endpoint" -H "Authorization: Bearer $CANDIDATE_TOKEN" -H "Content-Type: application/json" -d "$data")
  fi

  if [ "$status_code" -eq "$expected_code" ]; then
    echo -e "${GREEN}✓ $status_code${NC}"
  else
    echo -e "${RED}✗ Expected $expected_code, got $status_code${NC}"
  fi
}

# Test 1: Candidate Signup
echo "1️⃣  Authentication"
echo "------------------"
response=$(curl -s -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$CANDIDATE_EMAIL\",
    \"password\": \"$PASSWORD\",
    \"password_confirm\": \"$PASSWORD\",
    \"user_type\": \"candidate\"
  }")

if echo "$response" | grep -q "user_id"; then
  echo -e "${GREEN}✓ Candidate signup${NC}"
else
  echo -e "${RED}✗ Candidate signup failed${NC}"
  echo "Response: $response"
fi

# Test 2: Candidate Login
response=$(curl -s -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$CANDIDATE_EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

CANDIDATE_TOKEN=$(echo "$response" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$CANDIDATE_TOKEN" ]; then
  echo -e "${GREEN}✓ Candidate login (token: ${CANDIDATE_TOKEN:0:10}...)${NC}"
else
  echo -e "${RED}✗ Candidate login failed${NC}"
  echo "Response: $response"
  exit 1
fi

# Test 3: Get Profile
echo ""
echo "2️⃣  Candidate Profile"
echo "---------------------"
test_endpoint "GET" "/profiles/" "" 200

# Test 4: Update Profile
test_endpoint "PATCH" "/profiles/" "{
  \"first_name\": \"Test\",
  \"last_name\": \"Candidate\",
  \"phone\": \"07123456789\",
  \"location\": \"London, UK\",
  \"salary_expectations\": 60000
}" 200

# Test 5: Add Education
echo ""
echo "3️⃣  Education"
echo "---------------"
test_endpoint "POST" "/profiles/1/education/" "{
  \"institution\": \"Test University\",
  \"degree\": \"Bachelor of Science\",
  \"field\": \"Computer Science\",
  \"graduation_date\": \"2020-06-15\"
}" 201

# Test 6: Add Certification
echo ""
echo "4️⃣  Certifications"
echo "-------------------"
test_endpoint "POST" "/profiles/1/certifications/" "{
  \"name\": \"AWS Certified\",
  \"issuer\": \"Amazon\",
  \"issue_date\": \"2024-03-10\",
  \"expiry_date\": \"2026-03-10\"
}" 201

# Test 7: Employer Signup
echo ""
echo "5️⃣  Employer Account"
echo "---------------------"
response=$(curl -s -X POST "$API/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMPLOYER_EMAIL\",
    \"password\": \"$PASSWORD\",
    \"password_confirm\": \"$PASSWORD\",
    \"user_type\": \"employer\"
  }")

if echo "$response" | grep -q "user_id"; then
  echo -e "${GREEN}✓ Employer signup${NC}"
else
  echo -e "${RED}✗ Employer signup failed${NC}"
fi

# Test 8: Employer Login
response=$(curl -s -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMPLOYER_EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

EMPLOYER_TOKEN=$(echo "$response" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$EMPLOYER_TOKEN" ]; then
  echo -e "${GREEN}✓ Employer login (token: ${EMPLOYER_TOKEN:0:10}...)${NC}"
else
  echo -e "${RED}✗ Employer login failed${NC}"
fi

# Test 9: Create Job
echo ""
echo "6️⃣  Job Management"
echo "-------------------"
response=$(curl -s -X POST "$API/jobs/" \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Senior Python Developer\",
    \"description\": \"We are looking for a Python developer\",
    \"location\": \"London, UK\",
    \"salary_min\": 70000,
    \"salary_max\": 90000,
    \"experience_level\": \"senior\"
  }")

if echo "$response" | grep -q "id"; then
  echo -e "${GREEN}✓ Job created${NC}"
  JOB_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
else
  echo -e "${RED}✗ Job creation failed${NC}"
  echo "Response: $response"
fi

# Test 10: Apply to Job
echo ""
echo "7️⃣  Job Applications"
echo "---------------------"
response=$(curl -s -X POST "$API/jobs/$JOB_ID/applications/" \
  -H "Authorization: Bearer $CANDIDATE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"cover_letter\": \"I am very interested in this position\"
  }")

if echo "$response" | grep -q "status"; then
  echo -e "${GREEN}✓ Application submitted${NC}"
  APP_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
else
  echo -e "${RED}✗ Application failed${NC}"
  echo "Response: $response"
fi

# Test 11: Shortlist Application
response=$(curl -s -X PATCH "$API/jobs/$JOB_ID/applications/$APP_ID/" \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"status\": \"shortlisted\"
  }")

if echo "$response" | grep -q "shortlisted"; then
  echo -e "${GREEN}✓ Application shortlisted${NC}"
else
  echo -e "${RED}✗ Shortlist failed${NC}"
fi

# Test 12: Check Hire Status
echo ""
echo "8️⃣  Hire Confirmation"
echo "---------------------"
response=$(curl -s -X GET "$API/jobs/$JOB_ID/applications/$APP_ID/hire-status/" \
  -H "Authorization: Bearer $CANDIDATE_TOKEN")

if echo "$response" | grep -q "status"; then
  echo -e "${GREEN}✓ Hire status retrieved${NC}"
else
  echo -e "${RED}✗ Hire status failed${NC}"
fi

# Test 13: Accept Hire
response=$(curl -s -X POST "$API/jobs/$JOB_ID/applications/$APP_ID/accept-hire/" \
  -H "Authorization: Bearer $CANDIDATE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{}")

if echo "$response" | grep -q "confirmed"; then
  echo -e "${GREEN}✓ Hire confirmed${NC}"
else
  echo -e "${RED}✗ Hire confirmation failed${NC}"
fi

# Test 14: View Commissions
echo ""
echo "9️⃣  Commissions"
echo "----------------"
response=$(curl -s -X GET "$API/employer/commissions/" \
  -H "Authorization: Bearer $EMPLOYER_TOKEN")

if echo "$response" | grep -q "id"; then
  echo -e "${GREEN}✓ Commissions retrieved${NC}"
else
  echo -e "${RED}✗ Commission retrieval failed${NC}"
fi

echo ""
echo "================================"
echo -e "${GREEN}✅ Test suite complete!${NC}"
echo ""
echo "To test with your own data:"
echo "1. Start the backend: python manage.py runserver"
echo "2. Run this script: bash test_api.sh"
echo "3. For detailed testing, see TESTING_GUIDE.md"
