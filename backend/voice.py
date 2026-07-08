import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from pathlib import Path

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

def text_to_speech(text):

    audio = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb",   # George (default voice)
        model_id="eleven_multilingual_v2",
        text=text
    )

    os.makedirs("temp_audio", exist_ok=True)

    output_path = "temp_audio/answer.mp3"

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path
def speech_to_text(audio_path):

    with open(audio_path, "rb") as audio:

        transcription = client.speech_to_text.convert(
            file=audio,
            model_id="scribe_v1"
        )

    return transcription.text
