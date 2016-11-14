from base import app
from base import bot
from flask import request
from flask import redirect
from flask import render_template,send_from_directory
from client import NovaClient
from sessions_file import SESSION
from base import Decider
from flask import Flask, Response, redirect, url_for, request, session, abort
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
import os
app = Flask(__name__)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user"#"user" + str(id)
        self.password = "user"#self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20       
users = [User(id) for id in range(1, 21)]


# some protected url
@app.route('/')
@login_required
def home():
    return Response("Hello World!")


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if NovaClient().check_keystone(username,password) == True:
            print "login window"
            user = User("1")
            login_user(user)
            return render_template('test.html')
        else:
            return render_template('login.html',message='Invalid Username/Password',color='red')
    else:
        return render_template('login.html',message='If you are not sure which authentication method to use, contact your administrator.',color='#31708f')

# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html',message='If you are not sure which authentication method to use, contact your administrator.',color='#31708f')
    #return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return render_template('login.html',message='If you are not sure which authentication method to use, contact your administrator.',color='#31708f')
    return Response('<p>Login failed</p>')


# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)


def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/getConsoleLog')
def getConsoleLog():
    ip = request.args.get('ip')
    os.system("scp -i /home/ubuntu/nish_key-2.pem  ubuntu@"+str(ip)+":/home/ubuntu/log_"+str(ip)+".txt static/")
    return send_from_directory('static', 'log_'+str(ip)+'.txt')
    # UI: User clicks and goes to processLogin

@app.route('/consoleScreen')
def console():
    ip = request.args.get('ip')
    # UI: User clicks and goes to processLogin
    return render_template('console.html',ip=ip)

@app.route('/chatScreen')
@login_required
def chatScreen():
    # UI: User clicks and goes to processLogin
    return render_template('test.html')

@app.route('/test')
def test():
    # UI: Initial Landing page
    return render_template('index.html')


@app.route('/')
#@app.route('/logini')
#def login():
 #   # UI: User clicks and goes to processLogin
 #   return render_template('login.html')
#

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
def set():
    #import pdb; pdb.set_trace()
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
    bot.copy()
    app.run(host='0.0.0.0',debug=True, port=8080)
