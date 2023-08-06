class AuthorizationError(Exception):

    def __init__(self, message='Not authorised, please check that you have a valid token'):
        Exception.__init__(self)
        self.message = message


class InvalidTykInstance(Exception):

    def __init__(self, message='Invalid tyk domain'):
        Exception.__init__(self)
        self.message = message


class InvalidPolicy(Exception):

    def __init__(self, message='Invalid policy'):
        Exception.__init__(self)
        self.message = message


class TykInternalError(Exception):

    def __init__(self, message='It appears that tyk has problems handling your request'):
        Exception.__init__(self)
        self.message = message


class InvalidTykOperation(Exception):

    def __init__(self, message='It appears that tyk has problems handling your request'):
        Exception.__init__(self)
        self.message = message