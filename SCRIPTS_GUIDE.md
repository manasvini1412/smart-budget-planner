# 🚀 Shell Scripts Guide - Smart Budget Planner

Complete guide to using the startup and shutdown scripts for the Smart Budget Planner application.

---

## 📋 Available Scripts

### macOS/Linux Scripts
- `run.sh` - Universal control script (start, stop, restart, status)
- `start.sh` - Start the application
- `stop.sh` - Stop the application

### Windows Scripts
- `run.bat` - Universal control script (start, stop, restart, status)
- `start.bat` - Start the application
- `stop.bat` - Stop the application

---

## 🎯 Quick Start

### macOS/Linux

**Make scripts executable (first time only):**
```bash
chmod +x start.sh stop.sh run.sh
```

**Start the app:**
```bash
./run.sh start
```

**Stop the app:**
```bash
./run.sh stop
```

### Windows

**Start the app:**
```cmd
run.bat start
```

**Stop the app:**
```cmd
run.bat stop
```

---

## 📖 Detailed Usage

### macOS/Linux Universal Script (`run.sh`)

#### Start Application
```bash
./run.sh start
```

**What it does:**
- ✓ Checks Python installation
- ✓ Verifies all dependencies
- ✓ Initializes database if needed
- ✓ Starts Flask server on port 5000
- ✓ Opens instructions for accessing the app

**Output:**
```
═══════════════════════════════════════════════════════════
    🚀 Smart Budget Planner - Startup Script
═══════════════════════════════════════════════════════════

[1/4] Checking Python installation...
✓ Python found: 3.9.0

[2/4] Checking Python dependencies...
✓ All dependencies are installed

[3/4] Initializing database...
✓ Database already exists

[4/4] Starting Flask application...

═══════════════════════════════════════════════════════════
    ✨ Smart Budget Planner is running!
═══════════════════════════════════════════════════════════

📱 Open your browser and navigate to:
   http://localhost:5000

⏹️  To stop the application, press: Ctrl + C
```

#### Stop Application
```bash
./run.sh stop
```

**What it does:**
- ✓ Finds Flask process on port 5000
- ✓ Gracefully shuts down the application
- ✓ Force kills if needed
- ✓ Verifies process stopped

**Output:**
```
═══════════════════════════════════════════════════════════
    ⏹️  Smart Budget Planner - Shutdown Script
═══════════════════════════════════════════════════════════

[1/2] Checking for running processes on port 5000...
✓ Found process (PID: 12345) on port 5000

[2/2] Stopping the application...

✓ Process stopped successfully

═══════════════════════════════════════════════════════════
    ✨ Smart Budget Planner has been shut down
═══════════════════════════════════════════════════════════

To start again, run: ./start.sh
```

#### Restart Application
```bash
./run.sh restart
```

**What it does:**
- Stops the currently running application
- Waits 2 seconds
- Starts the application again

#### Check Status
```bash
./run.sh status
```

**What it does:**
- ✓ Checks if app is running on port 5000
- ✓ Shows process ID (PID)
- ✓ Shows port and URL
- ✓ Displays start/stop commands

**Output (Running):**
```
═══════════════════════════════════════════════════════════
    📊 Smart Budget Planner - Status
═══════════════════════════════════════════════════════════

✓ Application is RUNNING

Details:
  Process ID: 12345
  Port: 5000
  URL: http://localhost:5000

Stop command: ./run.sh stop
```

**Output (Stopped):**
```
═══════════════════════════════════════════════════════════
    📊 Smart Budget Planner - Status
═══════════════════════════════════════════════════════════

✗ Application is STOPPED

Start command: ./run.sh start
```

#### Show Help
```bash
./run.sh help
```

or just:

```bash
./run.sh
```

---

### Windows Universal Script (`run.bat`)

#### Start Application
```cmd
run.bat start
```

#### Stop Application
```cmd
run.bat stop
```

#### Restart Application
```cmd
run.bat restart
```

#### Check Status
```cmd
run.bat status
```

#### Show Help
```cmd
run.bat help
```

or just:

```cmd
run.bat
```

---

## 🔧 Individual Scripts

### Using Individual Start Scripts

#### macOS/Linux
```bash
./start.sh
```

#### Windows
```cmd
start.bat
```

**Note:** Individual scripts are automatically called by the universal script.

---

### Using Individual Stop Scripts

#### macOS/Linux
```bash
./stop.sh
```

#### Windows
```cmd
stop.bat
```

**Note:** Individual scripts are automatically called by the universal script.

---

## 📊 What Each Script Does

### start.sh / start.bat

1. **Check Python**: Verifies Python 3.8+ is installed
2. **Check Dependencies**: Ensures Flask, Pandas, NumPy are installed
3. **Install if Needed**: Runs `pip install -r requirements.txt`
4. **Initialize Database**: Runs `python database.py` if needed
5. **Check Port**: Verifies port 5000 is available
6. **Start App**: Runs `python app.py`

### stop.sh / stop.bat

1. **Find Process**: Locates Flask process on port 5000
2. **Graceful Shutdown**: Sends SIGTERM signal
3. **Wait**: Gives process time to shut down
4. **Force Kill if Needed**: Sends SIGKILL if graceful fails
5. **Verify**: Confirms process stopped

### run.sh / run.bat

