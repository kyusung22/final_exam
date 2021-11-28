from flask import Flask, request
import RPi.GPIO as GPIO

app = Flask(__name__)

LED = 7
GPIO.setmode(GPIO.BOARD)        #BOARD는 커넥터 pin번호 사용
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

@app.route("/")
def helloworld():
    return "Hello World"

@app.route("/led/<state>")          # state의 값으로 경로명을 사용함
def led(state):
    if state =='on':
        GPIO.output(LED, GPIO.HIGH)
    else:
        GPIO.output(LED, GPIO.LOW)
    return "LED " + state

@app.route("/gpio/cleanup")
def gpio_cleanup():
    GPIO.cleanup()
    return "GPIO CLEANUP" 

if __name__ == "__main__":
    app.run(host="0.0.0.0")