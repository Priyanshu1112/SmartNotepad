import string
from tkinter.filedialog import *
import os

class File_Model:
    def __init__(self):
        self.url=''
        self.key=string.ascii_letters+''.join(string.digits)
        self.offset=5

    def encrypt(self, plaintext):
        result=''
        for ch in plaintext:
            try:
                index=(self.key.index(ch)+self.offset)%62
                result+=self.key[index]
            except ValueError:
                result+=ch
        return result

    def decrypt(self, ciphertext):
        result=''
        for ch in ciphertext:
            try:
                index=(self.key.index(ch)-self.offset)%62
                result+=self.key[index]
            except ValueError:
                result+=ch
        return result

    def open_file(self):
        self.url=askopenfilename(title='Select File', filetypes=[("Text Documents", "*.*")])

    def new_file(self):
        self.url=''

    def save_as(self, msg):
        encrypted=self.encrypt(msg)
        self.url=asksaveasfile(mode='w', defaultextension='.ntxt', filetypes=([('All Files', '*.*'),('Text Documents', '*.txt')]))
        self.url.write(encrypted)
        filepath=self.url.name
        self.url.close()
        self.url=filepath

    def save_changes(self, msg, path):
        filename, file_extension = os.path.splitext(path)
        if file_extension in '.ntxt':
            msg = self.encrypt(msg)
        with open(path, 'w') as fw:
            fw.write(msg)

    def save_file(self, msg):
        if self.url=='':
            self.url=asksaveasfilename(title='Select File', defaultextension='.ntxt', filetypes=[('Text Documents', '*.*')])
        filename, file_extension=os.path.splitext(self.url)
        content=msg
        if file_extension in '.ntxt':
            content=self.encrypt(content)
        with open(self.url, 'w', encoding='utf-8') as fw:
            fw.write(content)

    def read_file(self, url=''):
        if url != '':
            self.url=url
        else:
            self.open_file()
        base=os.path.basename(self.url)
        filename, file_extension=os.path.splitext(self.url)
        fr=open(self.url,'r')
        contents=fr.read()
        if file_extension=='.ntxt':
            contents=self.decrypt(contents)
        fr.close()
        return contents, base




