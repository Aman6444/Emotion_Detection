# 🚀 Vercel Deployment Guide - Face Emotion Detection

Complete guide to deploy your Flask-based Face Emotion Detection application on Vercel.

---

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Configuration](#project-configuration)
3. [Deployment Steps](#deployment-steps)
4. [Environment Variables](#environment-variables)
5. [Important Limitations](#important-limitations)
6. [Troubleshooting](#troubleshooting)
7. [Alternative Solutions](#alternative-solutions)

---

## ⚠️ IMPORTANT NOTICE

**Vercel has significant limitations for this type of application:**

### Critical Limitations:
1. **Webcam Access:** Vercel serverless functions cannot access webcam directly
2. **Function Timeout:** 10 seconds for Hobby plan, 60 seconds for Pro
3. **Cold Starts:** First request may be slow due to model loading
4. **Memory Limits:** 1024 MB for Hobby, 3008 MB for Pro
5. **File Size:** Large model files (48.50 MB) may cause deployment issues
6. **Streaming:** Video streaming may not work reliably in serverless environment

### Recommended Alternatives:
- **Render.com** (Best for this project - supports long-running processes)
- **Railway.app** (Good for ML applications)
- **Heroku** (Classic choice for Flask apps)
- **DigitalOcean App Platform** (Good performance)
- **AWS EC2 / GCP Compute** (Full control)

---

## 🔧 Prerequisites

Before deploying to Vercel:

1. **Vercel Account**
   - Sign up at https://vercel.com
   - Install Vercel CLI (optional)

2. **GitHub Account**
   - Push your code to GitHub
   - Vercel will deploy from GitHub

3. **Project Requirements**
   - Python 3.9+ (Vercel supports 3.9, 3.10, 3.11)
   - All files in repository
   - Model files included

---

## 📁 Project Configuration

### Files Created for Vercel:

#### 1. vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

#### 2. requirements.txt (Optimized for Vercel)
```
Flask==3.0.0
Werkzeug==3.0.1
tensorflow-cpu==2.16.1
opencv-python-headless==4.9.0.80
numpy==1.26.3
python-dotenv==1.0.0
gunicorn==21.2.0
```

**Key Changes:**
- Using `tensorflow-cpu` (smaller, faster for serverless)
- Using `opencv-python-headless` (no GUI dependencies)
- Pinned versions for reproducibility
- Removed unnecessary packages

#### 3. .vercelignore
Excludes unnecessary files from deployment:
- Training images
- Test files
- Virtual environments
- Cache files

---

## 🚀 Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended)

#### Step 1: Push to GitHub
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Create GitHub repository and push
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

#### Step 2: Import to Vercel
1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Vercel will auto-detect it's a Python project

#### Step 3: Configure Project
- **Framework Preset:** Other
- **Root Directory:** ./
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)
- **Install Command:** `pip install -r requirements.txt`

#### Step 4: Add Environment Variables
Click **"Environment Variables"** and add:
```
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key-here
```

Generate secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Step 5: Deploy
1. Click **"Deploy"**
2. Wait 5-10 minutes for build
3. Get your deployment URL: `https://your-project.vercel.app`

---

### Method 2: Deploy via Vercel CLI

#### Step 1: Install Vercel CLI
```bash
npm i -g vercel
```

#### Step 2: Login
```bash
vercel login
```

#### Step 3: Deploy
```bash
# Navigate to project directory
cd path/to/your/project

# Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? (enter name)
# - Directory? ./
# - Override settings? No
```

#### Step 4: Production Deployment
```bash
vercel --prod
```

---

## 🔐 Environment Variables

### Required Variables:
```bash
FLASK_ENV=production
SECRET_KEY=your-secure-random-secret-key
```

### Optional Variables:
```bash
TF_ENABLE_ONEDNN_OPTS=0
TF_CPP_MIN_LOG_LEVEL=2
PORT=5000
```

### Setting via CLI:
```bash
vercel env add SECRET_KEY
# Enter value when prompted

vercel env add FLASK_ENV
# Enter: production
```

### Setting via Dashboard:
1. Go to Project Settings
2. Navigate to "Environment Variables"
3. Add each variable
4. Redeploy for changes to take effect

---

## ⚠️ Important Limitations

### 1. Webcam Access Issue
**Problem:** Vercel serverless functions cannot access user's webcam directly.

**Solutions:**
- **Option A:** Use client-side JavaScript to capture frames and send to backend
- **Option B:** Deploy to a platform with persistent servers (Render, Railway)
- **Option C:** Modify app to accept image uploads instead of live video

### 2. Function Timeout
**Problem:** Vercel has execution time limits:
- Hobby: 10 seconds
- Pro: 60 seconds

**Solutions:**
- Optimize model inference time
- Use smaller model
- Upgrade to Pro plan
- Use alternative platform

### 3. Cold Starts
**Problem:** First request loads the 48.50 MB model, causing delays.

**Solutions:**
- Accept slower first load
- Keep function warm with periodic pings
- Use model caching strategies
- Consider alternative platforms

### 4. Model File Size
**Problem:** Large model files may cause deployment issues.

**Solutions:**
- Ensure model files are in repository
- Check Vercel's file size limits
- Consider model compression
- Use external storage (S3) for model

### 5. Video Streaming
**Problem:** `/video_feed` endpoint may not work reliably.

**Solutions:**
- Modify to single-frame processing
- Use WebSocket for real-time updates
- Deploy to platform supporting streaming

---

## 🐛 Troubleshooting

### Issue 1: Build Fails - TensorFlow Installation
**Error:** `ERROR: Could not find a version that satisfies the requirement tensorflow`

**Solution:**
```bash
# Use tensorflow-cpu instead
# Already updated in requirements.txt
tensorflow-cpu==2.16.1
```

### Issue 2: Model Files Not Found
**Error:** `FileNotFoundError: emotiondetector.h5`

**Solution:**
1. Ensure model files are committed to git:
   ```bash
   git add emotiondetector.h5 emotiondetector.json
   git commit -m "Add model files"
   git push
   ```

2. Check `.gitignore` doesn't exclude them

3. Verify files are in root directory

### Issue 3: Function Timeout
**Error:** `FUNCTION_INVOCATION_TIMEOUT`

**Solution:**
1. Upgrade to Vercel Pro (60s timeout)
2. Optimize model loading
3. Use alternative platform

### Issue 4: Memory Limit Exceeded
**Error:** `FUNCTION_INVOCATION_FAILED` (memory)

**Solution:**
1. Use `tensorflow-cpu` (lighter)
2. Optimize model size
3. Upgrade to Pro plan (3GB memory)
4. Use alternative platform

### Issue 5: Webcam Not Working
**Error:** Video feed not displaying

**Solution:**
This is expected on Vercel. Options:
1. Modify app for image upload instead
2. Use client-side processing
3. Deploy to Render/Railway instead

### Issue 6: Static Files Not Loading
**Error:** 404 on CSS/JS files

**Solution:**
1. Ensure `static/` folder is in repository
2. Check `vercel.json` routes configuration
3. Verify file paths in templates

---

## 🔄 Alternative Deployment Approach

### Modified App for Vercel (Image Upload Instead of Webcam)

If you want to make it work on Vercel, modify the app to accept image uploads:

#### Create `api/detect.py`:
```python
from flask import Flask, request, jsonify
import cv2
import numpy as np
from keras.models import model_from_json
import base64

app = Flask(__name__)

# Load model (cached)
with open("emotiondetector.json", "r") as f:
    model = model_from_json(f.read())
model.load_weights("emotiondetector.h5")

haar_file = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haar_file)

labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 
          4: 'neutral', 5: 'sad', 6: 'surprise'}

@app.route('/api/detect', methods=['POST'])
def detect_emotion():
    try:
        # Get image from request
        data = request.json
        image_data = base64.b64decode(data['image'])
        
        # Convert to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect faces and emotions
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        results = []
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (48, 48))
            face = face.reshape(1, 48, 48, 1) / 255.0
            
            prediction = model.predict(face, verbose=0)
            emotion = labels[prediction.argmax()]
            
            results.append({
                'emotion': emotion,
                'confidence': float(prediction.max()),
                'bbox': [int(x), int(y), int(w), int(h)]
            })
        
        return jsonify({'success': True, 'faces': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
```

---

## 🎯 Recommended Deployment Platform

### For This Project, We Recommend:

#### 1. **Render.com** (Best Choice) ⭐
**Pros:**
- ✅ Supports long-running processes
- ✅ Webcam streaming works
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy deployment

**Deploy Command:**
```bash
# See DEPLOYMENT.md for full guide
```

#### 2. **Railway.app** (Good Alternative)
**Pros:**
- ✅ Fast deployment
- ✅ Good for ML apps
- ✅ Generous free tier
- ✅ Simple setup

#### 3. **Heroku** (Classic Choice)
**Pros:**
- ✅ Well-documented
- ✅ Large community
- ✅ Reliable
- ⚠️ No free tier anymore

---

## 📊 Vercel vs Alternatives Comparison

| Feature | Vercel | Render | Railway | Heroku |
|---------|--------|--------|---------|--------|
| Webcam Support | ❌ | ✅ | ✅ | ✅ |
| Video Streaming | ⚠️ | ✅ | ✅ | ✅ |
| Free Tier | ✅ | ✅ | ✅ | ❌ |
| Timeout | 10-60s | None | None | 30s |
| ML Support | ⚠️ | ✅ | ✅ | ✅ |
| Setup Difficulty | Easy | Easy | Easy | Medium |
| **Recommended** | ❌ | ✅ | ✅ | ⚠️ |

---

## ✅ Deployment Checklist

Before deploying to Vercel:

- [ ] Code pushed to GitHub
- [ ] `vercel.json` configured
- [ ] `requirements.txt` optimized
- [ ] `.vercelignore` created
- [ ] Model files in repository
- [ ] Environment variables prepared
- [ ] SECRET_KEY generated
- [ ] Understand limitations
- [ ] Consider alternatives
- [ ] Test locally first

---

## 🔗 Useful Links

- **Vercel Documentation:** https://vercel.com/docs
- **Vercel Python Runtime:** https://vercel.com/docs/runtimes#official-runtimes/python
- **Vercel CLI:** https://vercel.com/docs/cli
- **Vercel Limits:** https://vercel.com/docs/concepts/limits/overview

---

## 📞 Support

### If Deployment Fails:

1. **Check Vercel Logs:**
   - Dashboard → Project → Deployments → Click deployment → View logs

2. **Common Issues:**
   - Model files too large → Use external storage
   - Timeout errors → Use alternative platform
   - Memory errors → Upgrade plan or use alternative

3. **Get Help:**
   - Vercel Discord: https://vercel.com/discord
   - GitHub Issues
   - Stack Overflow

---

## 🎉 Success Criteria

Your deployment is successful if:

- ✅ Build completes without errors
- ✅ Landing page loads
- ✅ Health endpoint returns 200
- ⚠️ Video streaming may not work (Vercel limitation)

**Test URLs:**
- Landing: `https://your-project.vercel.app/`
- Health: `https://your-project.vercel.app/health`

---

## 💡 Final Recommendation

**For this specific project (Face Emotion Detection with webcam), we strongly recommend using Render.com or Railway.app instead of Vercel.**

Vercel is excellent for:
- Static sites
- API endpoints
- Serverless functions
- Short-running tasks

But NOT ideal for:
- ❌ Webcam streaming
- ❌ Long-running processes
- ❌ Large ML models with real-time inference
- ❌ Video processing

**See DEPLOYMENT.md for Render/Railway deployment instructions.**

---

**Generated:** 2026-04-22  
**Status:** ⚠️ Vercel has limitations for this project  
**Recommendation:** Use Render.com or Railway.app instead  

---

## 🚀 Quick Deploy to Better Alternatives

### Render.com (Recommended):
```bash
# See DEPLOYMENT.md section 2
# 1. Push to GitHub
# 2. Connect to Render
# 3. Deploy (5 minutes)
```

### Railway.app:
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

Both support webcam streaming and work perfectly with this application! 🎉