1. **Route Commands**: Directs to appropriate script
2. **Manage Lifecycle**: Handles start, stop, restart, status
3. **Show Status**: Displays current application state
4. **Error Handling**: Catches and reports issues

---

## ✅ Common Scenarios

### Scenario 1: Fresh Start
```bash
# First time setup - makes scripts executable
chmod +x run.sh start.sh stop.sh

# Start the app
./run.sh start
```

### Scenario 2: Regular Daily Use
```bash
# Start in the morning
./run.sh start

# Do work...

# Stop when done
./run.sh stop
```

### Scenario 3: Troubleshoot Issues
```bash
# Check if app is running
./run.sh status

# Restart if having issues
./run.sh restart

# Check details
lsof -i :5000
```

### Scenario 4: Port Already in Use
```bash
# See what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Try starting again
./run.sh start
```

### Scenario 5: Multiple Sessions
```bash
# Terminal 1: Start with verbose output
./start.sh

# Terminal 2: Check status
./run.sh status

# Terminal 2: Stop when ready
./run.sh stop
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied" on macOS/Linux

**Solution:**
```bash
chmod +x run.sh start.sh stop.sh
./run.sh start
```

### Issue: "Port 5000 is already in use"

**macOS/Linux:**
```bash
# Find process
lsof -i :5000

# Kill process
kill -9 <PID>

# Or change port in app.py
```

**Windows:**
```cmd
# Find process
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F

# Or change port in app.py
```

### Issue: "Python not found"

**macOS/Linux:**
```bash
# Check if python3 is available
python3 --version

# Edit start.sh to use python3 instead of python
# Change: python app.py
# To: python3 app.py
```

**Windows:**
```cmd
# Make sure Python is in PATH
python --version

# If not found, reinstall Python and check "Add to PATH"
```

### Issue: Dependencies not installed

**macOS/Linux:**
```bash
pip install -r requirements.txt
./run.sh start
```

**Windows:**
```cmd
pip install -r requirements.txt
run.bat start
```

### Issue: Database errors

**macOS/Linux:**
```bash
python database.py
./run.sh start
```

**Windows:**
```cmd
python database.py
run.bat start
```

---

## 🔄 Process Management

### View All Python Processes

**macOS/Linux:**
```bash
ps aux | grep python
```

**Windows:**
```cmd
tasklist | findstr python
```

### View Specific Port Usage

**macOS/Linux:**
```bash
lsof -i :5000
```

**Windows:**
```cmd
netstat -ano | findstr :5000
```

### Kill Process by PID

**macOS/Linux:**
```bash
kill -9 <PID>
```

**Windows:**
```cmd
taskkill /PID <PID> /F
```

---

## 📝 Script Customization

### Change Port

Edit `app.py` and find the last line:

```python
# Before
app.run(debug=True, host='localhost', port=5000)

# After (use different port)
app.run(debug=True, host='localhost', port=5001)
```

Then use:
```bash
./run.sh start
```

### Change Python Command

If using `python3` instead of `python`:

**macOS/Linux - Edit start.sh:**
```bash
# Line to change
$PYTHON_CMD app.py

# Change PYTHON_CMD selection logic
```

**Windows - Edit start.bat:**
```batch
REM Line to change
python app.py

REM Change to
python3 app.py
```

### Add Pre-Startup Tasks

Edit `start.sh` or `start.bat` to add tasks before starting, for example:

**macOS/Linux:**
```bash
# Before starting app
echo "Backing up database..."
cp database.db database.db.backup
```

---

## 🎯 Automation

### Cron Job (macOS/Linux - Auto Start)

Create a cron job to start app on reboot:

```bash
# Edit crontab
crontab -e

# Add this line (starts on reboot)
@reboot /path/to/smart-budget-planner/run.sh start
```

### Task Scheduler (Windows - Auto Start)

Create a scheduled task:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "At Startup"
4. Set action to: `C:\path\to\smart-budget-planner\run.bat start`

---

## 📚 Script Reference

### Environment Variables (macOS/Linux)

```bash
# Available in scripts
SCRIPT_DIR     # Directory where script is located
PYTHON_CMD     # Python command (python or python3)
PYTHON_VERSION # Python version string
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error/Failure |

---

## 🔐 Security Notes

- Scripts run with current user permissions
- Database file should have proper permissions
- Logs can contain sensitive info (check accordingly)
- For production, use proper process managers

---

## 💡 Pro Tips

1. **Create alias for easier access:**
   ```bash
   alias budget="~/path/to/smart-budget-planner/run.sh"
   # Then use: budget start
   ```

2. **Use tmux for background running:**
   ```bash
   tmux new-session -d -s budget "./run.sh start"
   tmux kill-session -t budget
   ```

3. **Monitor with watch:**
   ```bash
   watch -n 5 "./run.sh status"
   ```

4. **Redirect logs:**
   ```bash
   ./run.sh start > app.log 2>&1 &
   ```

---

## 📞 Support

If scripts don't work:

1. Check file permissions: `ls -la run.sh`
2. Verify Python: `python --version`
3. Check dependencies: `pip list`
4. Review error messages carefully
5. Check the TROUBLESHOOTING.md guide

---

**Scripts Version**: 1.0
**Compatible With**: Smart Budget Planner v1.0
**Last Updated**: May 2024

Enjoy automated startup! 🚀
