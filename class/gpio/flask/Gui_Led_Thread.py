from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM)

led_pin=4

# GPIO 18번 핀을 출력으로 설정 
GPIO.setup(4, GPIO.OUT)  
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 50Hz
GPIO.setup(18, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 100)  

lock=threading.Lock()     

stans = False
GPIO.setup(led_pin, GPIO.OUT)

def musicstart():
    global stans
    global Frq
    global p
    try:
        lock.acquire()
        p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)
        for fr in Frq:
            if stans==True: break
            p.ChangeFrequency(fr)    #주파수를 fr로 변경   
            time.sleep(0.5) 
        lock.release()
        p.stop()
                   
        return "ok"
    except :
        return "fail"

     

Frq = [ 392, 392, 440, 440, 392,392,330,392]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/led/on")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def led_on():
    try:
        GPIO.output(led_pin,1)         # 불을 켜고
        return "ok"                         # 함수가 'ok'문자열을 반환함
    except :
        return "fail"

@app.route("/led/holy")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def led_holy():
    try:
        GPIO.output(led_pin,0)         # 불을 켜고
        return "ok"                         # 함수가 'ok'문자열을 반환함
    except :
        return "fail"



@app.route("/music/on")
def led_off():
    global stans
    stans=False
    t1 = threading.Thread(target=musicstart)
    t1.start()
    t1.join()

@app.route("/music/off")
def music_off():
    global stans
    stans = True
    t1 = threading.Thread(target=musicstart)
    t1.start()
    t1.join()
        
    


if __name__ == "__main__":
    app.run(host="0.0.0.0")