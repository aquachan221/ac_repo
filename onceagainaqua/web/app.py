from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
chat_history = []  # In-memory message storage

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    user_message = data.get('message')
    if user_message:
        chat_history.append({'user': user_message, 'bot': f"You said: {user_message}"})
        return jsonify(chat_history[-1])
    return jsonify({'error': 'No message received'}), 400

@app.route('/history')
def history():
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)