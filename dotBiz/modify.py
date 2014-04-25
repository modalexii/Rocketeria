import webapp2,logging
import handle_errors,gae_db,templates

logging.getLogger().setLevel(logging.INFO)

class ModificationHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''

		request_path = self.request.path.strip('/')

		if request_path == "modify/upload":
			import cloudstorage

			self.response.write(
				templates.get("uploader")
			)

		elif request_path == "modify/new":
			from google.appengine.api import users

			if users.is_current_user_admin():
				current_user = users.get_current_user()
				nickname = current_user.nickname().split('@')[0] # user, no domain

			seteditable = '''<script>var editable_existing = false; var new_editor = true;</script>'''

			self.response.write(
				templates.get("header")
			)
			self.response.write('''<div id="editable">''')
			self.response.write(
				'''<p class="click_to_edit">Click here to begin editing...</p>'''
			)
			self.response.write('''</div> <!-- /editable -->''')
			self.response.write(
				templates.get("admin_functions").format(**locals())
			)
			self.response.write(
				templates.get("footer")
			)

		elif request_path == "modify/banner":
			self.response.write(
				templates.get("alert_banner_settings")
			)



	def post(self, *args, **kwargs):
		'''handle HTTP POSTs'''

		from urllib import quote

		request_path = self.request.path.strip('/')

		uri = self.request.get("resource")
		if uri:
			uri = uri.strip()
			if uri[0] == "/":
				uri = uri[1:]
			uri = quote(uri)

		if request_path == "modify/publish":
			content = self.request.get("content")
			key = gae_db.add_or_update_page(uri, content)
			#self.redirect("/%s" % uri.strip())

		elif request_path == "modify/delete":
			gae_db.delete_page(uri)
			logging.info("deleting uri \"%s\"" % uri)

		elif request_path == "modify/upload":
			import cloudstorage

			uploaded_file = self.request.params["file"]
			filename = quote(uploaded_file.filename)
			child_bin = self.request.get("child_bin")
			gcs_bin = "/res/"

			if child_bin:
				child_bin = child_bin.strip("/")
				child_bin = quote(child_bin)
				gcs_bin = "%s%s/" % (gcs_bin, child_bin)

			logging.info("New file upload, bin \"%s\", name \"%s\", type \"%s\"" % (gcs_bin, filename, uploaded_file.type))

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

			absolute_uri = "%s%s%s" % (self.request.host_url, gcs_bin, filename)

			self.response.write(templates.get("upload_success").format(**locals()))

		elif request_path == "modify/banner":

			state = self.request.get("state")

			if state != "on":
				# clear banner
				# THIS WILL BREAK IF THE BANNER DOES NOT EXIST - CATCH THAT
				gae_db.delete_page("/banner")
				return

			banner_bg = self.request.get("banner_bg")
			text_color = self.request.get("text_color")
			message = self.request.get("message").strip()

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

			gae_db.add_or_update_page("/banner", banner_content)




application = webapp2.WSGIApplication([
	('/modify/?.*', ModificationHandler),
], debug=False)
#application.error_handlers[404] = handle_errors.http404
#application.error_handlers[500] = handle_errors.http500