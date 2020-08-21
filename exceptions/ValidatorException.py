class ValidatorException(Exception):
    errors = []
    status_code = 400

    def __init__(self, validator=None, errors=None):
        Exception.__init__(self)
        self.errors = errors if not validator else validator.errors