from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask on port 5050!"

if __name__ == "__main__":
    app.run(port=5050, debug=True)