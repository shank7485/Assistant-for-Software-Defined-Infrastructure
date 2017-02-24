import chatterbot
import os
from shutil import copyfile


class CopyCorpus(object):
    def __init__(self):
        self.directory = os.path.dirname(chatterbot.__file__)
        self.subdirectory = '{}{}'.format(
            self.directory, '/corpus/data/openstack/')

    def copy(self):
        if not os.path.exists(self.subdirectory):
            os.makedirs(self.subdirectory)
            print('Made /corpus/data/openstack/ directory.')

        src = 'openstack-corpus/conversation.corpus.json'
        dst = self.subdirectory
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        copyfile(src, dst)
        print('Loaded OpenStack conversation.corpus.json')

