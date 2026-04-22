# 🚀 Deployment Guide - Face Emotion Detection

Complete guide to deploy your Face Emotion Detection application to various platforms.

---

## 📋 Table of Contents
1. [Heroku Deployment](#heroku-deployment)
2. [Render Deployment](#render-deployment)
3. [Railway Deployment](#railway-deployment)
4. [DigitalOcean/AWS/GCP Deployment](#vps-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Environment Variables](#environment-variables)

---

## 🔧 Prerequisites

- Git installed
- Python 3.10+
- Account on your chosen deployment platform
- All project files including model files (`emotiondetector.h5`, `emotiondetector.json`)

---

## 1️⃣ Heroku Deployment

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Create Heroku App
```bash
heroku create your-emotion-detector-app
```

### Step 4: Add Buildpacks
```bash
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
```

### Step 5: Create Aptfile (for OpenCV dependencies)
Create a file named `Aptfile` in root directory:
```
libsm6
libxext6
libxrender-dev
libgomp1
libglib2.0-0
```

### Step 6: Deploy
```bash
git init
git add .
git commit -m "Initial deployment"
heroku git:remote -a your-emotion-detector-app
git push heroku main
```

### Step 7: Scale Web Dyno
```bash
heroku ps:scale web=1
```

### Step 8: Open App
```bash
heroku open
```

**⚠️ Note:** Webcam access may be limited on Heroku due to browser security restrictions with HTTP.

---

## 2️⃣ Render Deployment (Recommended)

### Step 1: Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up with GitHub

### Step 3: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** your-emotion-detector
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Instance Type:** Free (or paid for better performance)

### Step 4: Add Environment Variables
```
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
```

### Step 5: Deploy
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)

### Step 6: Enable HTTPS
- Render provides free SSL automatically
- Your app will be available at: `https://your-emotion-detector.onrender.com`

---

## 3️⃣ Railway Deployment

### Step 1: Install Railway CLI
```bash
npm i -g @railway/cli
```

### Step 2: Login
```bash
railway login
```

### Step 3: Initialize Project
```bash
railway init
```

### Step 4: Deploy
```bash
railway up
```

### Step 5: Set Variables
```bash
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-secret-key
```

### Step 6: Get URL
```bash
railway open
```

---

## 4️⃣ VPS Deployment (DigitalOcean/AWS/GCP)

### Step 1: SSH into Server
```bash
ssh root@your-server-ip
```

### Step 2: Install Dependencies
```bash
apt update
apt install python3-pip python3-dev nginx git -y
apt install libsm6 libxext6 libxrender-dev libgomp1 libglib2.0-0 -y
```

### Step 3: Clone Repository
```bash
cd /var/www
git clone YOUR_REPO_URL
cd your-emotion-detector
```

### Step 4: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Install Gunicorn
```bash
pip install gunicorn
```

### Step 6: Create Systemd Service
```bash
nano /etc/systemd/system/emotion-detector.service
```

Add:
```ini
[Unit]
Description=Emotion Detection Web App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/your-emotion-detector
Environment="PATH=/var/www/your-emotion-detector/venv/bin"
ExecStart=/var/www/your-emotion-detector/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8000 wsgi:app

[Install]
WantedBy=multi-user.target
```

### Step 7: Configure Nginx
```bash
nano /etc/nginx/sites-available/emotion-detector
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Step 8: Enable and Start Services
```bash
ln -s /etc/nginx/sites-available/emotion-detector /etc/nginx/sites-enabled
systemctl start emotion-detector
systemctl enable emotion-detector
systemctl restart nginx
```

### Step 9: Setup SSL (Optional but Recommended)
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## 5️⃣ Docker Deployment

### Dockerfile
Already created in your project root.

### Build and Run
```bash
docker build -t emotion-detector .
docker run -p 5000:5000 emotion-detector
```

### Docker Compose (Optional)
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
```

Run:
```bash
docker-compose up -d
```

---

## 🔐 Environment Variables

Create a `.env` file for local development:
```bash
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
PORT=5000
```

For production, set:
```bash
FLASK_ENV=production
SECRET_KEY=generate-a-secure-random-key
PORT=5000
```

---

## 📊 Performance Optimization

### 1. Use Production WSGI Server
- Gunicorn (included in requirements.txt)
- uWSGI
- Waitress

### 2. Optimize Workers
```bash
gunicorn --workers 2 --threads 4 --timeout 120 wsgi:app
```

### 3. Enable Caching
Add caching headers in app.py for static files.

### 4. Use CDN
Serve static files (CSS, JS) from a CDN.

---

## 🐛 Troubleshooting

### Issue: Camera Not Working
- Ensure HTTPS is enabled (required for webcam access)
- Check browser permissions

### Issue: Model Loading Error
- Verify `emotiondetector.h5` and `emotiondetector.json` are in root directory
- Check file permissions

### Issue: High Memory Usage
- Reduce number of workers
- Use smaller model if possible
- Enable swap memory on VPS

### Issue: Slow Response
- Use paid tier with more resources
- Optimize model inference
- Add caching

---

## 📱 Testing Deployment

### Health Check
```bash
curl https://your-app-url.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "cascade_loaded": true
}
```

---

## 🔒 Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Enable HTTPS/SSL
- [ ] Set FLASK_ENV=production
- [ ] Disable debug mode
- [ ] Add rate limiting
- [ ] Implement CORS if needed
- [ ] Use environment variables for sensitive data
- [ ] Regular security updates

---

## 📝 Post-Deployment

1. **Monitor Logs:**
   - Heroku: `heroku logs --tail`
   - Render: Check dashboard logs
   - VPS: `journalctl -u emotion-detector -f`

2. **Set Up Monitoring:**
   - Use services like New Relic, Datadog, or Sentry
   - Monitor uptime with UptimeRobot or Pingdom

3. **Backup Data:**
   - Keep backups of model files
   - Version control everything

---

## 🎯 Recommended Platform

**For Beginners:** Render.com (Free tier, easy setup, HTTPS included)
**For Production:** AWS/GCP/DigitalOcean (More control, better performance)
**For Quick Testing:** Railway.app (Fast deployment, generous free tier)

---

## 📞 Support

If you encounter issues:
1. Check logs for error messages
2. Verify all files are uploaded correctly
3. Ensure model files are accessible
4. Check platform-specific documentation

---

## ✅ Success!

Your app should now be live and accessible! 🎉

Test it at your deployment URL and enjoy real-time emotion detection!
