from google.cloud import texttospeech
import pygame
import io

def init_speaker():
    global client, voice, audio_config

    pygame.mixer.init()

    client = texttospeech.TextToSpeechClient()

    voice = texttospeech.VoiceSelectionParams(language_code='en-US', name='en-US-Chirp3-HD-Puck')

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

def speak(text):
    input_text = texttospeech.SynthesisInput(text=text)

    response = client.synthesize_speech(request={'input': input_text, 'voice': voice, 'audio_config': audio_config})

    try:
        audio_stream = io.BytesIO(response.audio_content)
        pygame.mixer.music.load(audio_stream)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
    except pygame.error as e:
        print(f"Error playing audio: {e}")