# 💰 Smart Budget Planner

A modern, responsive web application for managing expenses, tracking budgets, and analyzing spending habits with interactive charts and smart insights powered by Pandas and Chart.js.

## 🌟 Features

### 1. Dashboard
- **Key Metrics Display**: Total budget, total spent, remaining budget, budget percentage
- **Budget Alerts**: Real-time warnings when spending approaches or exceeds budget limits
- **Visual Progress Indicator**: Color-coded progress bar (green/yellow/red)
- **Interactive Charts**: 
  - Pie chart for category-wise spending distribution
  - Bar chart for last 7 days spending
  - Line chart for 30-day spending trends
- **Smart Insights**: AI-powered recommendations and observations
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

### 2. Expense Management
- **Add Expenses**: Quick and easy expense entry with validation
- **Edit Expenses**: Modify existing expenses anytime
- **Delete Expenses**: Remove expenses with confirmation
- **Expense Table**: View all expenses with date, category, description, and amount
- **Category Support**: 8 predefined categories (Food, Transportation, Entertainment, Shopping, Utilities, Healthcare, Education, Other)
- **Date Tracking**: Automatic tracking of expense dates

### 3. Budget Management
- **Set Monthly Budget**: Configure your monthly spending limit
- **Budget Alerts**:
  - Green (Safe): 0-79% of budget used
  - Yellow (Warning): 80-99% of budget used
  - Red (Exceeded): 100%+ of budget used
- **Real-time Calculation**: Automatic remaining budget calculation
- **Alert Levels**: Visual indicators for budget status

### 4. Smart Analytics
- **Category-wise Summary**: Spending breakdown by category with count and averages
- **Spending Trends**: Daily and weekly spending patterns
- **Highest Category**: Identification of highest spending category
- **Average Analysis**: Calculate average spending per category
- **Trend Analysis**: Visual representation of spending over time

### 5. Data Visualization (Chart.js)
- **Pie Charts**: Category distribution (doughnut style)
- **Bar Charts**: Last 7 days comparison
- **Line Charts**: 30-day trend with smooth interpolation
- **Interactive Elements**: Hover tooltips and legend controls
- **Responsive Charts**: Auto-adjust to container size

### 6. Data Management
- **CSV Export**: Download all expenses as CSV file
- **Date Organization**: Expenses sorted by date
- **Data Persistence**: All data stored in SQLite database

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: SQLite
- **Data Analysis**: Pandas & NumPy
- **Charts**: Chart.js
- **Architecture**: RESTful API

## 📁 Project Structure

```
smart-budget-planner/
│
├── app.py                          # Flask application with API routes
├── database.py                     # Database module for SQLite operations
├── requirements.txt                # Python dependencies
├── database.db                     # SQLite database (created on first run)
│
├── templates/
│   └── index.html                  # Main HTML template
│
└── static/
    ├── css/
    │   └── style.css               # Modern CSS styling
    └── js/
        └── script.js               # Frontend JavaScript logic
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone/Download the Project
```bash
# Navigate to project directory
cd smart-budget-planner
```

### Step 2: Create Virtual Environment (Optional but Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python database.py
```

This command will create the SQLite database with the default monthly budget of $5,000.

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 6: Access in Browser
Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Dashboard
1. View your monthly budget summary
2. Monitor budget status with color-coded alerts
3. Check spending by category with pie chart
4. View recent spending trends with bar and line charts
5. Read smart insights about your spending habits

### Adding an Expense
1. Click **"+ Add Expense"** button in the Expenses section
2. Fill in the expense details:
   - Amount (required)
   - Category (required)
   - Description (optional)
   - Date (required)
3. Click **"Save Expense"**
4. Dashboard updates automatically

### Editing an Expense
1. Go to the Expenses section
2. Find the expense in the table
3. Click **"Edit"** button
4. Modify the details
5. Click **"Save Expense"**

### Deleting an Expense
1. Go to the Expenses section
2. Find the expense in the table
3. Click **"Delete"** button
4. Confirm the deletion

### Setting Budget
1. Go to Settings section
2. Enter your desired monthly budget limit
3. Click **"Update Budget"**
4. Budget updates immediately

### Viewing Analytics
1. Click the **"Analytics"** tab
2. View category-wise spending summary
3. Check daily and weekly spending trends

### Exporting Data
1. Go to Settings section
2. Click **"📥 Export Data"** button
3. CSV file downloads to your computer

## 🔌 API Routes

### Expense Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses` | Get all expenses |
| POST | `/api/expenses` | Create new expense |
| GET | `/api/expenses/<id>` | Get specific expense |
| PUT | `/api/expenses/<id>` | Update expense |
| DELETE | `/api/expenses/<id>` | Delete expense |

