import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import time
import numpy as np
import os
import google.generativeai as genai

# -------------------------------
#  GEMINI API KEY
# -------------------------------
GEMINI_API_KEY = "AIzaSyBpzOvjuR_calaqtTkYaEjau4OKUkc9vIc"  # Your key

genai.configure(api_key=GEMINI_API_KEY)

# --------------
        print("🎤 Speak now…")
        fs = 16000        # 16 kHz works best for speech
        duration = 6      # Enough time to speak clearly

        audio = sd.rec(int(duration * fs),
                       samplerate=fs,
                       channels=1,
                       dtype='float32')
        sd.wait()

        audio_int16 = (audio * 32767).astype(np.int16)
        filename = "input.wav"
        write(filename, fs, audio_int16)

        return filename

    except Exception as e:
        print("❌ Recording error:", e)
        return None

# -------------------------------
#  SPEECH → TEXT (Tamil)
# -------------------------------
def speech_to_text(filename):
    if not filename or not os.path.exists(filename):
        return ""

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(filename) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language="ta-IN")

        print("📝 You:", text)
        return text

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return ""

    except Exception as e:
        print("❌ Speech error:", e)
        return ""

# -------------------------------
#  ASK GEMINI
# -------------------------------
def ask_gemini(prompt):
    if not prompt.strip():
        return "ஏதோ தவறு நடந்துள்ளது, மீண்டும் முயற்சிக்கவும்."

    try:
        # Correct working model name
        model = genai.GenerativeModel("models/gemini-pro-latest")

        full_prompt = f"""
        நீங்கள் ஒரு உதவியாளர். எப்போதும் தமிழில் பதிலளிக்கவும்.
        பதில் சுருக்கமாகவும் தெளிவாகவும் இருக்க வேண்டும்.

        பயனரின் கேள்வி: {prompt}

        தமிழில் பதிலளிக்கவும்:
        """

        response = model.generate_content(full_prompt)

        if response and response.text:
            reply = response.text.strip()
            print("🤖 Gemini:", reply)
            return reply

        return "மன்னிக்கவும், பதில் பெற முடியவில்லை."

    except Exception as e:
        print("❌ Gemini API Error:", e)
        return "மன்னிக்கவும், பிழை ஏற்பட்டுள்ளது."

# -------------------------------
#  TEXT → VOICE (Tamil)
# -------------------------------
def speak_tamil(text):
    if not text.strip():
        return

    try:
        clean_text = text.replace("*", "").replace("_", "").strip()

        tts = gTTS(text=clean_text, lang="ta", slow=False)

        filename = f"reply_{int(time.time())}.mp3"
        tts.save(filename)

        playsound(filename)

        # Delete after playing
        try:
            os.remove(filename)
        except:
            pass

    except Exception as e:
        print("❌ TTS Error:", e)

# -------------------------------
#  CLEAN OLD FILES
# -------------------------------
def cleanup_old_files():
    try:
        for file in os.listdir("."):
            if file.startswith("reply_") and file.endswith(".mp3"):
                os.remove(file)
        if os.path.exists("input.wav"):
            os.remove("input.wav")
    except:
        pass

# -------------------------------
#  MAIN PROGRAM
# -------------------------------
print("✨ Tamil Voice Assistant with Gemini Ready ✨")
print("Press Ctrl+C to exit\n")

cleanup_old_files()

try:
    while True:
        audio_file = record_audio()

        if audio_file:
            text = speech_to_text(audio_file)

            if text:
                reply = ask_gemini(text)
                speak_tamil(reply)
            else:
                speak_tamil("மன்னிக்கவும், உங்கள் குரலை புரிந்து கொள்ள முடியவில்லை. மீண்டும் முயற்சிக்கவும்.")

        print("\n" + "="*50 + "\n")

except KeyboardInterrupt:
    print("\n👋 நன்றி, பயன்படுத்தியதற்கு!")
    cleanup_old_files()
    -----------------
#  RECORD AUDIO
# -------------------------------
def record_audio():
    try: