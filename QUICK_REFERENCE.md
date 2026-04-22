# 🚀 Quick Reference Card - Face Emotion Detection

## ⚡ One-Line Setup

```bash
pip install -r requirements.txt && python app.py
```

Then open: **http://localhost:5000**

---

## 📋 Essential Commands

### Setup & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run setup verification
python setup.py

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Running the App
```bash
# Development mode
python app.py

# Production mode
gunicorn wsgi:app --bind 0.0.0.0:5000

# With Docker
docker-compose up -d

# Windows startup
start.bat

# Linux/Mac startup
./start.sh
```

### Testing
```bash
# Health check
curl http://localhost:5000/health

# Run tests
python test_app.py

# Verify deployment
python verify_deployment.py
```

---

## 🌐 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/detect` | GET | Detection page |
| `/video_feed` | GET | Video stream (MJPEG) |
| `/health` | GET | Health check |

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `wsgi.py` | Production WSGI entry |
| `config.py` | Configuration management |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables |
| `emotiondetector.h5` | Model weights (48.50 MB) |
| `emotiondetector.json` | Model architecture |

---

## 🔧 Configuration (.env)

```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=5000
TF_ENABLE_ONEDNN_OPTS=0
TF_CPP_MIN_LOG_LEVEL=2
```

Generate secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🐳 Docker Commands

```bash
# Build image
docker build -t emotion-detector .

# Run container
docker run -p 5000:5000 emotion-detector

# Docker Compose
docker-compose up -d        # Start
docker-compose logs -f      # View logs
docker-compose down         # Stop
```

---

## 🚀 Quick Deploy

### Render.com
1. Push to GitHub
2. Connect repo on Render
3. Deploy (auto-detects settings)

### Railway
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

### Heroku
```bash
heroku create app-name
git push heroku main
heroku ps:scale web=1
```

---

## 🐛 Quick Fixes

### Port in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Dependencies issue
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Camera not working
- Allow browser permissions
- Close other apps using camera
- Use HTTPS in production
- Try Chrome/Firefox

### Model not loading
- Verify files exist: `emotiondetector.h5`, `emotiondetector.json`
- Check file size: ~48 MB
- Review logs for errors

---

## 📊 System Requirements

- **Python:** 3.10+ (3.12.6 tested)
- **RAM:** 2GB+ recommended
- **Disk:** 500MB+ free space
- **Webcam:** Required for live detection
- **Browser:** Chrome/Firefox (latest)

---

## 🎯 Detected Emotions

1. 😠 Angry
2. 🤢 Disgust
3. 😨 Fear
4. 😊 Happy
5. 😐 Neutral
6. 😢 Sad
7. 😲 Surprise

---

## 📚 Documentation

| File | Description |
|------|-------------|
| `PROJECT_ANALYSIS.md` | Complete project analysis |
| `SETUP_COMPLETE.md` | Setup summary |
| `README.md` | Main documentation |
| `QUICKSTART.md` | Quick start guide |
| `DEPLOYMENT.md` | Deployment guide |
| `QUICK_REFERENCE.md` | This file |

---

## 🔐 Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS/SSL
- [ ] Update .env with secure values
- [ ] Disable debug mode
- [ ] Review security settings

---

## 📞 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | `pip install -r requirements.txt` |
| Port in use | Change PORT in .env |
| Camera blocked | Check browser permissions |
| Model error | Verify .h5 and .json files |
| Slow performance | Reduce workers, optimize |

---

## ⚡ Performance Tips

### Development
- Single worker
- Debug mode enabled
- Local testing

### Production
- Multiple workers (2-4)
- HTTPS enabled
- Caching configured
- CDN for static files

```bash
# Optimized production command
gunicorn wsgi:app \
  --bind 0.0.0.0:5000 \
  --workers 2 \
  --threads 4 \
  --timeout 120
```

---

## 🎉 Quick Start Checklist

- [ ] Clone/download project
- [ ] Install Python 3.10+
- [ ] Run `pip install -r requirements.txt`
- [ ] Create `.env` from `.env.example`
- [ ] Run `python app.py`
- [ ] Open http://localhost:5000
- [ ] Allow camera permissions
- [ ] Test emotion detection
- [ ] Deploy to cloud (optional)

---

## 📈 Project Stats

- **Files:** 50+
- **Documentation:** 8 guides
- **Model Size:** 48.50 MB
- **Test Images:** 5,090+
- **Emotions:** 7 classes
- **Deployment Options:** 5+
- **Python Version:** 3.12.6
- **Status:** ✅ Production-Ready

---

## 🌟 Quick Links

- **Local App:** http://localhost:5000
- **Health Check:** http://localhost:5000/health
- **GitHub:** (your-repo-url)
- **Docs:** README.md

---

**Last Updated:** 2026-04-22  
**Version:** 1.0.0  
**Status:** ✅ Ready to Deploy

---

## 💡 Pro Tips

1. **Use virtual environment** for clean dependency management
2. **Test locally first** before deploying
3. **Enable HTTPS** for webcam access in production
4. **Monitor logs** for debugging
5. **Use health endpoint** for uptime monitoring
6. **Keep SECRET_KEY secure** and unique
7. **Update dependencies** regularly
8. **Backup model files** before changes

---

**🚀 Ready to go! Install dependencies and run the app!**

```bash
pip install -r requirements.txt && python app.py
```
