# 📚 API Documentation - Smart Budget Planner

## Base URL
```
http://localhost:5000
```

## Response Format

All API responses return JSON with the following structure:

### Success Response
```json
{
    "success": true,
    "data": {...},
    "message": "Optional message"
}
```

### Error Response
```json
{
    "success": false,
    "error": "Error message"
}
```

---

## 📥 Expense Endpoints

### 1. Get All Expenses
**Endpoint:** `GET /api/expenses`

**Description:** Fetch all recorded expenses

**Response (200 OK):**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "amount": 45.50,
            "category": "Food",
            "description": "Lunch at restaurant",
            "date": "2024-05-10"
        }
    ],
    "total_count": 1
}
```

**Example:**
```bash
curl http://localhost:5000/api/expenses
```

---

### 2. Create New Expense
**Endpoint:** `POST /api/expenses`

**Description:** Add a new expense

**Request Body:**
```json
{
    "amount": 45.50,
    "category": "Food",
    "description": "Lunch",
    "date": "2024-05-10"
}
```

**Request Headers:**
```
Content-Type: application/json
```

**Parameters:**
| Name | Type | Required | Notes |
|------|------|----------|-------|
| amount | float | Yes | Must be > 0 |
| category | string | Yes | See categories below |
| description | string | No | Optional |
| date | string | Yes | Format: YYYY-MM-DD |

**Categories:**
- Food
- Transportation
- Entertainment
- Shopping
- Utilities
- Healthcare
- Education
- Other

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 2,
        "amount": 45.50,
        "category": "Food",
        "description": "Lunch",
        "date": "2024-05-10"
    },
    "message": "Expense created successfully"
}
```

**Error (400 Bad Request):**
```json
{
    "success": false,
    "error": "Missing required fields: amount, category, date"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.50,
    "category": "Food",
    "description": "Lunch",
    "date": "2024-05-10"
  }'
```

---

### 3. Get Specific Expense
**Endpoint:** `GET /api/expenses/<id>`

**Description:** Fetch a specific expense by ID

**URL Parameters:**
- `id` (integer): Expense ID

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "amount": 45.50,
        "category": "Food",
        "description": "Lunch",
        "date": "2024-05-10"
    }
}
```

**Error (404 Not Found):**
```json
{
    "success": false,
    "error": "Expense not found"
}
```

**Example:**
```bash
curl http://localhost:5000/api/expenses/1
```

---

### 4. Update Expense
**Endpoint:** `PUT /api/expenses/<id>`

**Description:** Update an existing expense

**URL Parameters:**
- `id` (integer): Expense ID

**Request Body:** (all fields optional)
```json
{
    "amount": 50.00,
    "category": "Dining",
    "description": "Dinner",
    "date": "2024-05-11"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "amount": 50.00,
        "category": "Dining",
        "description": "Dinner",
        "date": "2024-05-11"
    },
    "message": "Expense updated successfully"
}
```

**Example:**
```bash
curl -X PUT http://localhost:5000/api/expenses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "category": "Food"
  }'
```

---

### 5. Delete Expense
**Endpoint:** `DELETE /api/expenses/<id>`

**Description:** Delete an expense

**URL Parameters:**
- `id` (integer): Expense ID

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Expense deleted successfully"
}
```

**Error (404 Not Found):**
```json
{
    "success": false,
    "error": "Expense not found"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/expenses/1
```

---

## 💰 Budget Endpoints

### 1. Get Budget Information
**Endpoint:** `GET /api/budget`

**Description:** Get current budget and spending status

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "monthly_limit": 5000.00,
        "total_spent": 1234.56,
        "remaining": 3765.44,
        "percentage_used": 24.69,
        "status": "safe"
    }
}
```

**Status Values:**
- `safe`: 0-79% used
- `warning`: 80-99% used
- `exceeded`: 100%+ used

**Example:**
```bash
curl http://localhost:5000/api/budget
```

---

### 2. Set/Update Budget
**Endpoint:** `POST /api/budget`

**Description:** Set or update the monthly budget limit

**Request Body:**
```json
{
    "monthly_limit": 6000.00
}
```

**Parameters:**
| Name | Type | Required | Notes |
|------|------|----------|-------|
| monthly_limit | float | Yes | Must be > 0 |

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "monthly_limit": 6000.00
    },
    "message": "Budget updated successfully"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/budget \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_limit": 6000.00
  }'
```

---

## 📊 Analytics Endpoints

### 1. Category Summary
**Endpoint:** `GET /api/analytics/category-summary`

