# Expense & Budget Management API - Postman Testing Guide

## Base URL
```
http://localhost:8000
```

## API Version
```
/api/v1
```

---

## 📋 Table of Contents
1. [Authentication APIs](#authentication-apis)
2. [User Management APIs](#user-management-apis)
3. [Expense Management APIs](#expense-management-apis)
4. [Budget Summary APIs](#budget-summary-apis)

---

## 🔐 Authentication APIs

### 1. User Login (OAuth2 Form)
**Endpoint:** `POST /api/v1/auth/login`

**Content-Type:** `application/x-www-form-urlencoded`

**Body (form-data):**
```
username: john_doe
password: password123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 2. User Login (JSON Body)
**Endpoint:** `POST /api/v1/auth/login-json`

**Content-Type:** `application/json`

**Body (raw JSON):**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 👤 User Management APIs

### 1. Create User
**Endpoint:** `POST /api/v1/users/`

**Content-Type:** `application/json`

**Body (raw JSON):**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "salary": 50000.00
}
```

**Response:**
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "salary": 50000.0,
  "is_active": true,
  "created_at": "2025-01-06T10:30:00",
  "updated_at": "2025-01-06T10:30:00"
}
```

---

### 2. Get User by ID
**Endpoint:** `GET /api/v1/users/{user_id}`

**Example:** `GET /api/v1/users/1`

**Headers:** None required

**Response:**
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "salary": 50000.0,
  "is_active": true,
  "created_at": "2025-01-06T10:30:00",
  "updated_at": "2025-01-06T10:30:00"
}
```

---

### 3. Get Current User Profile
**Endpoint:** `GET /api/v1/users/me/profile`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "salary": 50000.0,
  "is_active": true,
  "created_at": "2025-01-06T10:30:00",
  "updated_at": "2025-01-06T10:30:00"
}
```

---

### 4. Update User
**Endpoint:** `PUT /api/v1/users/{user_id}`

**Example:** `PUT /api/v1/users/1`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "salary": 60000.00,
  "email": "john.doe@example.com"
}
```

**Response:**
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john.doe@example.com",
  "salary": 60000.0,
  "is_active": true,
  "created_at": "2025-01-06T10:30:00",
  "updated_at": "2025-01-06T11:00:00"
}
```

---

### 5. Delete User
**Endpoint:** `DELETE /api/v1/users/{user_id}`

**Example:** `DELETE /api/v1/users/1`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

## 💰 Expense Management APIs

### 1. Create Expense
**Endpoint:** `POST /api/v1/expenses/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "user_id": 1,
  "name": "Grocery Shopping",
  "amount": 150.50,
  "category": "Food"
}
```

**Categories:** `Food`, `Transport`, `Entertainment`, `Utilities`, `Other`

**Response:**
```json
{
  "expense_id": 1,
  "user_id": 1,
  "name": "Grocery Shopping",
  "amount": 150.50,
  "category": "Food",
  "created_at": "2025-01-06T10:30:00"
}
```

---

### 2. Get User Expenses (All)
**Endpoint:** `GET /api/v1/expenses/{user_id}`

**Example:** `GET /api/v1/expenses/1`

**Response:**
```json
[
  {
    "expense_id": 1,
    "user_id": 1,
    "name": "Grocery Shopping",
    "amount": 150.50,
    "category": "Food",
    "created_at": "2025-01-06T10:30:00"
  },
  {
    "expense_id": 2,
    "user_id": 1,
    "name": "Uber Ride",
    "amount": 25.00,
    "category": "Transport",
    "created_at": "2025-01-06T11:00:00"
  }
]
```

---

### 3. Get User Expenses (Filtered by Day)
**Endpoint:** `GET /api/v1/expenses/{user_id}?day=2025-01-06`

**Example:** `GET /api/v1/expenses/1?day=2025-01-06`

**Response:** Same as above (filtered by day)

---

### 4. Get User Expenses (Filtered by Week)
**Endpoint:** `GET /api/v1/expenses/{user_id}?week=2&year=2025`

**Example:** `GET /api/v1/expenses/1?week=2&year=2025`

**Response:** Same as above (filtered by week)

---

### 5. Get User Expenses (Filtered by Month)
**Endpoint:** `GET /api/v1/expenses/{user_id}?month=1&year=2025`

**Example:** `GET /api/v1/expenses/1?month=1&year=2025`

**Response:** Same as above (filtered by month)

---

### 6. Get User Expenses (Filtered by Category)
**Endpoint:** `GET /api/v1/expenses/{user_id}?category=Food`

**Example:** `GET /api/v1/expenses/1?category=Food`

**Response:** Same as above (filtered by category)

---

### 7. Get User Expenses (Multiple Filters)
**Endpoint:** `GET /api/v1/expenses/{user_id}?month=1&year=2025&category=Food`

**Example:** `GET /api/v1/expenses/1?month=1&year=2025&category=Food`

**Response:** Same as above (filtered by month and category)

---

### 8. Get Expense by ID
**Endpoint:** `GET /api/v1/expenses/detail/{expense_id}`

**Example:** `GET /api/v1/expenses/detail/1`

**Response:**
```json
{
  "expense_id": 1,
  "user_id": 1,
  "name": "Grocery Shopping",
  "amount": 150.50,
  "category": "Food",
  "created_at": "2025-01-06T10:30:00"
}
```

---

### 9. Update Expense
**Endpoint:** `PUT /api/v1/expenses/{expense_id}`

**Example:** `PUT /api/v1/expenses/1`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "name": "Weekly Grocery Shopping",
  "amount": 175.00,
  "category": "Food"
}
```

