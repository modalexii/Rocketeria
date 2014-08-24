import webapp2

class AuthenticationHandler(webapp2.RequestHandler):

	def get(self):
		from google.appengine.api import users
		login_url = users.create_login_url(dest_url="/",federated_identity="https://www.google.com/accounts/o8/id")

		self.redirect(login_url)


application = webapp2.WSGIApplication([
	(r'/enableadmin', AuthenticationHandler),
], debug=False)