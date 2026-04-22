# 🚀 Quick Start Guide

Get your Face Emotion Detection app running in minutes!

---

## 🏃 Fast Track (2 Minutes)

### Windows
```powershell
# 1. Navigate to project directory
cd path\to\face_emotion_detection_model-main

# 2. Run the startup script
start.bat
```

### Linux/Mac
```bash
# 1. Navigate to project directory
cd path/to/face_emotion_detection_model-main

# 2. Make script executable
chmod +x start.sh

# 3. Run the startup script
./start.sh
```

### Manual Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py
```

---

## 🌐 Access Your App

Once running, open your browser:
- **Local:** http://localhost:5000
- **Network:** http://YOUR_IP:5000

---

## ✅ Verify Everything is Ready

```bash
python verify_deployment.py
```

This checks:
- ✅ All required files exist
- ✅ Python packages installed
- ✅ Model files present
- ✅ Templates and static files ready

---

## 🐳 Quick Docker Start

```bash
# Build and run with one command
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🚀 Deploy to Cloud (5 Minutes)

### Option 1: Render.com (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Click "Create Web Service"
   - ✅ Done! (Wait 5-10 minutes for build)

### Option 2: Railway.app

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

### Option 3: Heroku

1. **Install Heroku CLI and login:**
   ```bash
   heroku login
   ```

2. **Deploy:**
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku ps:scale web=1
   heroku open
   ```

---

## 🔧 Common Issues & Quick Fixes

### Camera Not Working
- ✅ Allow camera permissions in browser
- ✅ Use HTTPS in production
- ✅ Close other apps using camera

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Check if App is Running

```bash
# Health check
curl http://localhost:5000/health

# Expected response:
# {"status":"healthy","model_loaded":true,"cascade_loaded":true}
```

---

## 🎯 Next Steps

1. ✅ Test locally: http://localhost:5000
2. ✅ Run verification: `python verify_deployment.py`
3. ✅ Review DEPLOYMENT.md for detailed deployment guide
4. ✅ Deploy to your preferred platform
5. ✅ Share your live app!

---

## 📞 Need Help?

- 📖 Read [README.md](README.md) for detailed documentation
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guides
- 🐛 Review app logs for error messages
- 🔍 Run verification script for diagnostics

---

## 🎉 You're All Set!

Your emotion detection app is ready to go!

**Made with ❤️ using Flask, TensorFlow, and OpenCV**
