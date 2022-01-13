from NotePadFileModel import *
import speech_recognition as sr
class File_Controller:
    def __init__(self):
        self.file_model=File_Model()

    def save_file(self, msg):
        self.file_model.save_file(msg)

    def save_as(self, msg):
        self.file_model.save_as(msg)

    def save_changes(self, msg, path):
        self.file_model.save_changes(msg, path)

    def read_file(self, url):
        self.msg, self.base = self.file_model.read_file(url)
        return self.msg, self.base

    def new_file(self):
        self.file_model.new_file()

    def take_query(self):
        s=sr.Recognizer()
        print('Listening...')
        with sr.Microphone() as m:
            sr.pause_threshold = 1
            audio=s.listen(m)
            query=s.recognize_google(audio, language='en-in')
            return query
        