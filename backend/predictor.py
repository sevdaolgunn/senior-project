import joblib
import pandas as pd
import numpy as np

MODEL_PATH = "models/son_model.joblib"
model = joblib.load(MODEL_PATH)

df1 = pd.read_csv("data/Symptom-severity.csv")
df1['Symptom'] = df1['Symptom'].str.strip().str.lower()

discrp = pd.read_csv("data/symptom_Description.csv")
ektra7at = pd.read_csv("data/symptom_precaution.csv")

model_features = df1['Symptom'].unique().tolist()
print(f"Model features loaded: {len(model_features)} features: {model_features}")


def predict_disease_from_symptoms(model, symptoms, all_symptoms):
    """
    Semptom listesi alır ve hastalık tahmini yapar

    :param model: Eğitilmiş makine öğrenimi modeli
    :param symptoms: Kullanıcıdan gelen semptom listesi
    :param all_symptoms: Modelin eğitildiği tüm semptomlar listesi
    :return: (tahmin edilen hastalık, tahmin güven skoru %, eşleşen semptomlar)
    """
    # Semptomları temizle ve standartlaştır
    cleaned_symptoms = []
    for symptom in symptoms:
        if isinstance(symptom, str) and symptom.strip():
            cleaned_symptoms.append(symptom.lower().strip())

    if not cleaned_symptoms:
        return "Geçerli semptom girilmedi.", 0.0, []

    # Tüm semptomlar için one-hot encoding
    input_vector = np.zeros(len(symptoms))
    matched_symptoms = []

    for symptom in cleaned_symptoms:
        # Tam eşleşme ara
        if symptom in all_symptoms:
            idx = all_symptoms.index(symptom)
            input_vector[idx] = 1
            matched_symptoms.append(symptom)
        else:
            # En yakın eşleşmeyi ara
            potential_matches = [s for s in all_symptoms if symptom in s]
            if potential_matches:
                idx = all_symptoms.index(potential_matches[0])
                input_vector[idx] = 1
                matched_symptoms.append(potential_matches[0])
                print(f"'{symptom}' semptomu '{potential_matches[0]}' olarak eşleştirildi.")
            else:
                print(f"Uyarı: '{symptom}' semptomu veritabanında bulunamadı.")

    if not matched_symptoms:
        return "Geçerli semptom bulunamadı.", 0.0, []

    # Tahmin yap
    prediction = model.predict([input_vector])[0]

    # Tahmin güvenini hesapla
    confidence = np.max(model.predict_proba([input_vector])[0]) * 100

    return prediction, confidence, matched_symptoms



