'''
render the development server root page...
static html with links to various things
'''

import webapp2

class TestHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('''<hmtl><body>''')
		import fsapi,json,pprint,clients,rockapi
		from google.appengine.api import urlfetch

		self.response.write('''
			<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
			<script>
			$(document).ready(function(){
				function send_data() {
					$.post("/api", {
						"request" : "cancel", 
						"id" : "8gUW60F2b4",
						"fsat" : "2014-03-10T16:00:00-0500"
					})	
					.done(function(data) {
						concole.log(ok);
					})
					.fail(function(textStatus, errorThrown) {
						console.log(textStatus + ': ' + errorThrown); // temp debugging measure
					});
				}

				console.log("about to send data...");
				send_data();
				console.log("should have sent data.");
			});
			</script>
			''')

		self.response.write('''</body></html>''')

application = webapp2.WSGIApplication([
	(r'/test', TestHandler),
], debug=False)