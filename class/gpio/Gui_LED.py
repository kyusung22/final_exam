from tkinter import *
import RPi.GPIO as GPIO 
import time   
import threading

frame = Tk()
light_on=False
music_on=False
led_pin = 4

 # 불필요한 warning 제거
GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 
# LED 핀의 OUT설정
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(18, 100)  

Frq = [ [392,392,440,440,392,392,330],
[392,392,330,330,294],
[392,392,440,440,392,392,330],
[392,330,294,330,262 ] ]

speed = 0.5 # 음과 음 사이 연주시간 설정 (0.5초)
delay_Value = 0.75

def buttonled_callback():
    global light_on    # Global 변수선언 
    if light_on == False:  # LED 불이 꺼져있을때 
        GPIO.output(led_pin,1)   # LED ON 
        buttonLed.config(text="LED OFF")
        print("LED ON!")
    else:                                # LED 불이 져있을때 
        GPIO.output(led_pin,0)  # LED OFF
        buttonLed.config(text="LED ON")
        print("LED OFF!")
    light_on = not light_on  # False <=> True

def buttonmusic_callback():
    global music_on    # Global 변수선언 
    buttonMusic.config(text="Music OFF")

    p.start(10)  # PWM 시작 , 듀티사이클 10 (충분)  
    if music_on == False:
        try:
            while 1:                
                for i in range(4):
                    for fr in Frq[i]:
                        p.ChangeFrequency(fr)    #주파수를 fr로 변경
                        time.sleep(speed)       #speed 초만큼 딜레이 (0.5s) 
                    time.sleep(delay_Value)                
        except KeyboardInterrupt:      # 키보드 Ctrl+C 눌렀을때 예외발생 
            pass                       # 무한반복을 빠져나와 아래의 코드를 실행  
            p.stop()                        # PWM을 종료
            GPIO.cleanup()                 # GPIO 설정을 초기화 
            #
    

buttonLed=Button(frame,text="LED ON",command= buttonled_callback)
buttonMusic=Button(frame,text="MUSIC ON",command= buttonmusic_callback)

buttonLed.pack()
buttonMusic.pack()

frame.mainloop()