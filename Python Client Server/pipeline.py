from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
HOST = "192.168.1.7"
PORT = "8888"
URL = 'http://' + HOST + ':' + PORT

#r = requests.post(URL, json={'username': 'DogeLearner37', 'password': 'testPassword','usertype':'Teacher'})
#print("request sent")
#print(r.json())
#print(type(r.json()['int test']))
#r = requests.get(URL)
#print(r.text)

class myHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def configureResponse(self):
        # Add response header to header's buffer & log accepted request
        self.send_response(200)
        # Add HTTP header to internal buffer to be written to output stream
        self.send_header('Content-type', 'text/html') #FIXME TRY DIFFERENT INPUTS TO THIS FXN HERE TO BE DIFFERENT/MORE SPECIFIC
        # Indicate end of HTTP headers in response and send to output stream
        self.end_headers()
        return

    def do_GET(self):
        global myJ
        self.configureResponse()
        self.wfile.write(myJ.encode('utf-8'))
        return

    def do_POST(self):
        global myJ
        
        # Get length of data received
        contentLength = int(self.headers['Content-Length']) 
        
        # Get data received
        postData = self.rfile.read(contentLength) 
        print("postData: |||" + postData.decode('utf-8') + "|||")
        
        functionRequest = str(self.path)
        print("functionRequest: |" + functionRequest + "|")
        #functionRequest = "diffsignup"
        clientInfo = json.loads(postData.decode('utf-8'))

        if functionRequest == "/signUp":
            print("Sign up request received from client\n")
            r = requests.post(URL, json.dumps({'path' : functionRequest, 'username': clientInfo['username'], 'password': clientInfo['password'], 'usertype': clientInfo['usertype']}))
        elif functionRequest == "/signIn":
            print("Sign in request received from client\n")
            r = requests.post(URL, json.dumps({'path' : functionRequest, 'username': clientInfo['username'], 'password': clientInfo['password']}))

        print("Data sent from backend to frontend.")
        print("Sent JSON = " + str(r.json()))

        self.configureResponse()
        self.wfile.write(json.dumps(r.json()).encode('utf-8')) 

        return
        
def run(server_class=HTTPServer, handler_class=myHandler, PORT=8080, HOST = "localhost"):
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()     
    except KeyboardInterrupt:
        print("\nServer Shutdown: Keyboard Interrupt\nGoodbye!")
        pass
    httpd.server_close()


# Driver code for server
PORT = 8080
HOST = "192.168.1.9"
print("Welcome to the TikEdu server! You are on port {}.\n".format(PORT))
run(PORT = PORT, HOST = HOST)