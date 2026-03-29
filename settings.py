import ujson

class Settings:
    FILE = "settings.json"
    
    def __init__(self):
        #defaults
        self.universe = 1
        self.address = 1
        self.freq = 1000
        self.current = 1.0
        self.ssid = "No More Mr WiFi"
        self.password = "6BorderWay"
        self.ip = "192.168.68.55"
        self.subnet = "255.255.255.0"
        self.gateway = "192.168.68.1"
        self.dns = "192.168.68.1"

    def load(self):
        try:
            with open(self.FILE, "r") as f:
                data = ujson.load(f)
               
            self.universe = data.get("universe",self.universe)
            self.address = data.get("address",self.address)
            self.freq = data.get("freq",self.freq)
            self.ssid = data.get("ssid",self.ssid)
            self.current = data.get("current", self.current)
            self.password = data.get("password",self.password)
            self.ip = data.get("ip",self.ip)
            self.subnet = data.get("subnet",self.subnet)
            self.gateway = data.get("gateway",self.gateway)
            self.dns = data.get("dns",self.dns)
            
            return True
        except OSError:
            return False
        
    def save(self):
        data = {
            "universe" : self.universe,
            "address" : self.address,
            "freq" : 1000,
            "ssid": self.ssid,
            "current" : self.current,
            "password" : self.password,
            "ip" : self.ip,
            "subnet" : self.subnet,
            "gateway" : self.gateway,
            "dns" : self.dns
            }
        
        with open(self.FILE, "w") as f:
            ujson.dump(data, f)