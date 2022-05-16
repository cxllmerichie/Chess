from speech_recognition import Recognizer, Microphone, AudioData
import pyttsx3


class VoiceAssistant:
    def __init__(self):
        self.engine: pyttsx3 = pyttsx3.init()
        self.voices: list = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.recognizer: Recognizer = Recognizer()

    def start(self):
        with Microphone() as source:
            print('Cleaning background noises, please wait...')
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print('[ASSISTANT] Ask me something:')
            audio: AudioData = self.recognizer.listen(source)
        try:
            # str_audio: str = self.recognizer.recognize_google(audio)
            str_audio: str = self.recognizer.recognize_sphinx(audio)
            print(str_audio)
            self.engine.say(str_audio)
            if 'exit' in str_audio:
                return
        except Exception as error:
            print(f'[ASSISTANT] Error. (orig: {error})')
