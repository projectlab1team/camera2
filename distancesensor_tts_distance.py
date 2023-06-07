import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO
import time
import pyttsx3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

client = mqtt.Client()

TRIG = 20
ECHO = 21
print("초음파 거리 측정기")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("초음파 출력 초기화")
time.sleep(2)
client.connect('localhost', 1883)

engine = pyttsx3.init()

# TTS 소리 크기 조절
volume_level = 5.0  # 0.0 ~ 1.0 (1.0은 최대 볼륨)
engine.setProperty('volume', volume_level)

try:
    while True:
        GPIO.output(TRIG,True)
        time.sleep(0.00001)        # 10uS의 펄스 발생을 위한 딜레이
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            start = time.time()     # Echo핀 상승 시간값 저장
            
        while GPIO.input(ECHO)==1:
            stop = time.time()      # Echo핀 하강 시간값 저장
            
        check_time = stop - start
        distance = round((check_time * 34300 / 2),1)  #거리계산 + 소수점1자리수까지

        client.publish('sensor', distance, 1) #mqtt출력
        print("Distance : %.1f cm" % distance)
        
        # 거리를 TTS로 출력
        engine.say("%.1f centimeters" % distance)
        engine.runAndWait()
        
        time.sleep(1)

except KeyboardInterrupt:
    print("거리 측정 완료")
    client.publish('siye', "거리 측정 완료")
    GPIO.cleanup()   