### Budget Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/budget` | Get budget info |
| POST | `/api/budget` | Set/update budget |

### Analytics Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/category-summary` | Category breakdown |
| GET | `/api/analytics/trends` | Spending trends |
| GET | `/api/analytics/insights` | Smart insights |
| GET | `/api/analytics/chart-data` | Chart.js formatted data |

## 💾 Database Schema

### expenses table
```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
)
```

### budget table
```sql
CREATE TABLE budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monthly_limit REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
```

## 🎨 UI Features

### Modern Design
- Gradient sidebar with navigation
- Card-based layout
- Smooth animations and transitions
- Color-coded alerts and status indicators

### Responsive Layout
- Mobile-first design
- Tablet optimization
- Desktop enhanced experience
- Touch-friendly buttons

### Visual Hierarchy
- Clear typography with multiple font sizes
- Strategic use of colors
- Icon integration for quick recognition
- Whitespace for readability

## 🔐 Error Handling

- Form validation on both client and server
- Error messages for invalid operations
- Try-catch blocks in all API routes
- Toast notifications for user feedback
- Database connection error management

## ⚡ Performance Features

- Client-side data caching
- Optimized database queries
- Minimal API calls
- Chart canvas reuse
- CSS animations (GPU accelerated)

## 🌐 Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Future Enhancements

### 1. Authentication & User Management
```python
- User registration and login
- Password hashing with bcrypt
- JWT token authentication
- Multi-user support
- User profiles
```

### 2. Dark Mode
```css
- System preference detection
- Manual toggle
- Local storage persistence
- Smooth transition effects
```

### 3. AI & Predictions
```python
- Spending predictions using ML
- Budget recommendations
- Anomaly detection
- Seasonal analysis
```

### 4. Advanced Reporting
```python
- PDF report generation
- Monthly summaries
- Year-to-date analysis
- Custom date range reports
```

### 5. Cloud Deployment
```
- AWS Lambda/EC2
- Heroku integration
- Docker containerization
- Cloud database (AWS RDS, MongoDB Atlas)
```

### 6. Mobile App
```
- React Native app
- iOS App Store
- Google Play Store
- Push notifications
```

### 7. Advanced Features
```
- Recurring expenses
- Split expenses
- Bill reminders
- Budget goals
- Savings targets
- Expense categories customization
- Tags and labels
```

### 8. Integrations
```
- Bank account connection
- Automatic transaction import
- Payment gateway integration
- Cloud storage sync
```

## 🐛 Troubleshooting

### Database Issues
**Problem**: Database.db not created
**Solution**: Run `python database.py` to initialize

**Problem**: Database locked error
**Solution**: Close the application and restart it

### Port Already in Use
**Problem**: Port 5000 is already in use
**Solution**: 
```bash
# Change port in app.py
app.run(debug=True, host='localhost', port=5001)
```

### Missing Dependencies
**Problem**: Module not found error
**Solution**: 
```bash
pip install -r requirements.txt --upgrade
```

### CORS Issues
**Problem**: API calls failing from frontend
**Solution**: Ensure Flask is running on same localhost

## 📝 Code Examples

### Adding an Expense via API
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "category": "Food",
    "description": "Lunch at restaurant",
    "date": "2024-05-10"
  }'
```

### Getting Budget Info
```bash
curl http://localhost:5000/api/budget
```

### Updating Budget
```bash
curl -X POST http://localhost:5000/api/budget \
  -H "Content-Type: application/json" \
  -d '{"monthly_limit": 6000}'
```

## 📊 Sample Data

To test the application with sample data, expenses will be automatically added when you interact with the app. The default budget is set to $5,000.

## 🔧 Configuration

### Changing Default Budget
Edit `database.py`:
```python
cursor.execute('INSERT INTO budget (monthly_limit) VALUES (?)', (5000.0,))
```

### Changing Port
Edit `app.py`:
```python
app.run(debug=True, host='localhost', port=5000)
```

### Adding New Expense Categories
Edit `index.html` in the expense form:
```html
<option value="Category Name">🔀 Category Name</option>
```

## 📞 Support & Contact

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review the code comments
3. Check Flask and Pandas documentation
4. Verify all dependencies are installed

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Flask documentation and community
- Chart.js for beautiful visualizations
- Pandas for data analysis
- Bootstrap for CSS inspiration

## ✨ Tips for Best Results

1. **Regular Backups**: Periodically export your data
2. **Monthly Review**: Check analytics to identify spending patterns
3. **Budget Adjustment**: Update budget based on your needs
4. **Category Organization**: Be consistent with categorizing expenses
5. **Date Accuracy**: Record expenses with correct dates for accurate trends

---

**Version**: 1.0
**Last Updated**: May 2024
**Status**: Production Ready

Enjoy tracking your budget! 💰📊✨
