from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from pydub.playback import play
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from selenium.webdriver.common.by import By
import os
import pyaudio
import webbrowser
from selenium import webdriver
import json
from random import random, randint

model = Model("vosk-model-small-ru-0.22") # полный путь к модели
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=8000
)
start_song = AudioSegment.from_wav('voice\Доброе утро.wav')
play(start_song)

stream.start_stream()
def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']

def play_song(name):
    song = AudioSegment.from_wav(f'voice\{name}.wav')
    play(song)

def access_request():
    voice = ['Есть', 'Загружаю сэр', 'Запрос выполнен сэр', 'К вашим услугам сэр', 'Как пожелаете ']
    randEl = randint(0, len(voice) - 1)
    return voice[randEl]

def command(text):
    if text.find('джарвис') != -1 or text.find('Джарвис') != -1:
        play_song("Да сэр")
        for text1 in listen():
            print(text1)
            if text1.find('открой браузер') != -1 or text1.find('открой пожалуйста браузер') != -1 or text1.find('открой гугл') != -1:
                webbrowser.open('https://google.com', new=0)

                play_song(f'{access_request()}')
                break
            elif text1.find('открой ютуб') != -1:
                driver = webdriver.Chrome(executable_path=r'')
                driver.implicitly_wait(5)
                driver.get('https://youtube.com')
                driver.find_element(By.ID("contents")).find_element(By.NAME('ytd-rich-item-renderer')).click()
                play_song(f'{access_request()}')
                break
            elif text1.find('громкость на максимум') != -1 or text1.find('громкость сто процентов') != -1 or text1.find('вруби на всю') != -1:
                soundVolume_max()
                play_song(f'{access_request()}')
                break
            elif text1.find('громкость на минимум') != -1 or text1.find('громкость ноль процентов') != -1 or text1.find('выключи звук') != -1:
                play_song(f'{access_request()}')
                soundVolume_min()
                break
            elif text1.find('джарвис') != -1 or text1.find('Джарвис') != -1:
                play_song("Да сэр(второй)")
    else:
        print("False")

def soundVolume_max():
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(0.0, None)

def soundVolume_min():
    # Get default audio device using PyCAW
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(-65.25, None)

for text in listen():
    command(text)
    print(text)