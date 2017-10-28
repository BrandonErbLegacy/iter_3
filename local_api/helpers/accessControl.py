from local_objects.required_objects import Session

def getUserBySession(sessionID, dbSession, ip):
	"""Returns userID given a @param1: SessionID, and @param2: databaseSession
	If no valid session, returns None"""
	try:
		sessionObject = dbSession.query(Session).filter(Session.id == sessionID).one()
		if (ip == sessionObject.addressIssued):
			return sessionObject.userID
		else:
			print("Possible session hijack. IP Mismatch (%s != %s)"%(ip, sessionObject.addressIssued))
			return None
	except ArithmeticError:
		print("Encountered Error in getUserBySession")
		return None

def getPeerIP(local_node):
	"""Given a twisted connection object, return the Peer's IP addr"""
	return local_node.transport.getPeer().host
