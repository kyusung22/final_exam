from flask import Flask
app = Flask(__name__)

@app.route("/")
def helloworld():
    return "Hello world rbtjddbs"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000) # port 입력하지 않을시 기본 5000