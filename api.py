from base import app
from base import bot
from base import sess
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import render_template
from client import NovaClient,NeutronClient

def createJSONResponse(type,list,msg):
    response = "{message: \""+msg+"\",\"list\":["
    l = []
    for a in list:
         temp = str(a).split(":")[1].strip()[:-1]
         temp1 = "{\"value\": \""+type+"\", \"onclick\": \"setvariable("+type+","+temp+")\"},"
         response = response + temp1
         #print temp1
    response = response[:-1] + "]}"
    return response

def code_checker(code, response):
    if code == '1':
        if is_session_empty('flavor', session):
            flavor_list = NovaClient().novaflavorlist()
            return createJSONResponse("Flavor list",flavor_list,response)
        elif is_session_empty('image', session):
            image_list = NovaClient().novaimagelist()
            return createJSONResponse("Image list",image_list,response)
        elif is_session_empty('name', session):
            return response
        elif 'flavor' in session and 'image' in session and 'name' in session \
            and is_session_empty('confirm', session):
            return '{} Flavor: {} Image: {} Name: {}'.format(str(
                bot.get_response('Confirm')),
                session['flavor'],
                session['image'],
                session['name'])
        elif 'confirm' in session:
            NovaClient().novaboot()
            session.clear()
            return 'Creation done'

    if code == '1.1':
        nova_list = NovaClient().nova_vm_list()
        return createJSONResponse("Nova list",nova_list,response)

    if code == '2':
        if is_session_empty('network_name', session):
            return response
        elif 'network_name' in session and is_session_empty(
                'confirm_network', session):
            return '{} Network: {}'.format(str(bot.get_response(
                'confirm_network'), session['network_name']))
        elif 'confirm_network' in session:
            NeutronClient().networkcreate()
            # call create_network()
            session.clear()
            return 'Network Creation Done'

    if code == '2.1':
        network_list = NeutronClient().netlist()
        return '{} : {}'.format(str(bot.get_response('Net_List')),
                                network_list)
    
    if code == '3':
        avail_zone = NovaClient().avail_zone_session()
        return createJSONResponse("AZ",avail_zone,response)


def is_session_empty(value, session):
    if value not in session:
        return True
    else:
        return False

@app.route('/test')
def test():
    # UI: Initial Landing page
    return render_template('index.html')

@app.route('/')
def index():
    # UI: Initial Landing page
    return '<h1> Welcome to OpenStack AI! </h1>' \
           'Please go to /login to see login page.'

@app.route('/login')
def login():
    # UI: User clicks and goes to processLogin
    return render_template('index.html')

@app.route('/processLogin')
def process_login():
    # Backend:
    username = request.args.get('username')
    password = request.args.get('password')
    session['username'] = username
    session['password'] = password
    if NovaClient().check_keystone:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

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
    app.secret_key = 'test'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)

    app.run(host='0.0.0.0', debug=True, port=8080)
