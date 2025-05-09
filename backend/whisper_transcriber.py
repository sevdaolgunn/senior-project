import whisper

# Whisper modeli yükleniyor
model = whisper.load_model("large")  # dilersen "small", "medium", "large" da seçebilirsin

def transcribe_audio(audio_path):
    """
    Verilen ses dosyasını metne dönüştürür.
    :param audio_path: .wav, .mp3 vs. gibi ses dosyasının yolu
    :return: metne dönüştürülmüş string çıktı
    """
    result = model.transcribe(audio_path)  # Türkçe için "tr"
    return result["text"]
