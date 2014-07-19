import webapp2,logging
import templates,quote_feed

# debug, info, warning, error, critical
logging.getLogger().setLevel(logging.INFO)

class MainHandler(webapp2.RequestHandler):	

	def get_title_from_h1(self,content):
		'''
		returns the contents of the first <h1>,
		or throws IndexError if no <h1> in content
		'''
		from lxml.html import document_fromstring
		from lxml.html.clean import Cleaner

		r = document_fromstring(content)
		h1_0 = r.xpath('//h1')[0]
		h1_0 = h1_0.text_content()
		h1_0 = h1_0[:40]

		cleaner = Cleaner() # with no options, will remove most anything

		h1_0 = cleaner.clean_html(h1_0)
		h1_0 = h1_0[3:-4] # remove <p> added by lxml
		h1_0 = h1_0.encode('utf-8', 'xmlcharrefreplace')

		return h1_0

	def get(self):
		'''handle HTTP GETs'''

		import gae_db
		from urllib import unquote 
		
		uri = self.request.path.strip('/')
		uri = unquote(uri.encode('ascii')).decode('utf-8')
		self.response.headers['Content-Type'] = 'text/html'

		if not uri:
			uri = "index"

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
			#	content_source = "template"
			#else:
			#	content_source = "template"
			finally:
				content_source = "template"
		else:
			content_source = "db"

		try:
			title = self.get_title_from_h1(content)
		except IndexError:
			title = "ROCKETERIA"

		self.response.write(
			templates.get("header").format(**locals())
		)

		if uri == "index":
			try:
				# grab banner
				self.response.write(
					gae_db.fetch_content(uri = "banner")
				)
			except AttributeError:
				# no banner
				pass

			nosidebar = True
			random_quote = quote_feed.get_random()

		self.response.write(content.format(**locals()))

		try:
			nosidebar
		except UnboundLocalError:
			# drop a random quote in the sidebar before writing it out
			random_quote = quote_feed.get_random()
			self.response.write(
				templates.get("sidebar").format(**locals())
			)

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

			admin_bar = templates.get("admin_bar").format(**locals())
		else:
			admin_bar = ""

		self.response.write(
			templates.get("footer").format(**locals())
		)

	def post(self):
		# for generated links
		pass

application = webapp2.WSGIApplication([
	(r'/.*', MainHandler),
], debug=False)