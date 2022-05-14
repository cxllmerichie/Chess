from speech_recognition import Recognizer, Microphone, AudioData
import datetime
import subprocess
import pyttsx3
import webbrowser


class VoiceAssistant:
    def __init__(self):
        self.engine: pyttsx3 = pyttsx3.init()
        self.voices: list = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.recognizer: Recognizer = Recognizer()

    def start(self):
        with Microphone() as source:
            # print('Cleaning background noises, please wait...')
            # self.recognizer.adjust_for_ambient_noise(self.source, duration=0.5)
            print('[ASSISTANT] Ask me something:')
            audio: AudioData = self.recognizer.listen(source)
        try:
            # command: str = self.recognizer.recognize_google(recorded_audio)
            str_audio: str = self.recognizer.recognize_google(audio)
            print(str_audio)
            self.engine.say(str_audio)
            if 'exit' in str_audio:
                return
        except Exception as error:
            print(f'[ASSISTANT] Error. (orig: {error})')
