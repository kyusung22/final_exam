#-*-coding:utf-8-*-
import spidev
import RPi.GPIO as GPIO
import time
# 딜레이 시간 (센서 측정 간격)
delay = 0.3
# MCP3008 채널중 센서에 연결한 채널 설정
pot_channel = 0
# SPI 인스턴스 spi 생성
spi = spidev.SpiDev()
# SPI 통신 시작하기
spi.open(0, 0)
# SPI 통신 속도 설정
spi.max_speed_hz = 100000

GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 50Hz
p = GPIO.PWM(13, 50)
p.start(0)  # PWM 시작  , 듀티비  = 0

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data


try:     
    while True:

# readadc 함수로 pot_channel의 SPI 데이터를
        # 읽어옵니다.
        pot_value = readadc(pot_channel)
        print ("---------------------------------------")
        print("POT Value: %d" % pot_value)
        if (pot_value>1000):
            pot_value-=24
            p.ChangeDutyCycle(pot_value/10)
        else:
            p.ChangeDutyCycle(pot_value/10)     # dc의 값으로 듀티비 변경  
        time.sleep(delay) # delay 시간만큼 기다립니다.

except KeyboardInterrupt:   # 키보드 Ctrl+C 눌렀을 때 예외발생 
    pass                   # 무한반복을 빠져나와 아래의 코드를 실행  
p.stop()                    # PWM을 종료
GPIO.cleanup()             # GPIO 설정을 초기화
