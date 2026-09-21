# sarvam_tts.py

from sarvamai import SarvamAI
from sarvamai.play import save
import tempfile
from playsound import playsound
import os

# Load your API key from the environment
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

if not SARVAM_API_KEY:
    raise RuntimeError("Please set SARVAM_API_KEY environment variable!")

# Create Sarvam client
sarvam = SarvamAI(api_subscription_key=SARVAM_API_KEY)

def speak_tamil(text):
    """Convert text to Tamil speech using Sarvam AI TTS."""
    try:
        # Convert text → Tamil voice
        audio = sarvam.text_to_speech.convert(
            target_language_code="ta-IN",   # Tamil language
            text=text,
            model="bulbul:v2",
            speaker="anushka"
        )

        # Save audio to temporary file
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_wav.close()
        save(audio, temp_wav.name)

        # Play the audio
        sound = sa.WaveObject.from_wave_file(temp_wav.name)
        play_obj = sound.play()
        play_obj.wait_done()

        # Delete file after playing
        os.remove(temp_wav.name)

    except Exception as e:
        print("Tamil TTS Error:", e)
