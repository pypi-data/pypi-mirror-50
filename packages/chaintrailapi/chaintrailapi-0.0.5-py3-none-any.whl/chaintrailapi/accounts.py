from . import session


class Account(object):

    def __init__(self, id):
        self.id = id

    def info(self):
        response = session.get('/anything/{}'.format(self.id))
        return response.json()

    @staticmethod
    def uuid():
        response = session.get('/uuid')
        return response.json()
