from flask import Flask, jsonify, request
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import random

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

bot = ChatBot('tinybot')
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.english.greetings')

@app.route('/process-message', methods=['GET', 'POST'])
def process_message():
    message = request.json.get('message')
    response = bot.get_response(message)
    return jsonify({'message': str(response)})

if __name__ == '__main__':
    app.run()