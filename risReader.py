class RisReader:
    def __init__(self, ris_text: str):
        self.text = ris_text
        self.ris = None

    def get_all_ris_value(self):
        if self.ris is not None:
            return self.ris
        self.ris = {}
        lines = self.text.splitlines()
        for line in lines:
            if len(line) <= 6:
                continue
            key = line[0:2]
            value = line[6:]
            if key not in self.ris:
                self.ris[key] = []
            self.ris[key].append(value)

        return self.ris

    def get_ris_value(self, key: str):
        if self.ris is None:
            self.get_all_ris_value()
        if key not in self.ris:
            return None
        return self.ris[key]

    def get_ris_value_first(self, key: str, default=''):
        values = self.get_ris_value(key)
        if values is None:
            return default
        if len(self.ris[key]) == 0:
            return default
        return self.ris[key][0]

    def v(self, key: str, default=''):
        return self.get_ris_value_first(key, default)
