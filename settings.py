import ujson

class Settings:
    FILE = "settings.json"
    
    def __init__(self):
        #defaults
        self.universe = 1
        self.address = 1
        self.freq = 1000
        self.current = 1.0

    def load(self):
        try:
            with open(self.FILE, "r") as f:
                data = ujson.load(f)
               
            self.universe = data.get("universe",self.universe)
            self.address = data.get("address",self.address)
            self.freq = data.get("freq",self.freq)
            self.current = data.get("current", self.current)
            
            
            return True
        except OSError:
            return False
        
    def save(self):
        data = {
            "universe" : self.universe,
            "address" : self.address,
            "freq" : 1000,
            "current" : self.current
            }
        
        with open(self.FILE, "w") as f:
            ujson.dump(data, f)