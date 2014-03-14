import webapp2

class LessonsHandler(webapp2.RequestHandler):

	def get(self, *args, **kwargs):
		'''handle HTTP GETs'''
		import htmlblob,templates
		from google.appengine.api import users
		self.response.headers['Content-Type'] = 'text/html'
		webcode = templates.get("rocketeria-head",)

		try:
			path = args[0]
		except IndexError:
			path = ""
		if "book" in path:
			import fsapi,services,employees
			import json
			# pull services from FS
			serviceobj = fsapi.apirequest('services')

			serviceobj = serviceobj.content
			serviceobj = json.loads(serviceobj)
			
			# pull & format employees from service object
			employeeobj = fsapi.apirequest('employees')
			employeeobj = employeeobj.content
			employeeobj = json.loads(employeeobj)
						
			webcode += services.gethtml(serviceobj)
			webcode += employees.gethtml(employeeobj)
			webcode += templates.get('booking_placeholders')
			
			#webcode += htmlblob.get("book")
		elif "loggedout" in path:
			webcode += templates.get("loggedout")
		else:

			from google.appengine.api import users
			user = users.get_current_user()
			if user:  # signed in already
				signout_url = users.create_logout_url(dest_url='/lessons/loggedout')
				openid_auth = '''Logged in as <em>%s</em>''' % (user.nickname())

				auth_links_template = templates.get("auth_links")
				auth_links = auth_links_template.format(**locals())
			else: # show authenticators
				openid_auth = '''Sign in with:<br />'''
				providers = [
					('google','https://www.google.com/accounts/o8/id'),
					('yahoo','yahoo.com'),
					('aol','aol.com'),
					('myopenid','myopenid.com'),
					# add more here
				]
				for p in providers:
					provider_name = p[0]
					provider_uri = p[1]
					provider_url = users.create_login_url(dest_url='/studentarea',federated_identity=provider_uri)
					provider_link_template = templates.get("openid_provider")
					openid_auth += provider_link_template.format(**locals())
					
				auth_links = "" # nothing since client is not authenticated

			lessons_template = templates.get("lessons")
			webcode += lessons_template.format(**locals())
		webcode += templates.get("rocketeria-tail")
		self.response.write(webcode) 

application = webapp2.WSGIApplication([
	(r'/lessons', LessonsHandler),
	webapp2.Route(r'/lessons/<:.*>', LessonsHandler),
], debug=False)