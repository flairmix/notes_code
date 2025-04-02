import ifcopenshell

class IFCLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.model = None

    def load(self):
        self.model = ifcopenshell.open(self.file_path)
        return self.model

    def reload(self):
        return self.load()