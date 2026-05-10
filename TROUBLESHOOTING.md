# 🆘 Troubleshooting Guide - Smart Budget Planner

## Common Issues & Solutions

### 🔴 Installation Issues

#### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Problem**: Python can't find Flask or other dependencies

**Solution**:
```bash
# Method 1: Install all dependencies
pip install -r requirements.txt

# Method 2: Install individually
pip install Flask==2.3.3
pip install pandas==2.0.3
pip install numpy==1.24.3

# Method 3: Check if pip is up to date
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify Installation**:
```bash
python -c "import flask; print(flask.__version__)"
python -c "import pandas; print(pandas.__version__)"
```

---

#### Issue 2: "Python not found" or "command not found: python"

**Problem**: Python is not installed or not in PATH

**Solution on macOS/Linux**:
```bash
# Check Python version
python3 --version

# Use python3 instead
python3 app.py
```

**Solution on Windows**:
```cmd
# Check Python version
python --version

# Add Python to PATH manually through Settings
# Or reinstall Python and check "Add Python to PATH"
```

---

#### Issue 3: "Permission denied" when running Python

**Problem**: No execute permissions on file

**Solution on macOS/Linux**:
```bash
chmod +x app.py
chmod +x database.py
python app.py
```

**Solution on Windows**:
- Right-click file → Properties → Security → Edit
- Grant permissions to your user

---

### 🔴 Database Issues

#### Issue 4: "No such table: expenses"

**Problem**: Database not initialized

**Solution**:
```bash
# Initialize database
python database.py
```

**Output Should Be**:
```
Database initialized successfully!
```

---

#### Issue 5: "database.db is locked"

**Problem**: Database file is locked by another process

**Solution**:
```bash
# Close all running instances of the app
# Ctrl+C in all terminals

# Verify no processes are using it
lsof | grep database.db  # macOS/Linux

# Delete lock file if it exists
rm database.db-wal
rm database.db-shm

# Restart the application
python app.py
```

---

#### Issue 6: "No such column: monthly_limit"

**Problem**: Database schema not matching

**Solution**:
```bash
# Backup existing database
cp database.db database.db.backup

# Delete database
rm database.db

# Reinitialize
python database.py

# Restart app
python app.py
```

---

### 🔴 Port & Server Issues

#### Issue 7: "Address already in use" or "Port 5000 is in use"

**Problem**: Another application is using port 5000

**Solution Option 1**: Stop other applications using port 5000

**macOS/Linux - Find process**:
```bash
lsof -i :5000
kill -9 <PID>
```

**Windows - Find process**:
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Solution Option 2**: Change Flask port in app.py

Edit the last line of `app.py`:
```python
# Before
app.run(debug=True, host='localhost', port=5000)

# After (use any port not in use, e.g., 5001-5010)
app.run(debug=True, host='localhost', port=5001)
```

Then access: `http://localhost:5001`

---

#### Issue 8: "Address cannot be assigned"

**Problem**: Localhost not configured properly

**Solution**:
```python
# In app.py, change host
app.run(debug=True, host='0.0.0.0', port=5000)

# Then access via
http://127.0.0.1:5000
# or
http://localhost:5000
# or
http://<your-ip>:5000
```

---

#### Issue 9: Application crashes immediately

**Problem**: Syntax errors or import issues

**Solution**:
```bash
# Check for syntax errors
python -m py_compile app.py
python -m py_compile database.py

# Run with full error output
python -u app.py

# Check for import errors
python -c "import app"
```

---

### 🔴 Browser & Frontend Issues

#### Issue 10: "Page not loading" / "Blank page"

**Problem**: Frontend can't load or JavaScript errors

**Solution**:
1. **Check browser console** (F12 → Console tab):
   - Look for error messages
   - Check Network tab for failed requests

2. **Common causes**:
   ```bash
   # Flask not running - check terminal
   # Ports don't match - verify localhost:5000
   # File paths wrong - check static file paths
   # JavaScript errors - fix in console output
   ```

3. **Fix**:
   - Refresh page: F5 or Cmd+R
   - Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (macOS)
   - Clear cache: DevTools → Application → Clear Storage

---

#### Issue 11: Styling looks broken / CSS not loading

**Problem**: CSS file not served correctly

**Solution**:
```bash
# Check file exists
ls static/css/style.css

# Verify Flask is serving static files
# In app.py, should have:
app = Flask(__name__)

# Then access in HTML:
{{ url_for('static', filename='css/style.css') }}

# Hard refresh browser
# Clear cache and restart browser
```

