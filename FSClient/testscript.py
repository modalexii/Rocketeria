import webapp2

class TestHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('''<hmtl><body>''')
		import fsapi,json

		post = {
		#"auth" : "aDbvS9DsQowbPhs9dfDxtEqsLCyZuVH9eaKHLtTsWLOpFe2wEq",
		"company" : {
			"key" : "rocketeria2",
			#"events" : [{ "id" : "u8c3gOQDo4", "deleted" : True}],
			},
		}

		post = json.dumps(post)

		#self.response.write("Cancelling event u8c3gOQDo4...<br/>")

		fs_response = fsapi.apirequest(resource = 'manage/company', post = post, fs_server = "app", apiroot = "api")

		self.response.write("FullSlate API replied: " + fs_response.content)

		self.response.write('''</body></html>''')

application = webapp2.WSGIApplication([
	(r'/test', TestHandler),
], debug=False)