from flask import Flask
from flask import request
from chatterbot import ChatBot

app = Flask(__name__)

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
chatbot.train("chatterbot.corpus.openstack")

@app.route('/')
def create_VM():
    try:
        question = request.args.get('question')
        return str(chatbot.get_response(question))
    except:
        print('Please pass parameters')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
