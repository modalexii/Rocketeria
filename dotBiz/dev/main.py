import webapp2,logging
import templates

# debug, info, warning, error, critical
logging.getLogger().setLevel(logging.INFO)

class MainHandler(webapp2.RequestHandler):	

	def get(self):
		'''handle HTTP GETs'''

		import gae_db
		from urllib import unquote 
		
		uri = self.request.path.strip('/')
		uri = unquote(uri.encode('ascii')).decode('utf-8')
		self.response.headers['Content-Type'] = 'text/html'

		if not uri:
			uri = "index"

		self.response.write(
			templates.get("header")
		)

		print "Main handler GET request for %s" % uri 

		if uri == "index":
			try:
				# grab banner
				self.response.write(
					gae_db.fetch_content(uri = "/banner")
				)
			except AttributeError:
				# no banner
				pass

		try:
			# check the database...
			content = gae_db.fetch_content(uri = uri)
		except AttributeError:
			try:
				# ...then check the templates
				content = templates.get(uri)
			except IOError as e:
				self.response.set_status(404)
				content = templates.get("404")
				content_source = "template"
			else:
				content_source = "template"
		else:
			content_source = "db"

		self.response.write(content)

		from google.appengine.api import users
		if users.is_current_user_admin():
			current_user = users.get_current_user()
			nickname = current_user.email()
			nickname = nickname.split('@')[0] # user, no domain

			signout_url = users.create_logout_url(dest_url="/%s" % uri)

			if content_source == "db":
				seteditable = '''<script>var editable_existing = true; var new_editor = false;</script>'''
			else:
				seteditable = '''<script>var editable_existing = false; var new_editor = false;</script>'''
			self.response.write(
				templates.get("admin_bar").format(**locals())
			)

		self.response.write(
			templates.get("footer") 
		)

	def post(self):
		# for generated links
		pass

application = webapp2.WSGIApplication([
	(r'/.*', MainHandler),
], debug=False)