**Response:**
```json
{
  "expense_id": 1,
  "user_id": 1,
  "name": "Weekly Grocery Shopping",
  "amount": 175.00,
  "category": "Food",
  "created_at": "2025-01-06T10:30:00"
}
```

---

### 10. Delete Expense
**Endpoint:** `DELETE /api/v1/expenses/{expense_id}`

**Example:** `DELETE /api/v1/expenses/1`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

## 📊 Budget Summary APIs

### 1. Get Budget Summary (All Expenses)
**Endpoint:** `GET /api/v1/expenses/totals/{user_id}`

**Example:** `GET /api/v1/expenses/totals/1`

**Response:**
```json
{
  "user_id": 1,
  "total_salary": 50000.00,
  "total_expense": 3300.50,
  "remaining_amount": 46699.50,
  "category_breakdown": {
    "Food": 1500.50,
    "Transport": 500.00,
    "Entertainment": 300.00,
    "Utilities": 800.00,
    "Other": 200.00
  }
}
```

---

### 2. Get Budget Summary (Filtered by Month)
**Endpoint:** `GET /api/v1/expenses/totals/{user_id}?month=1&year=2025`

**Example:** `GET /api/v1/expenses/totals/1?month=1&year=2025`

**Response:** Same as above (filtered by month)

---

### 3. Get Budget Summary (Filtered by Week)
**Endpoint:** `GET /api/v1/expenses/totals/{user_id}?week=2&year=2025`

**Example:** `GET /api/v1/expenses/totals/1?week=2&year=2025`

**Response:** Same as above (filtered by week)

---

### 4. Get Budget Summary (Filtered by Category)
**Endpoint:** `GET /api/v1/expenses/totals/{user_id}?category=Food`

**Example:** `GET /api/v1/expenses/totals/1?category=Food`

**Response:** Same as above (only Food category expenses)

---

## 🧪 Complete Testing Flow

### Step 1: Create a User
```
POST http://localhost:8000/api/v1/users/
```
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "salary": 75000.00
}
```

### Step 2: Login
```
POST http://localhost:8000/api/v1/auth/login-json
```
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```
**Copy the `access_token` from response**

### Step 3: Create Expenses (Use Token)
```
POST http://localhost:8000/api/v1/expenses/
Authorization: Bearer <your_token>
```
```json
{
  "user_id": 1,
  "name": "Supermarket",
  "amount": 250.75,
  "category": "Food"
}
```

Repeat with different categories:
```json
{
  "user_id": 1,
  "name": "Bus Pass",
  "amount": 50.00,
  "category": "Transport"
}
```

```json
{
  "user_id": 1,
  "name": "Netflix",
  "amount": 15.99,
  "category": "Entertainment"
}
```

```json
{
  "user_id": 1,
  "name": "Electricity Bill",
  "amount": 120.50,
  "category": "Utilities"
}
```

### Step 4: Get All Expenses
```
GET http://localhost:8000/api/v1/expenses/1
```

### Step 5: Get Budget Summary
```
GET http://localhost:8000/api/v1/expenses/totals/1
```

### Step 6: Test Filters
```
GET http://localhost:8000/api/v1/expenses/1?category=Food
GET http://localhost:8000/api/v1/expenses/1?month=1&year=2025
GET http://localhost:8000/api/v1/expenses/totals/1?category=Transport
```

---

## 🔧 Postman Environment Variables

Create these variables in Postman:

| Variable | Value |
|----------|-------|
| base_url | http://localhost:8000 |
| api_version | /api/v1 |
| access_token | (set after login) |
| user_id | (set after user creation) |

Then use:
```
{{base_url}}{{api_version}}/users/
```

---

## 🚨 Common Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already exists"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized to create expense for another user"
}
```

### 404 Not Found
```json
{
  "detail": "User with ID 999 not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "Amount must be greater than 0",
      "type": "value_error"
    }
  ]
}
```

---

## 📝 Notes

1. **Authentication:** Most endpoints require JWT token in Authorization header
2. **Categories:** Only these are valid: `Food`, `Transport`, `Entertainment`, `Utilities`, `Other`
3. **Amount Validation:** Must be greater than 0
4. **Date Format:** Use `YYYY-MM-DD` for day filter
5. **Week/Month:** Requires year parameter
6. **User Authorization:** Users can only modify their own data

---

## 🌐 API Documentation

Access interactive API documentation at:
- **Swagger UI:** http://localhost:8000/api/v1/docs
- **ReDoc:** http://localhost:8000/api/v1/redoc
