---
title: EmotionSense AI
emoji: 😄
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# EmotionSense AI — Facial Emotion Recognition

A Flask web app that detects human emotions from facial expressions using a **DenseNet121**-based deep learning model trained on the RAF-DB dataset.

## Features

| Mode | Description | Works on HF Spaces |
|------|-------------|-------------------|
| 📸 Quick Capture | Capture from your webcam via browser | ✅ Yes |
| 🎥 Live Stream | Real-time server-side camera stream | ⚠️ Local only |
| 📤 Upload Image | Upload any photo for prediction | ✅ Yes |

Detects 7 emotions: **Angry, Disgust, Fear, Happy, Neutral, Sad, Surprise**

## Model

- Architecture: DenseNet121 (transfer learning)
- Input: 100×100 RGB face crop
- Output: 7-class softmax probabilities
- Face detection: OpenCV Haar Cascade

## Deploying to Hugging Face Spaces

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose **Docker** as the SDK
3. Upload all project files (or push via git)
4. The Space will build automatically using the `Dockerfile`

> The app runs on port **7860** as required by Hugging Face Spaces.

## Running Locally with Docker

```bash
# Build the image
docker build -t emotion-detection .

# Run the container
docker run -p 7860:7860 emotion-detection
```

Then open [http://localhost:7860](http://localhost:7860)

## Running Locally without Docker

```bash
pip install -r requirements.txt
python app.py
```

## Project Structure

```
├── app.py                  # Flask application
├── Dockerfile              # Docker config for HF Spaces
├── requirements.txt        # Python dependencies
├── model/
│   └── model.DenseNet121.keras   # Trained model weights
├── static/
│   ├── style.css
│   └── emojis/             # Emotion emoji assets
└── templates/
    ├── index.html
    ├── capture.html
    ├── upload.html
    └── video.html
```

## Tech Stack

- Python 3.11
- Flask + Gunicorn
- TensorFlow / Keras
- OpenCV
- Pillow
