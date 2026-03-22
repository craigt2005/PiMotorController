import socket
from led_tape import TapeController

#some bollocks

class WebServer:
    def __init__(self, wlan, tape_controller: TapeController):
        self.wlan = wlan  
        self.tape_controller = tape_controller  
        print("WebServer V6")


    def serve_file(self, path):
        try:
            with open(path, "rb") as f:
                
                #substitute current values
                body = f.read().decode()
                
                #substitute network data
                config = self.wlan.ifconfig()
                
                body = body.replace("#IP#",config[0])
                body = body.replace("#SUBNET#",config[1])
                body = body.replace("#GATEWAY#",config[2])
                body = body.replace("#DNS#",config[3])
                
                return body.encode("utf-8")
        except Exception as err:
            print(err)
            return err
        

        # ---- Parse query string into dict ----
    def parse_query(self, qs):
        params = {}
        if not qs:
            return params
        pairs = qs.split("&")
        for p in pairs:
            if "=" in p:
                k, v = p.split("=", 1)
                params[self.unquote(k)] = self.unquote(v)
        return params


    def unquote(self, s):
        s = s.replace('+', ' ')
        out = ''
        i = 0
        while i < len(s):
            if s[i] == '%' and i+2 < len(s):
                out += chr(int(s[i+1:i+3], 16))
                i += 3
            else:
                out += s[i]
                i += 1
        return out

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return r, g, b

    def webServerTask(self):
        global mode
        global Colour1
        global Colour2
        
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        print("Web server listening on http://%s:%d" % addr)

        while True:
            cl, addr = s.accept()
            print('Client connected from', addr)
            
            
            
            request = cl.recv(1024).decode('utf-8')
            print('Request:')
            print(request)

            # Parse HTTP request
            
            request_line = request.split('\r\n')[0]
            
            try:
                method, path, _ = request_line.split()
            except Exception as err:
                print(err)
                cl.close()
                continue

            # Handle query parameters
            if '?' in path:
                path, qs = path.split('?', 1)
                params = self.parse_query(qs)
            else:
                params = {}

            # Handle different paths
            if path == '/':
                response = self.serve_file('index.html')
                cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n')
                cl.send(response)
            
            elif path == "/favicon.ico":
                cl.send("HTTP/1.1 204 No Content\r\n\r\n")
                #cl.close()
                #continue


            elif path == '/setmode':
                if 'mode' in params:
                    self.tape_controller.set_mode(params['mode'])
                    print('Mode set to:', params['mode'])
                    cl.send("HTTP/1.1 204 No Content\r\n\r\n")
            
            elif path == '/set_color1':
                if 'rgb' in params:
                    self.tape_controller.set_color1(self.hex_to_rgb(params['rgb']))
                    #print('Colour1 set to:', Colour1)
                    cl.send("HTTP/1.1 204 No Content\r\n\r\n")
            elif path == '/set_color2':
                if 'rgb' in params:
                    self.tape_controller.set_color2(self.hex_to_rgb(params['rgb']))
                    #print('Colour2 set to:', Colour2)
                    cl.send("HTTP/1.1 204 No Content\r\n\r\n")
            
            elif path == '/stop':
                if 'color' in params:
                    print('Stopping')
                    cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nColour2 set to ' + str(Colour2))
                    break
            



            else:
                response = b"404 Not Found"
                cl.send('HTTP/1.0 404 Not Found\r\nContent-Type: text/plain\r\n\r\n')
                cl.send(response)

            cl.close()
