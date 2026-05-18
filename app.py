from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_email():

    try:

        data = request.json

        purpose = data.get('purpose')
        tone = data.get('tone')
        recipient = data.get('recipient')

        prompt = f"""
        You are a professional email writer.

        Write a complete professional email.

        Purpose:
        {purpose}

        Tone:
        {tone}

        Recipient:
        {recipient}

        Include:
        1. Subject Line
        2. Proper Greeting
        3. Professional Email Body
        4. Closing Message
        """

        response = client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        result = response.choices[0].message.content

        return jsonify({
            'result': result
        })

    except Exception as e:

        return jsonify({
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)