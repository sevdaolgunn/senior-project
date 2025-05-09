from flask import Flask, request, jsonify
import os
import tempfile
from flask_cors import CORS
from models import db
from auth import auth_bp
import joblib

import whisper
from symptom_extractor import load_symptoms_from_csv, extract_symptoms
from predictor import predict_disease_from_symptoms

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'

# Whisper modeli tekrar indirilmesin diye cache ayarla
os.environ["WHISPER_CACHE_DIR"] = "C:/Users/MONSTER/.cache/whisper"

# Uygulama başlatılırken modeli ve semptom listesini yükle
db.init_app(app)
CORS(app)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()
    whisper_model = whisper.load_model("large", download_root=os.environ["WHISPER_CACHE_DIR"])
    symptom_list = load_symptoms_from_csv()
    MODEL_PATH = "models/son_model.joblib"
    model = joblib.load(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict_from_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'Ses dosyası eksik.'}), 400

    audio_file = request.files['audio']

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio_path = tmp.name
        audio_file.save(audio_path)

    try:
        result = whisper_model.transcribe(audio_path)
        transcribed_text = result['text']
        print(f"Whisper çıktı: {transcribed_text}")

        matched_symptoms = extract_symptoms(transcribed_text, symptom_list)
        print(f"Eşleşen semptomlar: {matched_symptoms}")

        if not matched_symptoms:
            return jsonify({
                'message': 'Semptom bulunamadı.',
                'transcript': transcribed_text
            }), 200
        all_symptoms = load_symptoms_from_csv()  # Bu da globalde veya route dışında bir yerde tanımlanmalı

        # predict_disease artık tuple döndürüyor
        prediction, confidence, used_symptoms = predict_disease_from_symptoms(model, matched_symptoms,
                                                                                   all_symptoms)

        return jsonify({
            'transcript': transcribed_text,

            'predicted_disease': prediction,

        })

    finally:
        os.remove(audio_path)

if __name__ == '__main__':
    app.run(debug=True)
