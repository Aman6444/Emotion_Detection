import os
import random
import base64
import cv2
import numpy as np
from flask import Flask, render_template, Response, request, jsonify
from io import BytesIO
from PIL import Image

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'model.DenseNet121.keras')

# Load trained model
model = tf.keras.models.load_model(MODEL_PATH)

# RAF-DB emotion labels with emoji fallback (used when image assets are missing)
emotion_meta = {
    'surprise': {'label': 'Surprise', 'emoji': '😲'},
    'fear': {'label': 'Fear', 'emoji': '😨'},
    'disgust': {'label': 'Disgust', 'emoji': '🤢'},
    'happy': {'label': 'Happy', 'emoji': '😄'},
    'sad': {'label': 'Sad', 'emoji': '😢'},
    'angry': {'label': 'Angry', 'emoji': '😠'},
    'neutral': {'label': 'Neutral', 'emoji': '😐'}
}
emotion_labels = list(emotion_meta.keys())

def load_emoji_paths():
    emoji_root = os.path.join(BASE_DIR, 'static', 'emojis')
    supported_ext = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    paths = {}

    for emotion in emotion_labels:
        emotion_dir = os.path.join(emoji_root, emotion)
        if not os.path.isdir(emotion_dir):
            paths[emotion] = []
            continue

        files = []
        for filename in os.listdir(emotion_dir):
            _, ext = os.path.splitext(filename)
            if ext.lower() in supported_ext:
                files.append(f'static/emojis/{emotion}/{filename}')
        paths[emotion] = files

    return paths


emoji_paths = load_emoji_paths()

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def is_camera_available(index=0):
    camera = cv2.VideoCapture(index)
    available = camera.isOpened()
    camera.release()
    return available

# Detect and crop face
def detect_and_crop_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        return frame[y:y+h, x:x+w]
    return None  # No face detected


def detect_largest_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return None, None

    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    pad = int(0.12 * max(w, h))
    x1 = max(x - pad, 0)
    y1 = max(y - pad, 0)
    x2 = min(x + w + pad, frame.shape[1])
    y2 = min(y + h + pad, frame.shape[0])
    return frame[y1:y2, x1:x2], (x1, y1, x2 - x1, y2 - y1)

# Preprocess frame
def preprocess_frame(frame):
    resized = cv2.resize(frame, (100, 100))
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    batch = np.expand_dims(rgb, axis=0)

    # Prefer the DenseNet preprocessing function from TF-Keras when available.
    preprocess = getattr(getattr(tf.keras.applications, 'densenet', None), 'preprocess_input', None)
    processed = preprocess(batch) if preprocess else (batch.astype(np.float32) / 255.0)
    return processed


def pick_emoji_path(emotion):
    emoji_list = emoji_paths.get(emotion, [])
    return '/' + random.choice(emoji_list) if emoji_list else ''


def get_emotion_display(emotion):
    return emotion_meta.get(emotion, {}).get('label', emotion.title())


def get_emotion_emoji(emotion):
    return emotion_meta.get(emotion, {}).get('emoji', '🙂')


def infer_emotion_from_frame(frame):
    face_crop, _ = detect_largest_face(frame)
    if face_crop is None:
        return None

    image_np = preprocess_frame(face_crop)
    prediction = model.predict(image_np, verbose=0)[0]
    emotion_index = int(np.argmax(prediction))
    emotion = emotion_labels[emotion_index]
    confidence = float(prediction[emotion_index])

    top3_idx = np.argsort(prediction)[-3:][::-1]
    top3 = [
        {
            'emotion': emotion_labels[int(i)],
            'emotion_display': get_emotion_display(emotion_labels[int(i)]),
            'emoji_char': get_emotion_emoji(emotion_labels[int(i)]),
            'confidence': float(prediction[int(i)])
        }
        for i in top3_idx
    ]

    return {
        'emotion': emotion,
        'emotion_display': get_emotion_display(emotion),
        'emoji_char': get_emotion_emoji(emotion),
        'confidence': confidence,
        'top3': top3
    }

# Stream video with predictions
def generate_frames():
    camera = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            face_crop, bbox = detect_largest_face(frame)

            if face_crop is None:
                cv2.putText(frame, 'No face detected', (10, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (10, 10, 240), 2)
            else:
                image_np = preprocess_frame(face_crop)
                prediction = model.predict(image_np, verbose=0)[0]
                emotion_index = int(np.argmax(prediction))
                emotion = emotion_labels[emotion_index]
                emotion_display = get_emotion_display(emotion)
                confidence = float(prediction[emotion_index])
                emoji_char = get_emotion_emoji(emotion)

                x, y, w, h = bbox
                cv2.rectangle(frame, (x, y), (x + w, y + h), (13, 110, 110), 2)

                label = f'{emoji_char} {emotion_display} {confidence * 100:.1f}%'
                cv2.putText(frame, label, (10, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.85, (13, 110, 110), 2)

            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        camera.release()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture():
    return render_template('capture.html')


@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/video_feed')
def video_feed():
    if not is_camera_available(0):
        return jsonify({'error': 'Webcam is not available in this environment.'}), 503
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'face_cascade_loaded': face_cascade is not None
    }), 200

@app.route('/predict_picture', methods=['POST'])
def predict_picture():
    data = request.get_json(silent=True) or {}
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    if ',' not in data['image']:
        return jsonify({'error': 'Invalid image data format'}), 400

    image_data = data['image'].split(',', 1)[1]
    image_bytes = base64.b64decode(image_data)

    # Decode to OpenCV image (BGR)
    np_img = np.frombuffer(image_bytes, np.uint8)
    img_bgr = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    if img_bgr is None:
        return jsonify({'error': 'Unable to decode image'}), 400

    inferred = infer_emotion_from_frame(img_bgr)
    if inferred is None:
        return jsonify({'error': 'No clear face detected. Please keep one face in frame.'}), 400

    emotion = inferred['emotion']
    emoji_path = pick_emoji_path(emotion)

    return jsonify({
        **inferred,
        'emoji_path': emoji_path
    })

@app.route('/predict_upload', methods=['POST'])
def predict_upload():
    # Check if the request contains a file
    if 'file' not in request.files or request.files['file'].filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file = request.files['file']

    # Read the uploaded image file into memory
    in_memory_file = BytesIO()
    file.save(in_memory_file)
    data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
    img_bgr = cv2.imdecode(data, cv2.IMREAD_COLOR)  # Decode image using OpenCV
    if img_bgr is None:
        return jsonify({'error': 'Unable to decode uploaded file as an image'}), 400

    # Convert BGR (OpenCV default) to RGB (for model and display)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    inferred = infer_emotion_from_frame(img_bgr)
    if inferred is None:
        return render_template('upload.html', error='No clear face detected. Upload an image with one visible face.')

    emotion = inferred['emotion']

    # Get corresponding emoji path list and select one at random
    emoji_path = pick_emoji_path(emotion)

    # Convert image to base64 to render in HTML without saving to disk
    img_pil = Image.fromarray(img_rgb)
    buffer = BytesIO()
    img_pil.save(buffer, format="JPEG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Render result on upload.html page with emotion, emoji, and uploaded image
    return render_template(
        'upload.html',
        emotion=emotion,
        emotion_display=inferred['emotion_display'],
        emoji_char=inferred['emoji_char'],
        confidence=inferred['confidence'],
        top3=inferred['top3'],
        emoji_path=emoji_path,
        uploaded_image=img_base64
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)