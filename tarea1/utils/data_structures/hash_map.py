from copy import deepcopy

class HashMap:
    def __init__(self):
        self.map = {}

    def put(self, key, value):
        self.map[key] = value

    def get(self, key):
        return self.map.get(key, None)

    def remove(self, key):
        if self.contains_key(key):
            item = self.map[key]
            del self.map[key]
            return item
        return None

    def contains_key(self, key):
        return key in self.map

    def size(self):
        return len(self.map)
    
    def get_keys(self):
        return list(self.map.keys())
    
    def get_values(self):
        return list(self.map.values())
    
    def copy(self):
        new_hash_map = HashMap()
        new_hash_map.map = deepcopy(self.map)
        return new_hash_map
    
    def __str__(self):
        return str(self.map)