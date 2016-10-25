from base import app
from base import bot
from flask import request


@app.route('/')
def create_VM():
    try:
        question = request.args.get('question')
        bot_response = str(bot.get_response(question))
        return bot_response
    except:
        print('Please pass parameters')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
