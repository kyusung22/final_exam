# 웹서버 프로그램 웹 브라우저에서 http://localhost:5000/로 접속하면 
# index.html을 실행하고 버튼을 이용하여 LED 작동시킴

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
import time   

light_on= False

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)                    #BOARD는 커넥터 pin번호 사용

pin=7         
buzzer= 12                              

GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(buzzer, GPIO.OUT)

# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(buzzer, 100)  

Frq = [ [392,392,440,440,392,392,330],
[392,392,330,330,294],
[392,392,440,440,392,392,330],
[392,330,294,330,262 ] ]

speed = 0.5 # 음과 음 사이 연주시간 설정 (0.5초)
delay_Value = 0.75


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/led/on")                       # index.html에서 이 주소를 접속하여 해당 함수를 실행
def led_on():
    try:
        global light_on    # Global 변수선언 
        if light_on == False:  # LED 불이 꺼져있을때 
            GPIO.output(pin,1)   # LED ON 
            #buttonLed.config(text="LED OFF")
            print("LED ON!")
            light_on=True
            return "ok1"
        else:                                # LED 불이 져있을때 
            GPIO.output(pin,0)  # LED OFF
            #buttonLed.config(text="LED ON")
            print("LED OFF!")
            light_on=False
            return "ok2"  # False <=> True
    except :
        return "fail"

@app.route("/led/off")
def led_off():
    p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)  
    try:
        while 1:                
            for i in range(4):
                for fr in Frq[i]:
                    p.ChangeFrequency(fr)    #주파수를 fr로 변경
                    time.sleep(speed)       #speed 초만큼 딜레이 (0.5s) 
                time.sleep(delay_Value)                
        return "ok"
    except :
        pass                       # 무한반복을 빠져나와 아래의 코드를 실행  
        p.stop()                        # PWM을 종료
        GPIO.cleanup()                 # GPIO 설정을 초기화     
        return "fail"

if __name__ == "__main__":
    app.run(host="0.0.0.0")