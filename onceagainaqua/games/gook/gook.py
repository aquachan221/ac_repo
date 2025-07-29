from flask import Flask
from flaredantic import FlareTunnel, FlareConfig
import threading

# Define your Flask app
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Flask!"








def run_flask():
    app.run(host="0.0.0.0", port=8080)

config = FlareConfig(port=8080)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

with FlareTunnel(config) as tunnel:
    print(f"🔗 Tunnel active at: {tunnel.tunnel_url}")
    input("🚪 Press Enter to shut it down...")

flask_thread.join()