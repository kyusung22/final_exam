#-*-coding:utf-8-*-

# 필요한 라이브러리를 불러옵니다. 
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#센서에 연결한 Trig와 Echo 핀의 핀 번호 설정 
led_pin = 4
TRIG = 23
ECHO = 24
print("Distance measurement in progress")

#Trig와 Echo 핀의 출력/입력 설정 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 

# LED 핀의 OUT설정
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 100)  

# 4옥타브 도~시 , 5옥타브 도의 주파수 
#Frq = [ 262, 294, 330, 349, 392, 440, 493, 523 ]
speed = 0.1 # 음과 음 사이 연주시간 설정 (0.5초)

#Trig핀의 신호를 0으로 출력 
GPIO.output(TRIG, False)
print("Waiting for sensor to settle")
time.sleep(2)

try:
    while True: 			     
        GPIO.output(TRIG, True)   # Triger 핀에  펄스신호를 만들기 위해 1 출력
        time.sleep(0.00001)       # 10µs 딜레이 
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            start= time.time() # Echo 핀 상승 시간 
        while GPIO.input(ECHO)==1:
            stop= time.time() # Echo 핀 하강 시간 
            
        check_time = stop - start
        distance = check_time * 34300 / 2
        print("Distance : %.1f cm" % distance)
        
        if (distance <= 30):
            print(" LEDLEDLEDLED! ")
            GPIO.output(led_pin,1)
            p.start(10)
                  
            p.ChangeFrequency(262)    #주파수를 fr로 변경
            time.sleep(speed)
                    
        else:
            print(" OFFOFFOFFOFF! ")
            GPIO.output(led_pin,0)
            p.stop()                        # PWM을 종료
        
            
        time.sleep(0.4)	# 0.4초 간격으로 센서 측정 
        
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
    
 