**Description:** Get spending summary by category

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "categories": [
            {
                "category": "Food",
                "total": 450.50,
                "count": 10,
                "average": 45.05
            },
            {
                "category": "Transportation",
                "total": 200.00,
                "count": 5,
                "average": 40.00
            }
        ],
        "highest_category": {
            "category": "Food",
            "total": 450.50,
            "count": 10,
            "average": 45.05
        },
        "total": 650.50,
        "average_spending": 42.33
    }
}
```

**Example:**
```bash
curl http://localhost:5000/api/analytics/category-summary
```

---

### 2. Expense Trends
**Endpoint:** `GET /api/analytics/trends`

**Description:** Get expense trends for last 30 days

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "daily_expenses": [
            {
                "date": "2024-05-10",
                "amount": 100.00
            },
            {
                "date": "2024-05-11",
                "amount": 75.50
            }
        ],
        "weekly_summary": [
            {
                "week": "2024-05-06",
                "amount": 500.00
            }
        ]
    }
}
```

**Example:**
```bash
curl http://localhost:5000/api/analytics/trends
```

---

### 3. Smart Insights
**Endpoint:** `GET /api/analytics/insights`

**Description:** Get AI-powered spending insights and recommendations

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "insights": [
            {
                "type": "warning",
                "message": "💡 You have used 85% of your budget"
            },
            {
                "type": "info",
                "message": "📊 Highest spending: Food ($450.50)"
            }
        ],
        "total_spent": 1234.56,
        "monthly_limit": 5000.00,
        "remaining": 3765.44
    }
}
```

**Insight Types:**
- `success`: Positive feedback
- `warning`: Caution needed
- `danger`: Alert needed
- `info`: Information

**Example:**
```bash
curl http://localhost:5000/api/analytics/insights
```

---

### 4. Chart Data
**Endpoint:** `GET /api/analytics/chart-data`

**Description:** Get data formatted for Chart.js visualizations

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "pie_chart": {
            "labels": ["Food", "Transportation", "Entertainment"],
            "data": [450.50, 200.00, 150.00]
        },
        "bar_chart": {
            "labels": ["2024-05-04", "2024-05-05", "2024-05-06"],
            "data": [100.00, 75.50, 125.00]
        },
        "line_chart": {
            "labels": ["2024-04-10", "2024-04-11", "2024-04-12"],
            "data": [100.00, 110.00, 105.00]
        }
    }
}
```

**Example:**
```bash
curl http://localhost:5000/api/analytics/chart-data
```

---

## HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET request |
| 201 | Created | Expense successfully added |
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | Expense doesn't exist |
| 500 | Server Error | Database error |

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider implementing:
- Request rate limiting
- API key authentication
- Rate limit headers

---

## Error Handling

### Common Errors

**Invalid Amount:**
```json
{
    "success": false,
    "error": "Invalid amount: Amount must be positive"
}
```

**Invalid Date Format:**
```json
{
    "success": false,
    "error": "Invalid date format. Use YYYY-MM-DD"
}
```

**Missing Required Fields:**
```json
{
    "success": false,
    "error": "Missing required fields: amount, category, date"
}
```

---

## Authentication

Current version does not require authentication. For production, implement:
- JWT tokens
- User session management
- API key validation

---

## CORS Configuration

Currently, CORS is enabled for all origins. For production, restrict to:
```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

---

## Testing with cURL

### Test Create Expense
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.00,
    "category": "Food",
    "description": "Breakfast",
    "date": "2024-05-10"
  }'
```

### Test Get All Expenses
```bash
curl http://localhost:5000/api/expenses
```

### Test Update Budget
```bash
curl -X POST http://localhost:5000/api/budget \
  -H "Content-Type: application/json" \
  -d '{"monthly_limit": 7000}'
```

### Test Get Insights
```bash
curl http://localhost:5000/api/analytics/insights
```

---

## Testing with Postman

1. Import the collection
2. Set base URL to `http://localhost:5000`
3. Run individual requests
4. Test different scenarios

---

## API Versioning

Current API Version: **v1.0** (no version prefix)

Future versions may use: `/api/v2/expenses`

---

## Best Practices

1. **Always include Content-Type header** for POST/PUT requests
2. **Validate dates** in YYYY-MM-DD format
3. **Handle errors** gracefully in your client
4. **Use appropriate HTTP methods** (GET, POST, PUT, DELETE)
5. **Check success field** before accessing data

---

**API Documentation Version:** 1.0
**Last Updated:** May 2024
