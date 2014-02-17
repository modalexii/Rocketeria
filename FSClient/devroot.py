'''
render the development server root page...
static html with links to various things
'''

import webapp2

class DevRootHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		webcode = '''
<html>
	<head>
		<title>rockfsclient-dev</title>
	</head>
	<body>
		<style type="text/css">
			.button {
				width: 300px;
				height: auto;
				color: #FFFAF0;
				font-weight: bold;
				font-size: 1.25em;
				padding: 3px;
				cursor: pointer;
			}
		</style>
		<center>
			<h2>Welcome to the FullSlate Client Development Server!</h2>
			<form action="/static/teacherview.html">
				<input type="submit" class="button" style="background-color:#008B8B;" value="Act Like a Teacher">
			</form>
			<form action="/static/backoffice.html">
				<input type="submit" class="button" style="background-color:#FF8C00;" value="Act Like Counter Staff ">
			</form>
			<form action="/lessons">
				<input type="submit" class="button" style="background-color:#556B2F;" value="Act Like a Customer">
			</form>
			<br />
			Resources:<br />
			<a href="https://github.com/modalexii/Rocketeria">Browse Source</a>
			<br/>
			<p style="width:50%">Tread Lightly: Web services are often in disarray on this server. Expect things to misfunction!</p>
			<h5>kyle {@} rocketeria {.} biz</h5>
		</center>
	</body>
</html>
		'''
		self.response.write(webcode)

application = webapp2.WSGIApplication([
	(r'/', DevRootHandler),
], debug=False)