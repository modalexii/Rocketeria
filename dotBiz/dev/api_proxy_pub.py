import webapp2,logging

class APIProxyHandler(webapp2.RequestHandler):

	def get(self):
		'''
		The only reason a user would GET this handler is if JS is disabled on a JS-only form.
		Display a decent page with some suggestions and JS-free links.
		'''
		import templates
		self.response.write(
			templates.get("header")
		)
		self.response.write(
			templates.get("noscript-formsubmit")
		)
		self.response.write(
			templates.get("footer")
		)

	def post(self):
		uri = self.request.path.strip('/')

		if uri == "api_proxy_pub/cc":
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
	(r'/api_proxy_pub/.*', APIProxyHandler),
], debug=False)