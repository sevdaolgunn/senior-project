import re
import csv

def load_symptoms_from_csv(path='data/Symptom-severity.csv'):
    symptoms = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symptom = row['Symptom'].strip().lower()
            if symptom:
                symptoms.append(symptom)
    return symptoms

def extract_symptoms(text, symptoms):
    """
    Metinden CSV'den alınan semptomlara göre eşleşenleri çıkartır.
    :param text: Transkript edilmiş metin
    :param symptoms: CSV'den yüklenen semptom listesi
    :return: Tanınan semptomlar listesi
    """
    text = text.lower()
    found_symptoms = [symptom for symptom in symptoms if re.search(rf"\b{re.escape(symptom)}\b", text)]
    return found_symptoms
