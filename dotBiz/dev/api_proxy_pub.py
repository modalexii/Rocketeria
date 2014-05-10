import webapp2,logging

class APIProxyHandler(webapp2.RequestHandler):

	def get(self):
		pass

	def post(self):
		uri = self.request.path.strip('/')

		if uri == "api_proxy_pub/cc":
			import json
			from google.appengine.api import urlfetch
			from key_definitions import *

			self.response.headers["Content-Type"] = "application/json"

			self.response.write('''<html><body>Response: ''')

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

			logging.info('POST looks like: ' + post)
			
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
				self.response.write('''error''')
			else:
				if cc_response.status_code == 201:
					self.response.write('''<h2>Thanks!</h2>''')
				elif cc_response.status_code == 409:
					self.response.write('''Looks like you're already on the list! If you're not getting emails, check your Spam folder or <a href="http://visitor.r20.constantcontact.com/manage/optin/ea?v=001Vzv-UqW3G56TS4HpjB5lNw%3D%3D" target="_blank">update your profile</a>.''')
				else:
					self.response.write('''Sorry, an error occurred. Please <a href="http://visitor.r20.constantcontact.com/manage/optin/ea?v=001Vzv-UqW3G56TS4HpjB5lNw%3D%3D" target="_blank">click here to subscribe</a>''')
					logging.error("ConstantContact returned %s " % cc_response.status_code)

			self.response.write('''</body></html>''')
application = webapp2.WSGIApplication([
	(r'/api_proxy_pub/.*', APIProxyHandler),
], debug=False)