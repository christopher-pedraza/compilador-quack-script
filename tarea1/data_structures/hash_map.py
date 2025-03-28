class HashMap:
    def __init__(self):
        self.map = {}

    def put(self, key, value):
        self.map[key] = value

    def get(self, key):
        return self.map.get(key, None)

    def remove(self, key):
        if self.contains_key(key):
            del self.map[key]

    def contains_key(self, key):
        return key in self.map

    def size(self):
        return len(self.map)
    
    def get_keys(self):
        return list(self.map.keys())
    
    def get_values(self):
        return list(self.map.values())
    
    def __str__(self):
        return str(self.map)