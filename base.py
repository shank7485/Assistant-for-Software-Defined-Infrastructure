from chatterbot import ChatBot
from flask import Flask, jsonify
import json

SESSION = {}


class OpenStackBot(object):
    def __init__(self):
        self.trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
        self.corpus = 'chatterbot.corpus.openstack'
        self.chatbot = ChatBot(
            'OpenStack Bot',
            trainer=self.trainer
        )
        self.chatbot.train("chatterbot.corpus.english.greetings", self.corpus)

    def get_response(self, question):
        return self.chatbot.get_response(question)


class Code(object):
    def __init__(self):
        self.code = None
        self.response = None

    def code_checker(self):
        """Implement respective by overriding this method."""
        pass

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
        response = "{\"message\": \"" + argv[2] + "\",\"type\": \"" + argv[
            0] + "\""
        l = []
        if argv[1] is not None:
            response = response + ",\"list\":["
            for a in argv[1]:
                temp = str(a).split(":")[1].strip()[:-1]
                temp1 = "{\"value\": \"" + temp + "\"},"
                response = response + temp1
            response = response[:-1] + "]"
        response = response + ",\"button\":\"" + str(
            button) + "\"" + ",\"callSet\":\"" + str(callSet) + "\""
        response = response + "}"
        return jsonify(json.loads(response))

    def is_session_empty(value, session):
        if value not in session:
            return True
        else:
            return False


