from http.server import BaseHTTPRequestHandler, HTTPServer
from io import SEEK_SET
from sre_constants import SUCCESS
import json
from colorama import Cursor
from matplotlib.font_manager import json_dump
import ServerCode
global myJson

global connection
global cursor

connection = ServerCode.get_connection()
connection.autocommit = True
cursor = ServerCode.get_cursor(connection)

# Sign Up Implementation
def configureJSON_signup(signUpIsSuccessful,userAccessToken,errorMessage):
    global myJson
    myJson = json.dumps({'signUpIsSuccessful': signUpIsSuccessful, 'userAccessToken': userAccessToken, 'errorMessage': errorMessage})

def signupLogic(username,password,usertype):
    # Call function checkUserExists()
    global connection
    global cursor
    exists = ServerCode.checkUserExists(cursor,username,password)

    # Above function will return true if the username/password combo already exists in the database

    global myJson

    # If checkUserExists() returns true, return error message - signup failed 
        # configureJSON_signup(False,"-1","Error with Sign Up - Username already exists")
        # return
    if exists:
        configureJSON_signup(False,"-1","Error with Sign Up - Username already exists")
        return
    else:
        ServerCode.addUser(cursor,usertype,username,password)
        userID = ServerCode.getUserID(cursor,username,password)
        
    # If checkUserExists() returns false, INSERT new user into database
        # INSERT statement - exactly as it would be in SQL Developer
        # SELECT statement - to obtain userID of this username/password combo
        configureJSON_signup(True,userID,"")
        return

# Sign In Implementation
def configureJSON_signin(signInIsSuccessful,userAccessToken,errorMessage):
    global myJson
    myJson = json.dumps({'signInIsSuccessful': signInIsSuccessful, 'userAccessToken': userAccessToken, 'errorMessage': errorMessage})

def signinLogic(username,password):
    global connection
    global cursor
    global myJson
    exists = ServerCode.checkUserExists(cursor,username,password)
    # Above function will return true if the username/password combo already exists in the database

    # If checkUserExists() returns false, return error message - signup failed 
    if not exists:
        configureJSON_signin(False,"-1","Error with Sign In - Username/password doesn't exist")
        return
    else:
        userID = ServerCode.getUserID(cursor,username,password)
        configureJSON_signin(True,userID,"")
        return

# Send All User Data Implementation
def configureJSON_sendAllUserData(userData):
    global myJson
    # myJ = json.dumps({'userDataSentSuccessfully': userData[0], 'usertype': userData[1], 'userID': userData[2], 'username': userData[3], 'tags_rank': userData[4], 'tags_names': userData[5], 'hashedPassword': userData[6], 'errorMessage': userData[7]})
    return

def sendAllUserDataLogic(userID):
    global myJson
    userData = []
    # SELECT statement to find user with given userID in the database
    # save resullt of above statement to usertype, username, tags_rank, tags_names, hashedPassword
    # userType = 
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

# User Associated Classes Implementation
def configureJSON_UserAssociatedClasses(isSuccessful,classes,errorMessage):
    global myJson
    # classes is a list
    myJson = json.dumps({'userAssociatedClassesSuccessful:': isSuccessful, 'userClasses': classes, 'errorMessage': errorMessage})
    return

def userAssociatedClassesLogic(userID):
    global myJson
    # SELECT statement to find user with given userID in the database
    # if userID found:
        # isSuccessful = true
        # classes = list of classIDs associated with userID
        # errorMessage = ""
    # if userID not found:
        # isSuccessful = false
        # classes = []
        # errorMessage = "Error with finding User Associated Classes - UserID not found"

    # configureJSON_UserAssociatedClasses(isSuccessful,classes,errorMessage)
    return

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
        global myJson
        self.configureResponse()
        self.wfile.write(myJson.encode('utf-8'))
        return

    def do_POST(self):
        global myJson
        
        # Get length of data received
        contentLength = int(self.headers['Content-Length']) 
        
        # Get data received
        postData = self.rfile.read(contentLength) 
        clientInfo = json.loads(postData.decode('utf-8'))
       #functionRequest = str(self.path)
        functionRequest = clientInfo['path']

        if functionRequest == "/signUp":
            print("Sign up request received from client")
            print("____________________________________")
            
            signupLogic(clientInfo['username'],clientInfo['password'],clientInfo['usertype'])
            self.configureResponse()
            self.wfile.write(myJson.encode('utf-8'))

            return 
        elif functionRequest == "/signIn":
            print("Sign in request received from client")
            print("____________________________________")
            
            clientInfo = json.loads(postData.decode('utf-8'))
            signinLogic(clientInfo['username'],clientInfo['password'])
            self.configureResponse()
            self.wfile.write(myJson.encode('utf-8'))

            return
        elif functionRequest == "/sendAllUserData":
            print("Send All User Data request received from client\n")
            clientInfo = json.loads(postData.decode('utf-8'))
            sendAllUserDataLogic(clientInfo['userAccessToken'])
            self.configureResponse()
            self.wfile.write(myJson.encode('utf-8'))

            return
        elif functionRequest == "/userAssociatedClasses":
            print("User Associated Classes request received from client\n")
            clientInfo = json.loads(postData.decode('utf-8'))
            userAssociatedClassesLogic(clientInfo['userAccessToken'])
            self.configureResponse()
            self.wfile.write(myJson.encode('utf-8'))

            return  
        else:
            print("Different request received from client\n")
            print(postData)
            #myJ = json.dumps({"Most recently bought plant" : "White Princess Philodendron", "Coffee Flavor Tonight" : "Toasted Almond", "Best Tequila" : "Tears of Llorona"})
            myJson = json.dumps({"plant array" : ["White Princess Philodendron", "Pink Princess Philodendron", "Monstera Albo"], "int test":23})
            self.configureResponse()
            self.wfile.write(myJson.encode('utf-8'))

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
PORT = 8888
HOST = "192.168.1.7"
print("Welcome to the TikEdu server! You are on port {}.\n".format(PORT))
run(PORT = PORT, HOST = HOST)