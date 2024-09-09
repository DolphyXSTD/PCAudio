import speech_recognition as spr
import vosk

sr = spr.Recognizer()
sr.pause_threshold = 0.5

with spr.Microphone() as mic:
    sr.adjust_for_ambient_noise(source=mic, duration=0.5)
    audio = sr.listen(mic)
    query = sr.recognize_vosk(audio_data=audio, language="ru-RU").lower()

    print(query)