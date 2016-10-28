from base import app
from base import bot
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from client import NovaClient,NeutronClient,CinderClient
from flask import jsonify
import json

SESSION = {}

def createJSONResponse(*argv):
    try:
       argv[3]
    except Exception:
       button = False
    else:
       button = argv[3]
    try:
       argv[4]
    except Exception:
       callSet = False
    else:
       callSet = argv[4]
    response = "{\"message\": \""+argv[2]+"\",\"type\": \""+argv[0]+"\""
    l = []
    if argv[1] is not None:
         response = response + ",\"list\":["
         for a in argv[1]:
                temp = str(a).split(":")[1].strip()[:-1]
                temp1 = "{\"value\": \""+temp+"\"},"
                response = response + temp1
         response = response[:-1] + "]"
    response = response + ",\"button\":\""+str(button)+"\""+ ",\"callSet\":\""+str(callSet)+"\""
    response = response+ "}"
    return "angular.callbacks._0("+response+")"


def code_checker(code, response):
    if code == '0':
        return createJSONResponse("", None, response)

    if code == '1':
        if is_session_empty('flavor', SESSION):
            # flavor_list = ['<:m1.tiny>']
            flavor_list = NovaClient().novaflavorlist()
            return createJSONResponse("flavor", flavor_list, response, True)
        elif is_session_empty('image', SESSION):
            # image_list = ['<:ubuntu>']
            image_list = NovaClient().novaimagelist()
            return createJSONResponse("image", image_list, response, True)
        elif is_session_empty('vm_name', SESSION):
            return createJSONResponse("vm_name", None, response)
        elif 'flavor' in SESSION and 'image' in SESSION and 'vm_name' in SESSION:
            if is_session_empty('vm_create_confirm', SESSION):
                res = '{} Flavor: {} Image: {} Name: {}'.format(str(
                    bot.get_response('VM_Create_Confirm')),
                    SESSION['flavor'],
                    SESSION['image'],
                    SESSION['vm_name'])
                lst = ['<:yes>', '<:no>']
                return createJSONResponse("vm_create_confirm", lst, res,
                                          True)
            else:
                if SESSION['vm_create_confirm'] == 'yes':
                    NovaClient().novaboot()
                    #NovaClient().novaboot()
                    SESSION.clear()
                    res = str(bot.get_response('VM_Create_Done'))
                    return createJSONResponse("", None, res)
                elif SESSION['vm_create_confirm'] == 'no':
                    SESSION.clear()
                    res = str(bot.get_response('VM_Create_Not_Confirm'))
                    return createJSONResponse("", None, res)

    if code == '1.1':
        nova_list = NovaClient().nova_vm_list()
        #nova_list = ['<:test>']
        return createJSONResponse("", nova_list, response)

    if code == '1.d':
        if is_session_empty('vm_delete', SESSION):
            nova_list = NovaClient().nova_vm_list()
            #nova_list = ['<:test>']
            return createJSONResponse("vm_delete", nova_list, response)
        elif 'vm_delete' in SESSION:
            if is_session_empty('vm_delete_confirm', SESSION):
                res = '{} Name: {}'.format(str(bot.get_response('VM_Delete_Confirm')))
                lst = ['<:yes>', '<:no>']
                return createJSONResponse("vm_delete_confirm", lst, res,
                                          True)
            else:
                if SESSION['vm_delete_confirm'] == 'yes':
                    NovaClient().nova_vm_delete()
                    #NovaClient().nova_vm_delete()
                    SESSION.clear()
                    res = str(bot.get_response('VM_Delete_Done'))
                    return createJSONResponse("", None, res)
                elif SESSION['vm_delete_confirm'] == 'no':
                    SESSION.clear()
                    res = str(bot.get_response('VM_Delete_Not_Confirm'))
                    return createJSONResponse("", None, res)

    if code == '1.3':
        avail_zone = NovaClient().avail_zone_session()
        #avail_zone = ['<:az>']
        return createJSONResponse("", avail_zone, response)

    if code == '2':
        if is_session_empty('network_name', SESSION):
            return createJSONResponse("network_name", None, response)
        elif 'network_name' in SESSION :
            if is_session_empty('network_create_confirm', SESSION):
                res = '{} Network: {}'.format(str(bot.get_response(
                    'Network_Create_Confirm')), SESSION['network_name'])
                list1 = ['<:yes>', '<:no>']
                return createJSONResponse("Network_Create_Confirm", list1,
                                          res, True)
            else:
                if SESSION['network_create_confirm'] == 'yes':
                    NeutronClient().networkcreate()
                    #NeutronClient().networkcreate()
                    SESSION.clear()
                    res = str(bot.get_response('Network_Create_Done'))
                    return createJSONResponse("", None, res)
                elif SESSION['network_create_confirm'] == 'no':
                    SESSION.clear()
                    res = str(bot.get_response('Network_Create_Not_Confirm'))
                    return createJSONResponse("", None, res)

    if code == '2.1':
        network_list = NeutronClient().netlist()
        #network_list = ['<:network>']
        return createJSONResponse("", network_list, response)

    if code == '2.2':
        if is_session_empty('network_delete', SESSION):
            network_list = NeutronClient().netlist()
            #network_list = ['<:network>']
            return createJSONResponse("network_delete", network_list, response)
        elif 'network_delete' in SESSION:
            if is_session_empty('network_delete_confirm'):
                res = '{} Name: {}'.format(str(bot.get_response('Network_Delete_Confirm')))
                lst = ['<:yes>', '<:no>']
                return createJSONResponse("network_delete_confirm", lst, res,
                          True)
            else:
                if SESSION['network_delete_confirm'] == 'yes':
                    NeutronClient().netdelete()
                    #NeutronClient().netdelete()
                    SESSION.clear()
                    res = str(bot.get_response('Network_Delete_Done'))
                    return createJSONResponse("", None, res)
                elif SESSION['network_delete_confirm'] == 'no':
                    SESSION.clear()
                    res = str(bot.get_response('Network_Delete_Not_Confirm'))
                    return createJSONResponse("", None, res)

    if code == '3':
        volume_list = CinderClient.volumelist()
        return createJSONResponse("", volume_list, response)


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
        print(e)


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
    app.run(debug=True, port=8080)
