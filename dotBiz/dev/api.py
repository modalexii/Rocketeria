import webapp2,logging

class APIProxyHandler(webapp2.RequestHandler):

	def get(self):
		uri = self.request.path.strip('/')

		# status is bad unless we set a different status later
		self.response.set_status(400)

		self.response.headers["Content-Type"] = "application/json"

		if uri == "api/db":
			'''
			Read database contents by uri
			'''
			import gae_db,json
			from urllib import unquote

			identifier = self.request.get("identifier")
			identifier = identifier.strip('/')
			identifier = unquote(identifier.encode('ascii')).decode('utf-8')

			try:
				# check the database...
				content = gae_db.fetch_content(uri = identifier)
			except AttributeError:
				self.response.set_status(404)
				content = {}
			else:
				self.response.set_status(200)

			content = {"content" : content}
			content = json.dumps(content)
			self.response.write(content)


	def post(self):
		uri = self.request.path.strip('/')

		if uri == "api/external/cc":
			'''
			Add an email address to the Constant Contact list specified in key_definitions
			'''
			import json
			from google.appengine.api import urlfetch
			from key_definitions import *

			self.response.headers["Content-Type"] = "application/json"

			headers = {
				"Content-Type" : "application/json",
				"Authorization" : "Bearer {cc_access_token}".format(**locals()),
			}
			url = "https://api.constantcontact.com/v2/contacts?action_by=ACTION_BY_VISITOR&api_key={cc_api_key}".format(**locals())
			email = self.request.get("email")

			post = {
				"lists": [
					{
					"id": cc_list_id
					}
				],
				"email_addresses": [
					{
					"email_address": email
					}
				]
			}

			post = json.dumps(post)
			
			try:
				cc_response = urlfetch.fetch(
					url = url,
					payload = post,
					method = urlfetch.POST,
					headers = headers,
					validate_certificate = True,
					)
			except Exception as e:
				logging.error("Error POSTing to ConstantContact: %s" % e)
				self.response.set_status(500)
			else:
				self.response.set_status(cc_response.status_code)
				if cc_response.status_code < 500:
					logging.info("ConstantContact API returned %s for %s" % (cc_response.status_code,email))
				else:
					logging.error("ConstantContact API returned %s for %s" % (cc_response.status_code,email))
				self.response.write('''{}''')


application = webapp2.WSGIApplication([
	(r'/api/.*', APIProxyHandler),
], debug=False)