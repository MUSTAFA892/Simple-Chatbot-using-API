from flask import Flask, render_template, request, jsonify
import cohere

app = Flask(__name__)

co = cohere.Client(api_key="fizBq19c3g3FRkSORAHWq2HMvPC0aQKlV8AHmHyM")
messages = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    messages.append({"role": "User", "message": user_input})

    stream = co.chat_stream(
        model='command-r-08-2024',
        message=user_input,
        temperature=0.3,
        chat_history=messages,
        prompt_truncation='AUTO',
        connectors=[{"id": "web-search"}]
    )

    assistant_reply = ""
    for event in stream:
        if event.event_type == "text-generation":
            assistant_reply += event.text
    
    messages.append({"role": "Chatbot", "message": assistant_reply})
    return jsonify({'response': assistant_reply})

@app.route('/set-prompt', methods=['POST'])
def set_prompt():
    custom_prompt = request.form['prompt']
    messages.insert(0, {"role": "Chatbot", "message": custom_prompt})
    return jsonify({'status': 'success', 'message': f'Prompt updated to: {custom_prompt}'})

if __name__ == '__main__':
    app.run(debug=True)
