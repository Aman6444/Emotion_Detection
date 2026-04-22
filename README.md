# Face Emotion Detection Web App

A production-ready web application for real-time face emotion detection using Flask, TensorFlow, and OpenCV.

## 🌟 Features

- 🎭 Real-time emotion detection from webcam
- 🌐 Web-based interface accessible from any browser
- 🎨 Clean, modern UI with landing page
- 📊 Detects 7 emotions: Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise
- 🚀 Production-ready with proper error handling
- 🐳 Docker support for easy deployment
- 📱 Mobile responsive design

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd face_emotion_detection_model-main
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Access the app**
Open your browser and navigate to: `http://localhost:5000`

## 📦 Deployment

This project is deployment-ready for multiple platforms. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deploy Options:

#### Render.com (Recommended)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Push code to GitHub
2. Connect GitHub repo to Render
3. Deploy with one click

#### Docker
```bash
docker build -t emotion-detector .
docker run -p 5000:5000 emotion-detector
```

#### Docker Compose
```bash
docker-compose up -d
```

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **ML Model**: Keras/TensorFlow CNN
- **Computer Vision**: OpenCV with Haar Cascade face detection
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn WSGI server
- **Containerization**: Docker

## 📁 Project Structure

```
.
├── app.py                    # Main Flask application (production-ready)
├── wsgi.py                   # WSGI entry point
├── config.py                 # Configuration management
├── emotiondetector.json      # Model architecture
├── emotiondetector.h5        # Trained model weights
├── requirements.txt          # Python dependencies (pinned versions)
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── Procfile                 # Heroku deployment
├── runtime.txt              # Python version specification
├── Aptfile                  # System dependencies
├── .gitignore              # Git ignore rules
├── .env.example            # Environment variables template
├── README.md               # This file
├── DEPLOYMENT.md           # Detailed deployment guide
├── templates/
│   ├── landing.html        # Landing page with camera access
│   └── detect.html         # Live detection page
├── static/
│   ├── landing.css         # Landing page styles
│   ├── style.css           # Detection page styles
│   └── script.js           # JavaScript functionality
└── images/
    ├── train/              # Training dataset
    └── test/               # Testing dataset
```

## 🎯 Usage

1. **Landing Page**: Visit the home page and click "Open Camera & Start Detection"
2. **Camera Permission**: Allow camera access when prompted by your browser
3. **Detection**: The app automatically redirects to the live detection page
4. **Real-time Analysis**: Watch as emotions are detected and labeled in real-time
5. **Try Expressions**: Make different facial expressions to see the AI in action

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
FLASK_ENV=production
SECRET_KEY=your-secure-random-secret-key
PORT=5000
```

### Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🔧 Development

### Install Development Dependencies
```bash
pip install -r requirements.txt
```

### Run in Development Mode
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python app.py
```

### Run Tests
```bash
python -m pytest tests/
```

## 🐳 Docker Development

### Build Image
```bash
docker build -t emotion-detector:dev .
```

### Run Container
```bash
docker run -p 5000:5000 -e FLASK_ENV=development emotion-detector:dev
```

## 📊 Model Information

- **Architecture**: Convolutional Neural Network (CNN)
- **Input Size**: 48x48 grayscale images
- **Output**: 7 emotion classes
- **Framework**: Keras with TensorFlow backend
- **Face Detection**: Haar Cascade Classifier

## 🔒 Security Features

- ✅ Secret key management
- ✅ Environment variable configuration
- ✅ Error handling and logging
- ✅ Input validation
- ✅ HTTPS support (in production)
- ✅ Content-type restrictions

## 📝 API Endpoints

- `GET /` - Landing page
- `GET /detect` - Detection page
- `GET /video_feed` - Video stream endpoint
- `GET /health` - Health check endpoint

### Health Check Example
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "cascade_loaded": true
}
```

## 🚨 Troubleshooting

### Camera Not Working
- Ensure your browser has camera permissions enabled
- Check if another application is using the camera
- Try using a different browser (Chrome/Firefox recommended)
- For production, ensure HTTPS is enabled (required for webcam access)

### Model Not Loading
- Verify that `emotiondetector.json` and `emotiondetector.h5` exist in the project directory
- Check if the model files are corrupted
- Review logs for specific error messages

### Port Already in Use
Edit `app.py` and change the port number:
```python
port = int(os.environ.get('PORT', 5001))  # Change to 5001
```

### High Memory Usage
- Reduce number of Gunicorn workers
- Use a machine with more RAM
- Consider model optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes.

## 👥 Authors

- Your Name

## 🙏 Acknowledgments

- TensorFlow and Keras teams
- OpenCV community
- Flask framework
- Dataset contributors

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- Review logs for error messages

## 🎉 Success Checklist

Before deploying to production:

- [ ] Update SECRET_KEY
- [ ] Set FLASK_ENV=production
- [ ] Test all endpoints
- [ ] Verify model files are included
- [ ] Test camera access on HTTPS
- [ ] Review security settings
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Test on target platform
- [ ] Document any platform-specific settings

---

**Made with ❤️ using Flask, TensorFlow, and OpenCV**

## Troubleshooting

### Camera Not Working
- Ensure your browser has camera permissions enabled
- Check if another application is using the camera
- Try using a different browser (Chrome/Firefox recommended)

### Model Not Loading
- Verify that `emotiondetector.json` and `emotiondetector.h5` exist in the project directory
- Check if the model files are corrupted

### Port Already in Use
Edit `app.py` and change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

## Notes

- The app streams video frames processed with emotion detection
- Detection works best with good lighting and clear facial visibility
- Multiple faces can be detected simultaneously

## License

This project is for educational purposes.
