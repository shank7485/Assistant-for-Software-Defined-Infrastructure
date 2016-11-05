from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot import ChatBot
from flask import Flask, jsonify
import json


SESSION = {}

class CustomLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(CustomLogicAdapter, self).__init__(kwargs)

    def can_process(self, statement):
        # Return true if the statement contains the search text
        return 'Search for' in statement.text

    def process(self, statement, search_text):
        text =  search_text # ... something you return based on your search
        response = Statement(text)
        confidence = 0.5
        return confidence, response


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

    def get_code(self):
        return self.code

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
    "Code: 0"
    def __init__(self, code, response):
        super(CodeText, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        return self.createJSONResponse("", None, self.response)


class CodeNova(Code):
    "code: 1.*"
    def __init__(self, code, response):
        super(CodeNova, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        if self.code == '1':
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

        if self.code == '1.1':
            # TODO
            pass

        "Add other 1.* related stuff."


class CodeNeutron(Code):
    "code: 1.*"
    def __init__(self, code, response):
        super(CodeNova, self).__init__()
        self.code = code
        self.response = response

    def code_checker(self):
        # TODO Similar to Nova.
        pass


bot = OpenStackBot()

app = Flask(__name__)
