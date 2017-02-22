import chatterbot
from chatterbot.conversation.response_selection import get_random_response
from flask import Flask, jsonify
import json
from client import DeployOpenStackCloud, NovaClient, NeutronClient, CinderClient
import os
from shutil import copyfile
from sessions_file import SESSION

class OpenStackBot(object):
    def __init__(self):
        self.corpus = 'chatterbot.corpus.openstack'
        self.chatbot = chatterbot.ChatBot(
            'OpenStack Bot',
            logic_adapters=[
                {
                   'import_path': 'chatterbot.adapters.logic.ClosestMatchAdapter'
                },
                {
                   'import_path': 'chatterbot.adapters.logic.LowConfidenceAdapter',
                   'threshold': 0.65,
                   'default_response': 'I am sorry, but I do not understand.'
                }
            ],
            trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
            response_selection_method=get_random_response
        )
        self.chatbot.train("chatterbot.corpus.english.greetings", self.corpus)

    def get_response(self, question):
        return self.chatbot.get_response(question)


    @staticmethod
    def copy():
        directory = os.path.dirname(chatterbot.__file__)
        # subdirectory_win = '{}{}'.format(directory, '\\corpus\\data\\openstack')
        subdirectory_nix = '{}{}'.format(directory, '/corpus/data/openstack/')

        src = 'conversation.corpus.json'
        dst = subdirectory_nix
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        copyfile(src, dst)
        print('Loaded OpenStack conversation.corpus.json')


class Code(object):
    def __init__(self):
        self.code = None
        self.response = None

    def code_checker(self):
        """Implement respective by overriding this method."""
        pass

    def createJSONResponse(*argv):
        try:
            argv[4]
        except Exception:
            button = False
        else:
            button = argv[4]
        try:
            argv[5]
        except Exception:
            callSet = False
        else:
            callSet = argv[5]
        response = "{\"message\": \"" + argv[3] + "\",\"type\": \"" + argv[
            1] + "\""
        l = []
        if argv[2] is not None:
            response = response + ",\"list\":["
            for a in argv[2]:
                temp = str(a).split(":")[1].strip()[:-1]
                temp1 = "{\"value\": \"" + temp + "\"},"
                response = response + temp1
            response = response[:-1] + "]"
        response = response + ",\"button\":\"" + str(
            button) + "\"" + ",\"callSet\":\"" + str(callSet) + "\""
        response = response + "}"
        return jsonify(json.loads(response))

    def is_session_empty(self, value, session):
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
        try:
            if self.code == '0': # if 1.0
                if self.is_session_empty('flavor', SESSION):
                    # flavor_list = ['<:m1.tiny>']
                    flavor_list = NovaClient().novaflavorlist()
                    return self.createJSONResponse("flavor", flavor_list, self.response, True)
                elif self.is_session_empty('image', SESSION):
                    # image_list = ['<:ubuntu>']
                    image_list = NovaClient().novaimagelist()
                    return self.createJSONResponse("image", image_list, self.response, True)
                elif self.is_session_empty('vm_name', SESSION):
                    return self.createJSONResponse("vm_name", None, self.response, False,
                                              True)
                elif self.is_session_empty('net_name', SESSION):
                    network_list = NeutronClient().netlist()
                    return self.createJSONResponse('net_name', network_list,
                                                   self.response, True)
                elif 'flavor' in SESSION and 'image' in SESSION and 'vm_name'\
                    in SESSION and 'net_name' in SESSION:
                    if self.is_session_empty('vm_create_confirm', SESSION):
                        res = '{} Flavor: {} Image: {} Name: {} Network_Name: {}'\
                            .format(str(bot.get_response('VM_Create_Confirm')).
                                    split(':')[1],SESSION['flavor'],
                                    SESSION['image'],SESSION['vm_name'],
                                    SESSION['net_name'])
                        lst = ['<:yes>', '<:no>']
                        return self.createJSONResponse("vm_create_confirm", lst, res,
                                                  True)
                    else:
                        if SESSION['vm_create_confirm'] == 'yes':
                            NovaClient().novaboot()
                            SESSION.clear()
                            res = \
                            str(bot.get_response('VM_Create_Done')).split(':')[1]
                            return self.createJSONResponse("", None, res)
                        elif SESSION['vm_create_confirm'] == 'no':
                            SESSION.clear()
                            res = \
                            str(bot.get_response('VM_Create_Not_Confirm')).split(
                                ':')[1]
                            return self.createJSONResponse("", None, res)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        try:
            if self.code == '1': # if 1.1
                nova_list = NovaClient().nova_vm_list()
                if len(nova_list) == 0:
                    return self.createJSONResponse("", None, "No VMs")
                return self.createJSONResponse("", nova_list,  self.response)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        try:
            if self.code == 'd': # if 1.d
                if self.is_session_empty('vm_delete', SESSION):
                    nova_list = NovaClient().nova_vm_list()
                    return self.createJSONResponse("vm_delete", nova_list, self.response,
                                              True)
                elif 'vm_delete' in SESSION:
                    if self.is_session_empty('vm_delete_confirm', SESSION):
                        res = str(bot.get_response('VM_Delete_Confirm')).split(':')[
                            1]
                        lst = ['<:yes>', '<:no>']
                        return self.createJSONResponse("vm_delete_confirm", lst, res,
                                                  True)
                    else:
                        if SESSION['vm_delete_confirm'] == 'yes':
                            NovaClient().nova_vm_delete()
                            SESSION.clear()
                            res = \
                            str(bot.get_response('VM_Delete_Done')).split(':')[1]
                            return self.createJSONResponse("", None, res)
                        elif SESSION['vm_delete_confirm'] == 'no':
                            SESSION.clear()
                            res = str(
                                bot.get_response('VM_Delete_Not_Confirm').split(
                                    ':')[1])
                            return self.createJSONResponse("", None, res)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        try:
            if self.code == '3':
                avail_zone = NovaClient().avail_zone_session()
                #avail_zone = ['<:az>']
                return self.createJSONResponse("", avail_zone, self.response)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        "Add other 1.* related stuff."


