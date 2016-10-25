class Session(object):
    def __init__(self, **kwargs):
        self.falvor = kwargs.get('flavor')
        self.image = kwargs.get('image')
        self.name = kwargs.get('name')
