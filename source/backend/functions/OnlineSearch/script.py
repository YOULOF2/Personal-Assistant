for i in range(10):
    with open(f"new_file_{i}.py", "w") as file:
        file.write(
            """from source.backend.functions.baseClasses import BaseClass
from source.backend.functions.customTypes import SetMethodDict


class CLASSNAME(BaseClass):
    def __init__(self):
        super().__init__()
        all_bindings = [
            
        ]
        self._create_binding(all_bindings)"""
        )