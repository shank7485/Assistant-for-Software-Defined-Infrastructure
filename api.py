from base import app
from base import bot
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from client import OpenStackClient


def code_checker(code, response):
    if code == 1 and 'flavor' not in session:
        flavor_list = ['m1.tiny'] # call get_flavor_list() method.
        return '{} {}'.format(response, flavor_list)
    elif code == 1 and 'image' not in session:
        image_list = ['Ubuntu 14.04 Serve']  # call get_image_list() method.
        return '{} {}'.format(response, image_list)
    elif code == 1 and 'name' not in session:
        return response
    elif code == 1 and 'flavor' in session and 'image' in session and 'name' \
            in session:
        # Update corpus for 'Confirm' and answer = code, response.
        return '{} Flavor: {} Image: {} Name: {}'.format(str(
            bot.get_response('Confirm')),
            session['flavor'],
            session['image'],
            session['name'])
    elif code == 1 and 'confirm' in session:
        # call create_vm_()
        return 'Creation done'


@app.route('/index')
def index():
    # UI: Initial Landing page
    return '<h1> Welcome to OpenStack AI! </h1>'

@app.route('/login')
def login():
    # UI: User clicks and goes to processLogin
    return '<h1> Welcome to Login Page</h1>'

@app.route('/processLogin')
def process_login():
    # Backend:
    username = request.args.get('username')
    password = request.args.get('password')
    session['username'] = username
    session['password'] = password
    if OpenStackClient().check_keystone:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/chat')
def end_point():
    try:
        # To chatterbot
        import pdb; pdb.set_trace()
        question = request.args.get('question')
        bot_response = str(bot.get_response(question))
        code = bot_response.split(',')[0]
        response = bot_response.split(',')[1]
        # Call code checker.
        return code_checker(code, response)
    except Exception, e:
        print(e)

@app.route('/set')
def set():
    key = request.args.get('key')
    value = request.args.get('value')
    session[key] = value
    bot_response = str(bot.get_response(key))
    code = bot_response.split(',')[0]
    response = bot_response.split(',')[1]
    # Update corpus question = key and answer = code, response.
    return code_checker(code, response)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
