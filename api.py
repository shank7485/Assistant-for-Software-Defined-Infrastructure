import os
from flask import Response, request
from flask import render_template, send_from_directory
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user

from assistant.base import Decider
from assistant.base import app
from assistant.base import bot
from assistant.client import OpenStackClient
from assistant.sessions_file import SESSION

app.config.update(
    SECRET_KEY='secret_xxx'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def index():
   return render_template('login.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        auth = OpenStackClient().keystone_auth(username, password)
        if auth:
            print "login window"
            user_id = auth[1]
            user = User(user_id)
            login_user(user)
            return render_template('chat-screen.html')
        else:
            return render_template('login.html',
                                   message='Invalid Username/Password',
                                   color='red')
    else:
        return render_template('login.html',
                               message='If you are not sure which  '
                                       'authentication method to use, '
                                       'contact your administrator.',
                               color='#31708f')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html',
                           message='If you are not sure which '
                                   'authentication method to use, '
                                   'contact your administrator.',
                           color='#31708f')


@app.errorhandler(401)
def page_not_found(e):
    return render_template('login.html',
                           message='If you are not sure which authentication '
                                   'method to use, contact your '
                                   'administrator.',
                           color='#31708f')
    return Response('<p> Login failed </p>')


@app.route('/getConsoleLog')
@login_required
def getConsoleLog():
    ip = request.args.get('ip')
    os.system("scp -i /home/ubuntu/deploy_key.pem  "
              "ubuntu@" + str(ip) + ":/home/ubuntu/log_" + str(ip) +
              ".txt /home/ubuntu/")
    return send_from_directory('/home/ubuntu/', 'log_' +str(ip)+ '.txt')


@app.route('/consoleScreen')
@login_required
def console():
    ip = request.args.get('ip')
    return render_template('console.html', ip=ip)


@app.route('/chat')
@login_required
def end_point():
    try:
        # To chatterbot
        question = request.args.get('question')
        bot_response = str(bot.get_response(question))
        print "Question "+question
        print "Bot Response "+bot_response
        code = bot_response.split(':')[0]
        response = bot_response.split(':')[1]
        # Call code checker.
        return Decider(code, response).get_response()
    except Exception, e:
        print e
        return Decider('0.0', bot_response).get_response()


@app.route('/set')
@login_required
def set():
    key = request.args.get('key')
    value = request.args.get('value')
    SESSION[key] = value
    bot_response = str(bot.get_response(key))
    print "Bot Response " + bot_response
    code = bot_response.split(':')[0]
    response = bot_response.split(':')[1]
    # Update corpus question = key and answer = code, response.
    return Decider(code, response).get_response()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
