from local_api.network.twisted_promises import Promises, Promise
from local_objects.required import User, Session
from local_api.file.dbobjects import GlobalDatabaseHandler
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from getpass import getpass
from hashlib import sha256
from functools import update_wrapper, partial


class Iter_3_Authenticate(Promise):
    def clientAction(self, **kw):
        username = kw["username"]
        password = kw["password"]
        success = kw["success"]
        fail = kw["fail"]
        user = User()
        user.username = username
        user.password = password
        self._register.executeRemotePromise("Iter_3_Authenticate")
        self._register.sendData("USER_CREDENTIAL", user)
        print("Sent credential")

        def authentication(result):
            print("Got result, ", result)
            if result == False:
                fail()
            else:
                self._register.addEnvironmentVariable("AUTHENTICATION_SESSION_ID", result)
                success(result)

        self._register.fetchDataFromBuffer("USER_CREDENTIAL", authentication)
        print("Waiting for result")

    def serverAction(self, **kw):
        local_node = kw["NODE"]
        #Received User object from clientAction
        #Check if User object username/password matches
        #If so, issue a session ID to the client/IP pair
        #otherwise issue a False return value

        def issueNewSessionID(userObject, dbSession):
            userSession = Session()
            userSession.id = str(uuid4())
            userSession.userID = userObject.id
            userSession.addressIssued = ""
            GlobalDatabaseHandler.addObject(userSession, dbSession)
            GlobalDatabaseHandler.saveSession(dbSession)
            local_node.sendData("USER_CREDENTIAL", userSession.id)

        def process(data):
            session = GlobalDatabaseHandler.createNewSession()
            try:
                result = session.query(User).filter_by(username=data.username).one()
                localPass = sha256((result.salt+data.password).encode("utf-8")).hexdigest()
                if localPass == result.password:
                    issueNewSessionID(result, session)
                else:
                    local_node.sendData("USER_CREDENTIAL", False)
            except NoResultFound:
                local_node.sendData("USER_CREDENTIAL", False)


        local_node.fetchDataFromBuffer("USER_CREDENTIAL", process)

class Iter_3_Create_User(Promise):
    def commandLineAction(self, **kw):
        username = input("Please enter the desired username: ")
        password = getpass("Please enter the desired password: ")
        user = User()
        user.username = username
        user.salt = str(uuid4())
        user.password = sha256((user.salt+password).encode("utf-8")).hexdigest()
        user.id = str(uuid4())
        dbSession = GlobalDatabaseHandler.createNewSession()
        GlobalDatabaseHandler.addObject(user, dbSession)
        GlobalDatabaseHandler.saveSession(dbSession)
        print("Successfully created user!")

class Iter_3_Authenticate_Session_ID(Promise):
    def clientAction(self, **kw):
        sessionID =  self._register.getEnvironmentVariable("AUTHENTICATION_SESSION_ID")
        success = kw["success"]
        fail = kw["fail"]
        def valid(returnVal):
            print("Received: ", returnVal)
            if returnVal:
                success()
            else:
                fail()

        self._register.sendData("AUTHENTICATION_SESSION_ID", sessionID)
        print("Sent ID")
        self._register.fetchDataFromBuffer("AUTHENTICATION_SESSION_ID_SUCCESS", valid)
        print("Waiting for success")

    def serverAction(self, **kw):
        local_node = kw["NODE"]

        def validateSessionID(sessionID):
            print("Sending success.")
            local_node.sendData("AUTHENTICATION_SESSION_ID_SUCCESS", True)

        local_node.fetchDataFromBuffer("AUTHENTICATION_SESSION_ID", validateSessionID)
        print("Waiting for session ID")

class AuthenticatePromise(object):
    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return partial(self.__call__, obj)

    def __call__(self, obj, *args, **kwargs):

        try:
            local_node = kwargs["NODE"]
        except KeyError:
            local_node = None
            #This indicates it's client and we don't need to pass the NODE
        def success():
            print("Authentication success!")
        def fail():
            print("Authentication failure!")
        if local_node:
            Promises.execute("Iter_3_Authenticate_Session_ID", NODE=local_node, success=success, fail=fail)
        else:
            Promises.execute("Iter_3_Authenticate_Session_ID", success=success, fail=fail)
        returnVal = self.func(obj, **kwargs)
        #return returnVal



Promises.register(Iter_3_Authenticate())
Promises.register(Iter_3_Create_User())
Promises.register(Iter_3_Authenticate_Session_ID())
