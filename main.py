import speech_recognition as spr

sr = spr.Recognizer()
sr.pause_threshold = 0.5

def listen_command():
    with spr.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=0.5)
        audio = sr.listen(mic)
        query = sr.recognize_vosk(audio_data=audio, language="ru-RU").lower()

        print(query)

while True:
    listen_command()