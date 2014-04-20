import webapp2,logging
import templates,handle_errors

# debug, info, warning, error, critical
logging.getLogger().setLevel(logging.INFO)

class MainHandler(webapp2.RequestHandler):	

	def get(self):
		'''handle HTTP GETs'''

		import gae_db
		from urllib import quote

		uri = self.request.path.strip('/')
		uri = quote(uri)
		self.response.headers['Content-Type'] = 'text/html'

		if not uri:
			uri = "index"

		self.response.write(
			templates.get("header")
		)

		try:
			# check the database...
			content = gae_db.fetch_content(uri = uri)
		except AttributeError:
			try:
				# ...then check the templates
				content = templates.get(uri)
			except IOError as e:
				handle_errors.http404(self.request, self.response)
				return
			else:
				content_source = "template"
				self.response.write('''<div id="editable">''')
		else:
			content_source = "db"
			self.response.write('''<div id="editable">''')

		self.response.write(content)
		self.response.write('''</div> <!-- /editable -->''')

		from google.appengine.api import users
		if users.is_current_user_admin():
			current_user = users.get_current_user()
			nickname = current_user.nickname()
			nickname = nickname.split('@')[0] # user, no domain
			signout_url = users.create_logout_url(dest_url="/%s" % uri)

			if content_source == "db":
				seteditable = '''<script>var editable_existing = true; var new_editor = false;</script>'''
			else:
				seteditable = '''<script>var editable_existing = false; var new_editor = false;</script>'''
			self.response.write(
				templates.get("admin_functions").format(**locals())
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

#application.error_handlers[404] = handle_errors.http404()
#application.error_handlers[500] = handle_errors.http500()