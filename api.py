from base import app
from base import bot
from flask import request
from flask import redirect
from flask import render_template
from client import NovaClient,NeutronClient,CinderClient
from base import SESSION
from base import Decider as code_checker

@app.route('/test')
def test():
    # UI: Initial Landing page
    return render_template('index.html')


@app.route('/')
@app.route('/login')
def login():
    # UI: User clicks and goes to processLogin
    return render_template('login.html')


@app.route('/processLogin')
def process_login():
    # Backend:
    username = request.args.get('username')
    password = request.args.get('password')
    SESSION['username'] = username
    SESSION['password'] = password
    print(SESSION['username'])
    if NovaClient().check_keystone() == True:
        return redirect("http://172.99.106.89/index.html", code=302)
    else:
        return redirect("http://172.99.106.89/login.html", code=302)


@app.route('/chat')
def end_point():
    try:
        # To chatterbot
        question = request.args.get('question')
        bot_response = str(bot.get_response(question))
        code = bot_response.split(',')[0]
        response = bot_response.split(',')[1]
        # Call code checker.
        return code_checker(code, response)
    except Exception, e:
        return code_checker('0',bot_response)


@app.route('/set')
def set():
    #import pdb; pdb.set_trace()
    key = request.args.get('key')
    value = request.args.get('value')
    SESSION[key] = value
    bot_response = str(bot.get_response(key))
    code = bot_response.split(',')[0]
    response = bot_response.split(',')[1]
    # Update corpus question = key and answer = code, response.
    return code_checker(code, response)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=8080)