---

#### Issue 12: Charts not displaying

**Problem**: Chart.js library not loaded or data missing

**Solution**:
1. **Check browser console for errors**
   - F12 → Console tab
   - Look for Chart.js errors

2. **Verify Chart.js CDN** in index.html:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
   ```

3. **Check if expenses exist**:
   - Add at least one expense
   - Wait for dashboard to load
   - Refresh page

4. **Debug**:
   ```javascript
   // In browser console
   console.log(pieChart)
   console.log(barChart)
   console.log(lineChart)
   ```

---

#### Issue 13: Buttons not working / Forms not submitting

**Problem**: JavaScript errors or event listeners not attached

**Solution**:
```bash
# Check browser console (F12)
# Look for JavaScript errors

# Verify JavaScript file is loaded
# In Network tab, check script.js loads

# Restart browser completely
# Try different browser (Chrome, Firefox, Safari)
```

---

#### Issue 14: "CORS error" or "blocked by CORS policy"

**Problem**: Browser blocking requests due to CORS

**Solution** (Frontend is on different port):
```python
# In app.py, add CORS support
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Then run
python app.py
```

---

### 🔴 API Issues

#### Issue 15: API endpoints returning 404

**Problem**: Routes not registered or wrong URL

**Solution**:
```bash
# Verify route exists in app.py
# Check exact endpoint name
# Ensure Flask is running

# Test endpoint with curl
curl http://localhost:5000/api/expenses
curl http://localhost:5000/api/budget
```

---

#### Issue 16: API returning "500 Internal Server Error"

**Problem**: Server-side error in route handler

**Solution**:
```bash
# Check terminal output for detailed error
# Look for traceback

# Common causes:
# - Database error
# - Missing imports
# - Syntax error
# - Invalid data processing

# Test with curl to see error
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"amount": "invalid"}'
```

---

#### Issue 17: Expense not saving / API returns 400 error

**Problem**: Invalid data sent to API

**Solution**:
```javascript
// Verify data format
console.log({
    amount: 25.50,      // Must be number > 0
    category: "Food",   // Must be valid category
    date: "2024-05-10", // Must be YYYY-MM-DD format
    description: "Lunch" // Can be empty
})

// Check browser console for error details
```

---

#### Issue 18: Charts not updating after adding expense

**Problem**: Charts not refreshed or data not fetched

**Solution**:
```bash
# Wait a moment after adding expense
# Browser may need time to fetch data

# Try manual refresh
# Click "Refresh" button on dashboard

# Check browser console for fetch errors
# Verify API endpoint returns new data
```

---

### 🔴 Performance Issues

#### Issue 19: Application is slow / unresponsive

**Problem**: Too many expenses or inefficient queries

**Solution**:
```python
# Optimize database queries in database.py
# Add indexes to frequently queried columns
# Limit results with pagination (future enhancement)

# Check browser performance
# F12 → Performance tab
# Record and analyze
```

---

#### Issue 20: Charts take long time to render

**Problem**: Too much data or inefficient Chart.js rendering

**Solution**:
```javascript
// In script.js, limit data points
// Use data aggregation
// Implement pagination

// Browser DevTools
// Check CPU usage
// Monitor memory
```

---

### 🟡 Data Loss Issues

#### Issue 21: Data disappeared after closing app

**Problem**: Data not saved to database

**Solution**:
```bash
# Verify database file exists
ls -la database.db

# Check if data is in database
sqlite3 database.db "SELECT COUNT(*) FROM expenses;"

# Backup important data
cp database.db database.db.backup

# Export as CSV before major changes
```

---

#### Issue 22: Cannot edit/delete expenses

**Problem**: Button click not working or API error

**Solution**:
1. **Check JavaScript console** for errors
2. **Verify expense exists** with correct ID
3. **Test with API**:
   ```bash
   # Test update
   curl -X PUT http://localhost:5000/api/expenses/1 \
     -H "Content-Type: application/json" \
     -d '{"amount": 30.00}'
   
   # Test delete
   curl -X DELETE http://localhost:5000/api/expenses/1
   ```

---

### 🟡 Browser-Specific Issues

#### Issue 23: Works in Chrome but not Firefox

**Problem**: Browser compatibility

**Solution**:
- Update browser to latest version
- Check for JavaScript version issues
- Test in different browsers
- Use fetch API (not XMLHttpRequest)
- Avoid ES6 features if old browser

---

#### Issue 24: Mobile version doesn't work

**Problem**: Responsive design issues

**Solution**:
```bash
# Test with Chrome DevTools mobile view
# F12 → Toggle device toolbar (Ctrl+Shift+M)

