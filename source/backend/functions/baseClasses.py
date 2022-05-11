from source.backend.functions.customTypes import SetMethodDict


class BaseClass:
    def __init__(self):
        self.bindings: list = []

    def _create_binding(self, *args):
        for value in args:
            if isinstance(value, list):
                for binding in value:
                    self.bindings.append(binding)
            else:
                if isinstance(value, SetMethodDict):
                    self.bindings.append(SetMethodDict)
