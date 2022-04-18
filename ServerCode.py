from colorama import Cursor
import cx_Oracle
from django.test import tag
from matplotlib.pyplot import connect, title
import config
import hashlib

def get_connection():
    #Gets a connection to the database
    return cx_Oracle.connect(config.username, config.password, config.dsn, encoding = config.encoding)

def get_cursor(connection):
    #Gets a cursor to the database
    return connection.cursor()\

def close_cursor(cursor):
    #Closes the cursor to the database
    cursor.close()

def close_connection(connection):
    #Closes the connection to the database
    connection.close()

def get_all_users(cursor):
    #Gets all users from the database
    cursor.execute("SELECT * FROM TikEdu_Users")
    return cursor.fetchall()

def getUserID(cursor, username, password):
    #Gets the userID of a user
    print("username is ", username)
    print("password is ", password)
    print()

    hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("SELECT UserID FROM TikEdu_User WHERE Username = :username AND HashedPassword = HEXTORAW(:hashedPassword)", (username, hashedPassword))
    return cursor.fetchone()[0]


def addClass(cursor, teacherID, className):
    #Adds a class to the database
    cursor.execute("INSERT INTO TikEdu_Class VALUES (Class_UserID_Array(), Class_VideoID_Array(), :teacherID, DEFAULT, :className)", (teacherID, className))

def addUser(cursor, userType, username, password):
    #Adds a user to the database
    hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("INSERT INTO TikEdu_User VALUES (:userType, DEFAULT, :username, User_TagNum_Array(), User_Tag_Array(), HEXTORAW(:hashedPassword))", (userType, username, hashedPassword))

def addVideo(cursor, video, tags, title, creatorID, isPublic, isVerified):
    # If a student adds a video then isVerified is false, if a teacher does then isVerified is true
    
    # Add the ability to save a video locally in the local file system
    beginning = "INSERT INTO TikEdu_Video VALUES (Video_Tag_Array("
    for i in tags:
        beginning += "'" + i + "',"

    beginning = beginning[:-1]
    
    # Add a video to a database
    addedList = beginning + "), :title, Video_Comment_Array(), Video_CommentUserID_Array(), :creatorID, :isPublic, 0, 0, 0, :isVerified, 0, DEFAULT)"
    cursor.execute(addedList, (title, creatorID, isPublic, isVerified))


def checkUserExists(cursor, username, password):
    #Checks if a user exists in the database
    hashedPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("SELECT * FROM TikEdu_User WHERE Username = :username AND HashedPassword = HEXTORAW(:hashedPassword)", (username, hashedPassword))
    if cursor.fetchone() is None:
        return False
    else:
        return True

## Tests the insertions, uncomment and run just this file on UF VPN

# connection = get_connection()
# connection.autocommit = True
# cursor = get_cursor(connection)

# print('Testing Insertions')

# username = "testUsername"
# password = "testPassword"
# addUser(cursor, "teacher", username, password)

# addClass(cursor, 123, "Math2")

# commenters = ["bob", "joe", "jane"]
# addVideo(cursor, None, commenters, "FirstMath Video", 123, 0, 1)

# if (checkUserExists(cursor, username, password)):
#     print(username + " exists")
# else:
#     print(username + " doesn't exists")

# username = "fakeUsername"
# password = "fakePassword"
# if (checkUserExists(cursor, username, password)):
#     print(username + " exists")
# else:
#     print(username + " doesn't exists")

# #End of file
# close_cursor(cursor)
# close_connection(connection)