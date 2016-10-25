from flask import Flask
from flask import request
from chatterbot import ChatBot
from chatterbot.adapters.logic import LogicAdapter

app = Flask(__name__)

class MyLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(MyLogicAdapter, self).__init__(kwargs)

    def can_process(self, statement):
        # Return true if the statement contains the search text
        return 'Search for' in statement.text
        return True

    def process(self, statement):
        from chatterbot.conversation import Statement

        text = "VM"# ... something you return based on your search
        response = Statement(text)

        confidence = 0.5
        return confidence, response


chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
#    logic_adapters=[
#        "chatterbot.adapters.logic.LogicAdapter"
#    ],
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
