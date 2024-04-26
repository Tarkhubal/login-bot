import json

class Configs:
    def __init__(self, f) -> None:
        self.f = f
        self.load()

    def load(self):
        self._raw: dict = json.load(open(self.f, "r", encoding="utf-8"))
        
        self.token = self._raw["TOKEN"]
        self.dev_token = self._raw["DEVTOKEN"]
        self.dev_mode_is_activated = self._raw["dev_mode_is_activated"]
        self.db = self.database_name = self._raw["database_name"]
        self.version = self._raw["version"]
        self.prefix = self._raw["prefix"]
        self.database_url = self._raw["database_url"]
        self.owners = self._raw["owners"]

    def update(self):
        self.load()

    def __getitem__(self, key):
        return self._raw[key]
    
    def __setitem__(self, key, value):
        self._raw[key] = value
        json.dump(self._raw, open(self.f, "w", encoding="utf-8"), indent=4)

    def __delitem__(self, key):
        del self._raw[key]
        json.dump(self._raw, open(self.f, "w", encoding="utf-8"), indent=4)

    def __iter__(self):
        return iter(self._raw)
    
    def __len__(self):
        return len(self._raw)
    
    def __str__(self):
        return str(self._raw)
    
    def __repr__(self):
        return repr(self._raw)
    
    def __contains__(self, item):
        return item in self._raw
    
    def __eq__(self, other):
        return self._raw == other
    


    def keys(self):
        return self._raw.keys()
    
    def values(self):
        return self._raw.values()
    
    def items(self):
        return self._raw.items()
    
    def get(self, key, default=None):
        return self._raw.get(key, default)
    