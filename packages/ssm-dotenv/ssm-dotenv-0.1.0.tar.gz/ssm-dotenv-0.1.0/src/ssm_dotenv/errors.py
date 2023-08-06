
class ParamSchemaValidationError(Exception):
    def __init__(self, message=None, errors=[]):
        super(ParamSchemaValidationError, self).__init__(message)
        self.errors = errors


class ParamCreateError(Exception):
    pass


class ParamDeleteError(Exception):
    pass


class SchemaConfigError(Exception):
    pass

