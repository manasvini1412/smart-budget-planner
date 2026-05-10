# 🚀 Quick Shell Scripts Reference

## 📋 Files Created

### Shell Scripts (macOS/Linux)
| File | Purpose | Usage |
|------|---------|-------|
| **run.sh** | Universal control script | `./run.sh [start\|stop\|restart\|status]` |
| **start.sh** | Startup script | `./start.sh` |
| **stop.sh** | Shutdown script | `./stop.sh` |

### Batch Scripts (Windows)
| File | Purpose | Usage |
|------|---------|-------|
| **run.bat** | Universal control script | `run.bat [start\|stop\|restart\|status]` |
| **start.bat** | Startup script | `start.bat` |
| **stop.bat** | Shutdown script | `stop.bat` |

### Documentation
| File | Content |
|------|---------|
| **SCRIPTS_GUIDE.md** | Comprehensive scripts manual |

---

## ⚡ Quick Commands

### macOS/Linux

```bash
# Make scripts executable (first time only)
chmod +x start.sh stop.sh run.sh

# Start the app
./run.sh start

# Stop the app
./run.sh stop

# Restart the app
./run.sh restart

# Check status
./run.sh status

# Show help
./run.sh help
```

### Windows

```cmd
# Start the app
run.bat start

# Stop the app
run.bat stop

# Restart the app
run.bat restart

# Check status
run.bat status

# Show help
run.bat help
```

---

## 🎯 What Scripts Do

### Startup Script Performs:
✅ Checks Python installation
✅ Verifies all dependencies
✅ Installs missing packages if needed
✅ Initializes SQLite database
✅ Checks port 5000 availability
✅ Starts Flask server
✅ Shows access instructions

### Shutdown Script Performs:
✅ Finds Flask process on port 5000
✅ Attempts graceful shutdown
✅ Force kills if necessary
✅ Verifies process stopped
✅ Shows confirmation message

---

## 📱 Typical Workflow

```bash
# 1. Navigate to project
cd /Users/manu/Projects/budgetPlanner/smart-budget-planner

# 2. Make scripts executable (first time only)
chmod +x run.sh

# 3. Start the application
./run.sh start

# 4. Open browser to http://localhost:5000

# 5. Use the application...

# 6. Stop when done
./run.sh stop
```

---

## 🔧 Common Tasks

### Check if app is running
```bash
./run.sh status
```

### Restart the app
```bash
./run.sh restart
```

### See help/usage
```bash
./run.sh help
```

### Manual port check (macOS/Linux)
```bash
lsof -i :5000
```

### Manual port check (Windows)
```cmd
netstat -ano | findstr :5000
```

---

## 📖 Full Documentation

For comprehensive guide including:
- Detailed setup instructions
- Troubleshooting issues
- Automation options
- Process management
- Customization tips

Read: **SCRIPTS_GUIDE.md**

---

## ✅ Setup Verification

After creating scripts, verify they work:

```bash
# 1. Check they're executable
ls -lh run.sh start.sh stop.sh

# 2. Test help command
./run.sh help

# 3. Check status
./run.sh status

# 4. Start app
./run.sh start

# 5. In another terminal
./run.sh status

# 6. Stop app
./run.sh stop
```

---

## 💡 Pro Tips

**Create an alias for easy access:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias budget="cd ~/Projects/budgetPlanner/smart-budget-planner && ./run.sh"

# Then use: budget start
```

**Use tmux for background running:**
```bash
tmux new-session -d -s budget "./run.sh start"
tmux kill-session -t budget
```

**Monitor app status continuously:**
```bash
watch -n 5 "./run.sh status"
```

---

## 🎉 Success Indicators

✓ Scripts are executable (chmod +x works)
✓ `./run.sh help` shows command list
✓ `./run.sh start` starts the app
✓ Browser shows app at http://localhost:5000
✓ `./run.sh status` shows running status
✓ `./run.sh stop` shuts down cleanly

---

**Ready to use!** Start with:
```bash
./run.sh start
```

Happy budgeting! 💰🚀
