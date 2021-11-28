#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

#  노란색 LED, 빨간색 LED, 센서 입력핀 번호 설정 
led_Y = 21
sensor = 4
SERVO_PIN = 18
buzzer= 19
# 불필요한 warning 제거,  GPIO핀의 번호 모드 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# LED 핀의 IN/OUT(입력/출력) 설정 
GPIO.setup(led_Y, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(19, 100)

Frq = [349]
speed= 0.5                                    
                                                                        
# PWM 인스턴스 servo 생성, 주파수 50으로 설정 
servo = GPIO.PWM(SERVO_PIN,50)
# PWM 듀티비 0 으로 시작 
servo.start(0)


print ("PIR Ready . . . . ")
time.sleep(5)  # PIR 센서 준비 시간 
c = 0

try:
    while True:
        if GPIO.input(sensor) == 1: 	#센서가 High(1)출력 
                c+=1
                p.start(10)
                GPIO.output(led_Y, 1)   # 노란색 LED 켬
                print("Motion Detected !")
                servo.ChangeDutyCycle(7.5)  # 0eh 
                print(c)
                time.sleep(0.2)
                for fr in Frq:
                        p.ChangeFrequency(fr)    #주파수를 fr로 변경                servo.ChangeDutyCycle(7.5)  # 90도 
                        time.sleep(speed)       #speed 초만큼 딜레이 (0.5s) 

                
        if GPIO.input(sensor) == 0:      #센서가 Low(0)출력  
                GPIO.output(led_Y, 0)   # 노란색 LED 끔
                print("NOT Detected !")
                servo.ChangeDutyCycle(2.5)  # 0eh 
                p.stop()
                time.sleep(0.2)                    
 
except KeyboardInterrupt:
                print("Stopped by User")
                
                GPIO.cleanup()

