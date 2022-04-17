from http.server import BaseHTTPRequestHandler, HTTPServer
from io import SEEK_SET
from sre_constants import SUCCESS
import json
from matplotlib.font_manager import json_dump

global myJ

# Sign Up Implementation
def configureJSON_signup(signUpIsSuccessful,userAccessToken,errorMessage):
    global myJ
    myJ = json.dumps({'signUpIsSuccessful': signUpIsSuccessful, 'userAccessToken': userAccessToken, 'errorMessage': errorMessage})

def signupLogic(username,password,usertype):
    # Call function checkUserExists()
    # Above function will return true if the username/password combo already exists in the database

    # global myJ

    # If checkUserExists() returns true, return error message - signup failed 
        # configureJSON_signup(False,"-1","Error with Sign Up - Username already exists")
        # return
    # If checkUserExists() returns false, INSERT new user into database
        # INSERT statement - exactly as it would be in SQL Developer
        # SELECT statement - to obtain userID of this username/password combo
        # configureJSON_signup(True,userID,"")
        return

# Sign In Implementation
def configureJSON_signin(signInIsSuccessful,userAccessToken,errorMessage):
    global myJ
    myJ = json.dumps({'signInIsSuccessful': signInIsSuccessful, 'userAccessToken': userAccessToken, 'errorMessage': errorMessage})

def signinLogic(username,password,usertype):
    # Call function checkUserExists()
    # Above function will return true if the username/password combo already exists in the database

    # global myJ

    # If checkUserExists() returns false, return error message - signin failed 
        # configureJSON_signin(False,"-1","Error with Sign In - Given password is not associated with this username")
        # return
    # If checkUserExists() returns true, return userID
        # SELECT statement - to obtain userID of this username/password combo
        # configureJSON_signup(True,userID,"")
        return

# Send All User Data Implementation
def configureJSON_sendAllUserData(userData):
    global myJ
    # myJ = json.dumps({'userDataSentSuccessfully': userData[0], 'usertype': userData[1], 'userID': userData[2], 'username': userData[3], 'tags_rank': userData[4], 'tags_names': userData[5], 'hashedPassword': userData[6], 'errorMessage': userData[7]})
    return

def sendAllUserDataLogic(userID):
    global myJ
    userData = []
    # SELECT statement to find user with given userID in the database
    # if userID found:
        # userData.append(true) # userDataSentSuccessfully
        # userData.append(usertype) # usertype
        # userData.append(userID) # userID
        # userData.append(username) # username
        # userData.append(tags_rank) # tags_rank
        # userData.append(tags_names) # tags_names
        # userData.append(hashedPassword) # hashedPassword
        # userData.append("") # errorMessage
    # if userID not found:
        # userData.append(false) # userDataSentSuccessfully is false
        # userData.append("") # usertype
        # userData.append("") # userID
        # userData.append("") # username
        # userData.append("") # tags_rank
        # userData.append("") # tags_names
        # userData.append("") # hashedPassword
        # userData.append("Error with Send All User Data - UserID not found") # errorMessage FIXME userID? display or not? is it userid or username?
    # configureJSON_sendAllUserData(userData)
    return

class myHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def configureResponse(self):
        # Add response header to header's buffer & log accepted request
        self.send_response(200)
        # Add HTTP header to internal buffer to be written to output stream
        self.send_header('Content-type', 'text/html')
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
        
       #functionRequest = str(self.path)
        functionRequest = "diffsignup"

        if functionRequest == "signup":
            print("Sign up request received from client\n")
            clientInfo = json.loads(postData.decode('utf-8'))
            signupLogic(clientInfo['username'],clientInfo['password'],clientInfo['usertype'])
            self.configureResponse()
            self.wfile.write(myJ.encode('utf-8'))

            return 
        elif functionRequest == "signin":
            print("Sign in request received from client\n")
            clientInfo = json.loads(postData.decode('utf-8'))
            signinLogic(clientInfo['username'],clientInfo['password'],clientInfo['usertype'])
            self.configureResponse()
            self.wfile.write(myJ.encode('utf-8'))

            return
        else:
            print("Different request received from client\n")
            #myJ = json.dumps({"Most recently bought plant" : "White Princess Philodendron", "Coffee Flavor Tonight" : "Toasted Almond", "Best Tequila" : "Tears of Llorona"})
            myJ = json.dumps({"plant array" : ["White Princess Philodendron", "Pink Princess Philodendron", "Monstera Albo"]})
            self.configureResponse()
            self.wfile.write(myJ.encode('utf-8'))

        return
        
def run(server_class=HTTPServer, handler_class=myHandler, PORT=8080, HOST = "localhost"):
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()     
    except KeyboardInterrupt:
        print("\nServer Shutdown: keyboard Interrupt\nGoodbye!")
        pass
    httpd.server_close()

# Driver code for server
PORT = 8080
HOST = "localhost" #"192.168.1.9"
print("Welcome to the TikEdu server on port {}!\n".format(PORT))
run(PORT = PORT, HOST = HOST)