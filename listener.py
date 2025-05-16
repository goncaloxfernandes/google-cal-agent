import os
from dotenv import load_dotenv
import pvporcupine
import pyaudio
import struct
import speech_recognition as sr

WAKE_WORD = "jarvis"

CHUNK = 512  # Number of data chunks to read at a time
FORMAT = pyaudio.paInt16  # Data format (16-bit integers)
CHANNELS = 1  # Mono audio
RATE = 16000  # Sampling rate (samples per second)
RECORD_SECONDS = 5  # Duration to record in seconds
AUDIO_START_TIMEOUT = 5  # Timeout in seconds for listening to the command
AUDIO_TIME_LIMIT = 10

def init_listener():
    global porcupine, audio, stream, recognizer, mic

    load_dotenv('keys.env')
    PORCUPINE_ACCESS_KEY = os.environ.get('PORCUPINE_ACCESS_KEY')

    porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=[WAKE_WORD])

    audio = pyaudio.PyAudio()

    # Open an audio stream for input
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=3)

    recognizer = sr.Recognizer()
    mic = sr.Microphone(sample_rate=RATE)

    recognizer.pause_threshold = 1

def listen_to_command():
    print("Listening to your command!")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=.2)

        try:
            audio = recognizer.listen(source, timeout=AUDIO_START_TIMEOUT, phrase_time_limit=AUDIO_TIME_LIMIT)
            command = recognizer.recognize_google(audio)
            print(f"Commmand recognized: {command}")
            return command
        except:
            print("Did not get command")

def wait_for_wake_word():
    print(f"* Listening for the wake word '{WAKE_WORD}'...")

    while True:
        pcm = stream.read(CHUNK)
        pcm = struct.unpack_from("h"*CHUNK, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index == 0:
            return