class CodeNeutron(Code):
    "Code: 2.*"
    def __init__(self, code, response):
        super(CodeNeutron, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        try:
            if self.code == '0': # if 2.0
                if self.is_session_empty('network_name', SESSION):
                    return self.createJSONResponse("network_name", None, self.response,False,True)
                if self.is_session_empty('subnet_name', SESSION):
                    return self.createJSONResponse("subnet_name", None,
                                                   self.response, False, True)
                elif self.is_session_empty('cidr', SESSION):
                    return self.createJSONResponse("cidr", None,
                                                       self.response, False, True)
                elif 'network_name' in SESSION and 'cidr' in SESSION and \
                                'subnet_name' in SESSION:
                    if self.is_session_empty('network_create_confirm', SESSION):
                        res = '{} Network_Name: {} Subnet_Name: {} CIDR: {}' \
                            .format(
                            str(bot.get_response('Network_Create_Confirm')).
                            split(':')[1], SESSION['network_name'],
                            SESSION['subnet_name'], SESSION['cidr'])
                        lst = ['<:yes>', '<:no>']
                        return self.createJSONResponse("network_create_confirm",
                                                       lst, res, True)
                    else:
                        if SESSION['network_create_confirm'] == 'yes':
                            NeutronClient().networkcreate()
                            SESSION.clear()
                            res = str(
                                bot.get_response('Network_Create_Done')).split(':')[
                                    1]
                            return self.createJSONResponse("", None, res)
                        elif SESSION['network_create_confirm'] == 'no':
                            SESSION.clear()
                            res = str(bot.get_response(
                                'Network_Create_Not_Confirm')).split(':')[1]
                            return self.createJSONResponse("", None, res)
        except Exception as e:
            import pdb; pdb.set_trace()
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        try:
            if self.code == '1': # if 2.1
                network_list = NeutronClient().netlist()
                #network_list = ['<:network>']
                if len(network_list) == 0:
                    return self.createJSONResponse("", None, "No Networks")
                return self.createJSONResponse("", network_list, self.response)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        try:
            if self.code == 'd': # if 2.2
                if self.is_session_empty('network_delete', SESSION):
                    network_list = NeutronClient().netlist()
                    #network_list = ['<:network>']
                    return self.createJSONResponse("network_delete", network_list,
                                                   self.response,True)
                elif 'network_delete' in SESSION:
                    if self.is_session_empty('network_delete_confirm', SESSION):
                        res = str(bot.get_response('network_Delete_Confirm')).split(':')[1]
                        lst = ['<:yes>', '<:no>']
                        return self.createJSONResponse("network_delete_confirm", lst,
                                                  res,
                                                  True)
                    else:
                        if SESSION['network_delete_confirm'] == 'yes':
                            NeutronClient().netdelete()
                            SESSION.clear()
                            res = str(
                                bot.get_response('Network_Delete_Done')).split(':')[
                                    1]
                            return self.createJSONResponse("", None, res)
                        elif SESSION['network_delete_confirm'] == 'no':
                            SESSION.clear()
                            res = str(bot.get_response(
                                'Network_Delete_Not_Confirm')).split(':')[1]
                            return self.createJSONResponse("", None, res)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        "Add other 2.* related stuff."


class CodeCinder(Code):
    "Code: 3.*"
    def __init__(self, code, response):
        super(CodeCinder, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        try:
            if self.code == '0': # if 3.0
                volume_list = CinderClient().volumelist()
                #volume_list = ['<:volume_list>']
                if len(volume_list) == 0:
                    return self.createJSONResponse("", None, "No Volumes")
                return self.createJSONResponse("", volume_list, self.response)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)

        "Add other 3.* related stuff."

class CodeDeploy(Code):
    "Code: 4.*"
    def __init__(self, code, response):
        super(CodeDeploy, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        try:
            if self.code == '0':
                if self.is_session_empty('type_of_deployment', SESSION):
                    deploy_list = ['<:all_in_one>', '<:multi_node>']
                    return self.createJSONResponse("type_of_deployment", deploy_list, self.response, True)
                elif self.is_session_empty('ipaddress_confirm', SESSION):
                    ip_list = ['<:192.168.0.225>','<:192.168.0.230>']
                    return self.createJSONResponse("ipaddress_confirm", ip_list, self.response, True)
                elif self.is_session_empty("deploy_confirm", SESSION):
                    choice_list = ['<:yes>', '<:no>']
                    return self.createJSONResponse("deploy_confirm", choice_list, self.response, True)
                else:
                    if SESSION['deploy_confirm'] == 'yes':
                        print SESSION['ipaddress_confirm']
                        DeployOpenStackCloud().deploy(SESSION['ipaddress_confirm'])
                        return self.createJSONResponse(
                            "", None, "We are deploying openstack for you please check status <a target='_blank' href='/consoleScreen?ip="+SESSION['ipaddress_confirm']+"'>Here </a>")
                        SESSION.clear()
                    else:
                        SESSION.clear()
                        res = str(bot.get_response('deploy_not_confirm')).split(
                                ':')[1]
                        return self.createJSONResponse("", None, res)
        except Exception as e:
            response = "Oops! It failed with - " + str(e)
            if "\n" in response:
                response = response.replace("\n", "")
            return self.createJSONResponse("", None, response)


class Decider(object):
    def __init__(self, code, response):
        self.response_value = None
        # code = code.split('.')  I think this should be there
        if code[0] == '0': # 0.*
            self.response_value = CodeText(code[-1], response).code_checker()
        elif code[0] == '1': # 1.*
            self.response_value = CodeNova(code[-1], response).code_checker()
        elif code[0] == '2': # 2.*
            self.response_value = CodeNeutron(code[-1], response).code_checker()
        elif code[0] == '3': # 3.*
            self.response_value = CodeCinder(code[-1], response).code_checker()
        elif code[0] == '4':
            self.response_value = CodeDeploy(code[-1], response).code_checker()
        # extend this elif condition for other classes.

    def get_response(self):
        return self.response_value

bot = OpenStackBot()
app = Flask(__name__)
