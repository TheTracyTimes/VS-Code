# Server Management Guide

## Port 8000 Already In Use Error

If you see this error:
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

This means the server is already running! Here are your options:

---

## Quick Fix (Automated)

### Option 1: Restart the Server
```bash
bash restart-server.sh
```

This will:
1. ✅ Find and stop any existing server
2. ✅ Start a fresh server instance
3. ✅ Use Python 3.11 automatically

### Option 2: Just Stop the Server
```bash
bash kill-server.sh
```

This will stop the server without restarting it.

---

## Manual Fix

### Step 1: Find the Process
```bash
lsof -ti:8000
```

This shows the Process ID (PID) using port 8000. Example output:
```
12345
```

### Step 2: Kill the Process
```bash
kill 12345
```

Replace `12345` with the actual PID from Step 1.

### Step 3: Force Kill (If Needed)
If the process won't die:
```bash
kill -9 12345
```

### Step 4: Start Fresh
```bash
cd web_app
python3.11 server.py
```

---

## Common Scenarios

### "I closed the terminal but server is still running"

The server runs as a background process even after you close the terminal.

**Fix:**
```bash
bash kill-server.sh
```

### "I want to restart the server to see new changes"

If you modified the code and want to reload:

**Fix:**
```bash
bash restart-server.sh
```

### "Port 8000 is already in use by another app"

Maybe you have another app using port 8000?

**Check what's using it:**
```bash
lsof -i:8000
```

**Start server on a different port:**
```bash
cd web_app
uvicorn server:app --host 0.0.0.0 --port 8080
```

Then open: `localhost:8080` in your browser.

---

## Server Commands Cheat Sheet

| Task | Command |
|------|---------|
| **Start server** | `cd web_app && python3.11 server.py` |
| **Stop server** | `bash kill-server.sh` |
| **Restart server** | `bash restart-server.sh` |
| **Find what's on port 8000** | `lsof -i:8000` |
| **Kill specific process** | `kill <PID>` |
| **Force kill process** | `kill -9 <PID>` |
| **Start on different port** | `cd web_app && uvicorn server:app --port 8080` |

---

## Keyboard Shortcuts

When the server is running in your terminal:

- **Ctrl+C** - Stop the server gracefully
- **Ctrl+Z** - Pause the server (not recommended)
- **Cmd+W** or **Cmd+Q** - Closes terminal but server keeps running!

⚠️ **Important:** Always use **Ctrl+C** to stop the server before closing the terminal!

---

## Troubleshooting

### Server won't stop

Try force kill:
```bash
kill -9 $(lsof -ti:8000)
```

### Multiple servers running

Find all Python processes:
```bash
ps aux | grep server.py
```

Kill them all:
```bash
pkill -f server.py
```

### Port still shows as in use

Wait 30 seconds - the OS needs time to release the port.

Or restart your computer (guaranteed fix).

### Need to run server in background

Use `nohup`:
```bash
cd web_app
nohup python3.11 server.py &
```

To stop it later:
```bash
pkill -f server.py
```

---

## Best Practices

1. **Always stop with Ctrl+C** before closing terminal
2. **Use restart-server.sh** when making code changes
3. **Check port first** with `lsof -ti:8000` if you get errors
4. **Use Python 3.11** (`python3.11 server.py`) for full functionality

---

## Need Help?

If none of these work, try:

1. Restart your terminal
2. Restart your computer
3. Check if another app is using port 8000
4. Try a different port (8080, 8888, etc.)

---

**Quick Reference:**
- Start: `cd web_app && python3.11 server.py`
- Stop: `Ctrl+C` or `bash kill-server.sh`
- Restart: `bash restart-server.sh`
