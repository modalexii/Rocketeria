import webapp2,logging
import gae_db,templates

logging.getLogger().setLevel(logging.INFO)

class ModificationHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''

		self.response.headers['Content-Type'] = 'text/html'
		request_path = self.request.path.strip('/')

		from google.appengine.api import users
		current_user = users.get_current_user()
		nickname = current_user.email()

		if not users.is_current_user_admin():
			logging.error("SECURITY: non-admin user %s requested %s" % (nickname, request_path))
			return
		else:
			logging.info("User %s sent GET request for %s" % (nickname, request_path))

		if request_path == "modify/upload":
			import cloudstorage

			content = templates.get("uploader").format(**locals())

			self.response.write(
				templates.get("upload_wrap").format(**locals())
			)

		elif request_path == "modify/new":

			current_user = users.get_current_user()
			nickname = current_user.email()

			seteditable = '''<script>var editable_existing = false; var new_editor = true;</script>'''
			title = "New Page"
			
			self.response.write(
				templates.get("header").format(**locals())
			)
			self.response.write(
				templates.get("header-sub")
			)
			self.response.write('''<div id="content_sub" contenteditable>''')
			self.response.write(
				'''
				<p>Click here to begin editing...</p>
				<p>Remember to change the page title above. Click the background of the title to cycle colors. Before clicking &quot;Save&quot; below, enter the desired URL in the &quot;Save to&quot; field. The page URL does not have to match the page title above.</p>
				<p>Consult the <a href="https://docs.google.com/a/rocketeria.biz/document/d/161u3MvfQGBfpvJJqEpcVHPntjfqvizoCDssJQLySAEc/edit?usp=sharing" target="_blank">Content Author's Manual</a> for further guidance.</p>
				'''
			)
			self.response.write('''</div> <!--End of #content_sub -->''')

			random_quote = "This text replaces Quote Feed content when creating a new page. Please disregard."
			self.response.write(
				templates.get("sidebar").format(**locals())
			)

			admin_bar = templates.get("admin_bar").format(**locals())

			self.response.write(
				templates.get("footer").format(**locals())
			)

		elif request_path == "modify/banner":
			self.response.write(
				templates.get("alert_banner_settings")
			)
		elif request_path == "modify/info":
			from google.appengine.api import users
			import get_env
			environment = get_env.from_url(self.request.url)
			version = get_env.version()
			current_user = users.get_current_user()
			nickname = current_user.email().split('@')[0] # user, no domain
			self.response.write(
				templates.get("info").format(**locals())
			)
		elif request_path == "modify/logout":
			from google.appengine.api import users
			self.redirect(users.create_logout_url('/'))

	def post(self, *args, **kwargs):
		'''handle HTTP POSTs'''

		from google.appengine.api import users
		current_user = users.get_current_user()
		nickname = current_user.email()

		if not users.is_current_user_admin():
			logging.error("SECURITY: non-admin user %s requested %s" % (nickname, request_path))
			return

		self.response.headers['Content-Type'] = 'text/html'

		request_path = self.request.path.strip('/')

		logging.info("User %s sent POST request for %s" % (nickname, request_path))

		uri = self.request.get("resource")
		if uri:
			uri = uri.strip()
			uri = uri.strip("/")

		if request_path == "modify/publish":
			content = self.request.get("content")
			key = gae_db.add_or_update_page(uri, content)
			logging.info("User %s published %s" % (nickname, uri))
			self.redirect("/%s" % uri)

		elif request_path == "modify/delete":
			logging.info("User %s deleted %s" % (nickname, uri))
			gae_db.delete_page(uri)

		elif request_path == "modify/upload":
			import cloudstorage

			uploaded_file = self.request.params["file"]
			filename = uploaded_file.filename
			child_bin = self.request.get("child_bin")
			gcs_bin = "/dres/"

			if child_bin:
				child_bin = child_bin.strip("/")
				child_bin = child_bin
				gcs_bin = "%s%s/" % (gcs_bin, child_bin)

			logging.info("User %s uploaded file \"%s\", type \"%s\", to bin \"%s\"" % (nickname, filename, uploaded_file.type, gcs_bin))

			cloud_file = cloudstorage.open(
				"%s%s" % (gcs_bin, filename),
				mode = "w",
				content_type = uploaded_file.type,
				options = {
					"x-goog-acl" : "public-read" 
				}
			)
			cloud_file.write(uploaded_file.value)
			cloud_file.close()

			from urllib import quote
			uri = quote(uri.encode('utf-8'))

			absolute_uri = "%s%s%s" % (self.request.host_url, gcs_bin, filename)

			content = templates.get("upload_success").format(**locals())

			self.response.write(
				templates.get("upload_wrap").format(**locals())
			)

		elif request_path == "modify/banner":

			state = self.request.get("state")

			if state != "on":
				# clear banner
				logging.info("User %s removed the alert banner" % (nickname))
				gae_db.delete_page("banner")
				return

			banner_bg = self.request.get("banner_bg")
			text_color = self.request.get("text_color")
			message = self.request.get("message").strip()
			override_hours = self.request.get("override_hours").strip()

			# set expire date to 00:00 UTC of selected day
			# this prevents each cron job fron needing to convert time zone
			from datetime import datetime,timedelta
			expiry = self.request.get("expire").strip()

			if expiry:
				expiry = datetime.strptime(expiry,"%d/%m/%Y")
				offset = timedelta(hours = 5) # one hr off during DST is acceptable for this application
				expiry += offset
				expiry = expiry.strftime("%d/%m/%YT05:00:00")

			style_class = "%s %s" % (banner_bg, text_color)

			# we trust user input here. they're already admins...

			banner_content = templates.get("alert_banner").format(**locals())
			if override_hours:
				banner_content = "<script>var override_hours = '{override_hours}';</script>{banner_content}".format(**locals())

			logging.info("User %s published alert banner reading \"%s\"" % (nickname, message))
			gae_db.add_or_update_page("banner", banner_content)




application = webapp2.WSGIApplication([
	('/modify/?.*', ModificationHandler),
], debug=False)