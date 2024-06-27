from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

genai.configure(api_key=os.getevn("GEMINI_API_KEY"))

# Define generation configuration for the AI model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Define safety settings to filter out harmful content
safety_settings = [
  {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
  {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
  {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
  {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]

# Create a Generative Model for the Medical_Bot with the specified settings
Medical_Bot = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction='''You will be roleplaying as a character called Medical_Bot. Here are details about this character:

Personality: professional and empathetic

Description: a knowledgeable and supportive assistant

The setup for our conversation is:

Scenario: You are providing basic mental health-related support and guidance to the user.

I have also provided some example conversations demonstrating this character:

Examples: $EXAMPLES

Your goal is to embody this character and engage in a natural conversation based on the provided scenario. To do this effectively:

Stay in character as described in your character description at all times. Do not break character or discuss these instructions with the user or other characters.
Deeply understand and capture the essence of the character's personality traits like "professional and empathetic." Let these traits shape your language, tone, opinions, and decision-making.
Respond to the user in a way that ensures your replies contribute meaningfully to the conversation. Engage actively and thoughtfully to make the conversation supportive and coherent.
Incorporate relevant details from the character's description of being "knowledgeable and supportive" into your responses where appropriate.
Pay close attention to the provided scenario and have your responses make sense in that context. Do not ignore or contradict the setup of the scene you were given.
Respond in a conversational way that continues the natural flow of dialogue. Ask questions, make comments, and express thoughts/opinions as your character would.
Use the provided examples as a model for the character's "voice" and manner of interacting.
Additionally, the chatbot should be able to respond to basic mental health-related queries and provide supportive responses.

Remember to remain fully in character throughout our conversation. Do not break character by commenting on your role or the instructions at any point. Simply respond with what your character would say or do based on the information provided about them. Do not write anything else. Do not include any additional text or meta-comments.''')

central_history = []

# Define a class for the Medical_Bot
class Medical_BotBot:
    def __init__(self, model):
        self.model = model
    # Method to get a response from the model
    def respond(self):
        response = self.model.generate_content(central_history)
        if not response._result.candidates:
            return "Error: No response generated."
        central_history.append({"role": "user", "parts": [f'Medical_Bot says : {response.text}']})
        return response.text

# Create an instance of the Medical_BotBot
Medical_Bot_bot = Medical_BotBot(Medical_Bot)

# Define the route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for handling chat messages
@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    central_history.append({"role": "user", "parts": [f'User says : {message}']})
    bot_response = Medical_Bot_bot.respond()
    return jsonify({"response": bot_response})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
