from typing import Union
import inspect


class _TypeMisMatchError(Exception):
    pass


class SetMethodDict:
    """
    Customised replacement for the built-in dict and can have sets as key pairs
    """
    def __init__(self, key_set: Union[list, str], method, **method_kwargs):
        if isinstance(key_set, list):
            self.key = set(key_set)
        else:
            self.key = set(key_set.split(" "))
        self.method = method
        self.method_kwargs = method_kwargs

    def __repr__(self):
        return "{\n" + f"{self.key} : {self.method}" + "\n}"

    def __str__(self):
        return "{\n" + f"{self.key} : {self.method}" + "\n}"

    def __eq__(self, other):
        if not isinstance(other, SetMethodDict):
            raise _TypeMisMatchError("Can not compare instance of SetValueDict and other")

        if (self.key == other.key) & (self.method == other.method):
            return True
        return False

    def export(self):
        return {
            " ".join(self.key): inspect.getsource(self.method),
            "kwargs": self.method_kwargs
        }

