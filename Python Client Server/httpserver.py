# from http.server import HTTPServer, BaseHTTPRequestHandler
# import socketserver

# # Driver code for server
# myServer = HTTPServer(server_address=('localhost',8080), RequestHandlerClass=BaseHTTPRequestHandler)
# print("\nWelcome to the TikEdu server!\n")
# myServer.serve_forever()









# # Import libraries
# import http.server
# import socketserver
# import json
  
# # Defining PORT number
# #HOST, PORT = "192.168.1.9", 8080
# HOST, PORT = "localhost", 8080
# # Creating handle
# Handler = http.server.SimpleHTTPRequestHandler
  
# # Creating TCPServer
# http = socketserver.TCPServer((HOST, PORT), Handler)
  
# # Getting logs
# print("serving at port", PORT)

# # Get json from the client
# def getJson(messageFromClient):
#     # Convert the message from client to json
#     jsonMessage = json.loads(messageFromClient)
#     # Return the json message
#     return jsonMessage



# http.serve_forever()





from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from sre_constants import SUCCESS
import json

global myJ
myS = {'text': 'Server get request'}
myJ = json.dumps(myS)

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global myJ
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write(myJ.encode('utf-8'))
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
                #gets the json data from the client
                #str(self.path), str(self.headers), getJson(post_data.decode('utf-8')))

        myjson = json.loads(post_data.decode('utf-8'))
        print("My req is")
        #print(myjson['text'])
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, PORT=8080, HOST = "localhost"):
    logging.basicConfig(level=logging.INFO)
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        print("SUCCESS")
        httpd.serve_forever()
        print()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


from sys import argv


PORT = 8080
HOST = "192.168.1.9"
run(PORT = PORT, HOST = HOST)