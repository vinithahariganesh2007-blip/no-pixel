import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something in Tamil...")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="ta-IN")
    print("Recognized Tamil text:")
    print(text)
except Exception as e:
    print("Error:", e)
