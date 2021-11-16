from aip import AipSpeech
import wave
from pyaudio import PyAudio, paInt16
import time
import requests
import json
#import speech_recognition as sr
#import win32com.client

APP_ID = '25172883'
API_KEY = 'b64rGZlWU3qgHdjrNwTA9TGH'
SECRET_KEY = '114nvOta4IwzUEOe5B02NbN3t8EdK25a'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# #############################生 成 录 音 文 件#######################################
framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'audio.wav'

def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()

# 录音
def my_record():
    pa = PyAudio()
    # 打开一个新的音频stream
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []  # 存放录音数据

    t = time.time()
    print('正在录音...')

    while time.time() < t + 5:  # 设置录音时间（秒）
        # 循环read，每次read 2000frames
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()

path = 'audio.wav'

###########################################################################################


# 将语音转文本STT
def listen():
    # 读取录音文件
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        # 参数dev_pid：1536普通话(支持简单的英文识别)、1537普通话(纯中文识别)、1737英语、1637粤语、1837四川话、1936普通话远场
        result = client.asr(voices, 'wav', 16000, {'dev_pid': 1537, })
        # result = CLIENT.asr(get_file_content(path), 'wav', 16000, {'lan': 'zh', })
        # print(result)
        # print(result['result'][0])
        # print(result)
        result_text = result["result"][0]
        print("you said: " + result_text)
        return result_text
    except KeyError:
        print("KeyError")

###########################################################################################





# #########################      调 用     #######################################
while True:
    my_record()
    request = listen()
    print(request)
    # response = Turing(request)
    # speaker.Speak(response)






