from google.appengine.api import users

class CurrentUser():
	self = users.get_current_user()
