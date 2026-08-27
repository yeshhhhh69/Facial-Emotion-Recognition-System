# Frontend Setup - Step by Step Commands

## Execute these commands in order in PowerShell/Terminal

### Step 1: Navigate to frontend directory
```powershell
cd "C:\Users\salel\OneDrive\Desktop\College files & projects\DL Project\Emotion Recognition\frontend"
```

### Step 2: Clean up old installations (if any issues)
```powershell
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item -Force package-lock.json -ErrorAction SilentlyContinue
```

### Step 3: Install all dependencies
```powershell
npm install --legacy-peer-deps
```

Wait for this to complete (may take 2-3 minutes)

### Step 4: Install Vite specifically (if needed)
```powershell
npm install vite @vitejs/plugin-react --save-dev
```

### Step 5: Start the development server
```powershell
npm run dev
```

OR if that doesn't work, try:
```powershell
.\node_modules\.bin\vite
```

OR use npx:
```powershell
npx vite
```

---

## Expected Output

You should see:
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

---

## If You Get Errors

**"Cannot find module 'vite'"**
```powershell
npm install
npm install vite --save-dev
npx vite
```

**"Port 5173 already in use"**
```powershell
npx vite --port 5174
```

**Still not working?**
```powershell
# Use global vite
npm install -g vite
vite
```

---

## Quick Copy-Paste (All in One)

```powershell
cd "C:\Users\salel\OneDrive\Desktop\College files & projects\DL Project\Emotion Recognition\frontend"
npm install --legacy-peer-deps
npm run dev
```

If that fails:
```powershell
npx vite
```

---

## After Frontend Starts

1. Open browser to `http://localhost:5173`
2. Make sure backend is running at `http://127.0.0.1:8000`
3. Test the webcam or upload an image!
