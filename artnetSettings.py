import ujson

class ArtnetSettings:
    FILE = "artnetSettings.json"
    
    def __init__(self):
        #defaults
        self.ssid = "No More Mr WiFi"
        self.password = "6BorderWay"
        self.ip = "192.168.68.55"
        self.subnet = "255.255.255.0"
        self.gateway = "192.168.68.1"
        self.dns = "192.168.68.1"
        self.controllerip = "2.0.0.10"
        self.artnetshort = "Short"
        self.artnetlong = "Long"

    def load(self):
        try:
            with open(self.FILE, "r") as f:
                data = ujson.load(f)
               
            self.ssid = data.get("ssid",self.ssid)
            self.password = data.get("password",self.password)
            self.ip = data.get("ip",self.ip)
            self.subnet = data.get("subnet",self.subnet)
            self.gateway = data.get("gateway",self.gateway)
            self.dns = data.get("dns",self.dns)
            self.controllerip = data.get("controllerip", self.controllerip)
            self.artnetshort = data.get("artnetshort", self.artnetshort)
            self.artnetlong = data.get("artnetlong", self.artnetlong)
            
            
            return True
        except OSError:
            return False
        
    def save(self):
        data = {
            "ssid": self.ssid,
            "password" : self.password,
            "ip" : self.ip,
            "subnet" : self.subnet,
            "gateway" : self.gateway,
            "dns" : self.dns,
            "controllerip" : slef.controllerip,
            "artnetshort" : self.artnetshort,
            "artnetlong" : self.artnetlong
            }
        
        with open(self.FILE, "w") as f:
            ujson.dump(data, f)