class CodeText(Code):
    "Code: 0.*"
    def __init__(self, code, response):
        super(CodeText, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        return self.createJSONResponse("", None, self.response)


class CodeNova(Code):
    "Code: 1.*"
    def __init__(self, code, response):
        super(CodeNova, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        if self.code == '0': # if 1.0
            if self.is_session_empty('flavor', SESSION):
                flavor_list = ['<:m1.tiny>']
                # flavor_list = NovaClient().novaflavorlist()
                return self.createJSONResponse("flavor", flavor_list, self.response, True)
            elif self.is_session_empty('image', SESSION):
                image_list = ['<:ubuntu>']
            # image_list = NovaClient().novaimagelist()
                return self.createJSONResponse("image", image_list, self.response, True)
            elif self.is_session_empty('vm_name', SESSION):
                return self.createJSONResponse("vm_name", None, self.response, False,
                                          True)
            elif 'flavor' in SESSION and 'image' in SESSION and 'vm_name' in SESSION:
                if self.is_session_empty('vm_create_confirm', SESSION):
                    res = '{} Flavor: {} Image: {} Name: {}'.format(str(
                        bot.get_response('VM_Create_Confirm')).split(',')[1],
                                                                    SESSION[
                                                                        'flavor'],
                                                                    SESSION[
                                                                        'image'],
                                                                    SESSION[
                                                                        'vm_name'])
                    lst = ['<:yes>', '<:no>']
                    return self.createJSONResponse("vm_create_confirm", lst, res,
                                              True)
                else:
                    if SESSION['vm_create_confirm'] == 'yes':
                        #NovaClient().novaboot()
                        # NovaClient().novaboot()
                        SESSION.clear()
                        res = \
                        str(bot.get_response('VM_Create_Done')).split(',')[1]
                        return self.createJSONResponse("", None, res)
                    elif SESSION['vm_create_confirm'] == 'no':
                        SESSION.clear()
                        res = \
                        str(bot.get_response('VM_Create_Not_Confirm')).split(
                            ',')[1]
                        return self.createJSONResponse("", None, res)

        if self.code == '1': # if 1.1
            # nova_list = NovaClient().nova_vm_list()
            nova_list = ['<:test>']
            return self.createJSONResponse("", nova_list,  self.response)

        if self.code == 'd': # if 1.d
            if self.is_session_empty('vm_delete', SESSION):
                #nova_list = NovaClient().nova_vm_list()
                nova_list = ['<:test>']
                return self.createJSONResponse("vm_delete", nova_list, self.response,
                                          True)
            elif 'vm_delete' in SESSION:
                if self.is_session_empty('vm_delete_confirm', SESSION):
                    res = str(bot.get_response('VM_Delete_Confirm')).split(',')[
                        1]
                    lst = ['<:yes>', '<:no>']
                    return self.createJSONResponse("vm_delete_confirm", lst, res,
                                              True)
                else:
                    if SESSION['vm_delete_confirm'] == 'yes':
                        #NovaClient().nova_vm_delete()
                        # NovaClient().nova_vm_delete()
                        SESSION.clear()
                        res = \
                        str(bot.get_response('VM_Delete_Done')).split(',')[1]
                        return self.createJSONResponse("", None, res)
                    elif SESSION['vm_delete_confirm'] == 'no':
                        SESSION.clear()
                        res = str(
                            bot.get_response('VM_Delete_Not_Confirm').split(
                                ',')[1])
                        return self.createJSONResponse("", None, res)

        if self.code == '3':
            #avail_zone = NovaClient().avail_zone_session()
            avail_zone = ['<:az>']
            return self.createJSONResponse("", avail_zone, self.response)

        "Add other 1.* related stuff."


class CodeNeutron(Code):
    "Code: 2.*"
    def __init__(self, code, response):
        super(CodeNova, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        if self.code == '0': # if 2.0
            if self.is_session_empty('network_name', SESSION):
                return self.createJSONResponse("network_name", None, self.response)
            elif 'network_name' in SESSION:
                if self.is_session_empty('network_create_confirm', SESSION):
                    res = '{} Network: {}'.format(str(bot.get_response(
                        'Network_Create_Confirm')).split(',')[1],
                                                  SESSION['network_name'])
                    list1 = ['<:yes>', '<:no>']
                    return self.createJSONResponse("Network_Create_Confirm", list1,
                                              res, True)
                else:
                    if SESSION['network_create_confirm'] == 'yes':
                        # NeutronClient().networkcreate()
                        # NeutronClient().networkcreate()
                        SESSION.clear()
                        res = str(
                            bot.get_response('Network_Create_Done').split(',')[
                                1])
                        return self.createJSONResponse("", None, res)
                    elif SESSION['network_create_confirm'] == 'no':
                        SESSION.clear()
                        res = str(bot.get_response(
                            'Network_Create_Not_Confirm').split(',')[1])
                        return self.createJSONResponse("", None, res)

        if self.code == '1': # if 2.1
            #network_list = NeutronClient().netlist()
            network_list = ['<:network>']
            return self.createJSONResponse("", network_list, self.response)

        if self.code == 'd': # if 2.2
            if self.is_session_empty('network_delete', SESSION):
                #network_list = NeutronClient().netlist()
                network_list = ['<:network>']
                return self.createJSONResponse("network_delete", network_list,
                                               self.response)
            elif 'network_delete' in SESSION:
                if self.is_session_empty('network_delete_confirm'):
                    res = '{} Name: {}'.format(
                        str(bot.get_response('Network_Delete_Confirm')))
                    lst = ['<:yes>', '<:no>']
                    return self.createJSONResponse("network_delete_confirm", lst,
                                              res,
                                              True)
                else:
                    if SESSION['network_delete_confirm'] == 'yes':
                        #NeutronClient().netdelete()
                        # NeutronClient().netdelete()
                        SESSION.clear()
                        res = str(
                            bot.get_response('Network_Delete_Done').split(',')[
                                1])
                        return self.createJSONResponse("", None, res)
                    elif SESSION['network_delete_confirm'] == 'no':
                        SESSION.clear()
                        res = str(bot.get_response(
                            'Network_Delete_Not_Confirm').split(',')[1])
                        return self.createJSONResponse("", None, res)

        "Add other 2.* related stuff."


class CodeCinder(Code):
    "Code: 3.*"
    def __init__(self, code, response):
        super(CodeCinder, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        if self.code == '0': # if 3.0
            # volume_list = CinderClient().volumelist()
            volume_list = ['<:vaolume_list>']
            return self.createJSONResponse("", volume_list, self.response)

        "Add other 3.* related stuff."


class Decider(object):
    def __init__(self, code, response):
        if code[0] == '0': # 0.*
            CodeText(code[-1], response).code_checker()
        elif code[0] == '1': # 1.*
            CodeNova(code[-1], response).code_checker()
        elif code[0] == '2': # 2.*
            CodeNeutron(code[-1], response).code_checker()
        elif code[0] == '3': # 3.*
            CodeCinder(code[-1], response).code_checker()
        # extend this elif condition for other classes.

bot = OpenStackBot()
app = Flask(__name__)
