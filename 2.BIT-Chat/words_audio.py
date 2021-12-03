import pyttsx3

# 初始化语音
engine = pyttsx3.init()  # 初始化语音库
# 设置语速
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)

answer = mian.temp

# 输出语音
engine.say("answer")  # 合成语音
engine.runAndWait()