# Verify CSS breakpoints
# Check touch events
# Test on actual mobile device

# Common issues:
# - Font too small
# - Buttons too small
# - Sidebar overlapping content
# - Horizontal scrolling
```

---

### 🟢 Quick Fix Checklist

When something breaks, try these in order:

1. **Restart everything**
   ```bash
   Ctrl+C (stop app)
   Wait 5 seconds
   python app.py (restart)
   ```

2. **Hard refresh browser**
   - Ctrl+Shift+R (Windows/Linux)
   - Cmd+Shift+R (macOS)

3. **Clear browser storage**
   - F12 → Application → Clear Storage

4. **Check browser console**
   - F12 → Console
   - Look for red errors

5. **Test API with curl**
   ```bash
   curl http://localhost:5000/api/expenses
   ```

6. **Check terminal output**
   - Look for error messages
   - Check database operations

7. **Restart Python environment**
   ```bash
   Ctrl+C
   deactivate
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python app.py
   ```

---

## 📞 Getting More Help

### Check These Resources

1. **Flask Documentation**
   - https://flask.palletsprojects.com

2. **Pandas Documentation**
   - https://pandas.pydata.org/docs

3. **SQLite Documentation**
   - https://www.sqlite.org/docs.html

4. **Chart.js Documentation**
   - https://www.chartjs.org/docs

5. **MDN Web Docs**
   - https://developer.mozilla.org

---

## 💾 Backup & Recovery

### Regular Backups
```bash
# Weekly backup
cp database.db database.db.$(date +%Y%m%d).backup

# Export to CSV
# Use Export Data button in Settings
```

### Recovery Process
```bash
# If database corrupted
# 1. Backup current database
cp database.db database.db.corrupted

# 2. Delete corrupted database
rm database.db

# 3. Reinitialize
python database.py

# 4. Restart app
python app.py

# 5. Re-enter important data or restore from backup
```

---

## ⚡ Performance Tuning

### Optimize Database Queries
```python
# In database.py
# Use efficient queries
# Add LIMIT clauses
# Use indexes
```

### Optimize Frontend
```javascript
// In script.js
// Debounce event handlers
// Cache DOM elements
// Minimize reflows
```

### Optimize CSS
```css
/* Use minimal animations */
/* Reduce file size */
/* Use minified version in production */
```

---

## 🔐 Security Checklist

- [x] Validate all input data
- [x] Escape output properly
- [x] Use parameterized queries
- [x] Handle errors safely
- [x] Check user permissions
- [x] Rate limit API calls (optional)
- [x] Use HTTPS in production
- [x] Secure sensitive data

---

## 📝 Debug Tips

### Enable Debug Mode
```python
# In app.py
app.run(debug=True)  # Already enabled

# Shows detailed errors in browser
# Auto-reloads on file changes
```

### Add Console Logging
```python
# In Python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add to functions
print(f"Debug: {variable}")
```

```javascript
// In JavaScript
console.log('Debug:', variable);
console.table(arrayOfObjects);
console.time('timer');
// ... code ...
console.timeEnd('timer');
```

---

## 🎯 Final Troubleshooting Steps

If nothing else works:

1. **Check all prerequisites**
   - Python 3.8+? `python --version`
   - Dependencies installed? `pip list`
   - Database initialized? `ls database.db`

2. **Review logs**
   - Terminal output
   - Browser console (F12)
   - Database error logs

3. **Isolate the problem**
   - Test backend with curl
   - Test frontend with hardcoded data
   - Test database directly

4. **Recreate from scratch**
   - Delete database.db
   - Run `python database.py`
   - Restart `python app.py`
   - Clear browser cache

5. **Seek help**
   - Check documentation
   - Review code comments
   - Check Stack Overflow
   - Review error messages carefully

---

**Remember**: Most issues are solved by:
- Restarting the application
- Clearing browser cache
- Checking error messages
- Reviewing documentation

Good luck! 🚀

---

**Troubleshooting Guide Version**: 1.0
**Last Updated**: May 2024
