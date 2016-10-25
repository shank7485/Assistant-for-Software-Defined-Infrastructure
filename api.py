from flask import request
from base import OpenStackBot
from base import app

@app.route('/')
def create_VM():
    try:
        question = request.args.get('question')
        bot = OpenStackBot()
        bot_response = str(bot.get_response(question))
        return bot_response
    except:
        print('Please pass parameters')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
