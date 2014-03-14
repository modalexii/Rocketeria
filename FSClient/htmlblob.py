import jsblob

def get(blobname,data = None):

	'''
	everything here needs to be moved to the new templating system
	this script will be obsolete soon
	'''
	

	if blobname == "federated_login":
		from google.appengine.api import users
		user = users.get_current_user()
		webcode = '''<div id="openidauth">'''
		if user:  # signed in already
			signouturl = users.create_logout_url(dest_url='/lessons/loggedout')
			webcode += '''Logged in as <em>%s</em>''' % (user.nickname())
			webcode += '''
			<a href="/studentarea">
				<img src="/static/style/studentarea.png" />
				Student Area
			</a>
			<br />
					   '''
			webcode += '''<a href="%s">''' % (signouturl)
			webcode += '''
							<img src="/static/style/logoff.png" />
							Sign Out
						</a>
					   '''
		else: # show authenticators
			webcode += '''Sign in with:<br />'''
			providers = [
				('google','https://www.google.com/accounts/o8/id'),
				('yahoo','yahoo.com'),
				('aol','aol.com'),
				('myopenid','myopenid.com'),
				# add more here
			]
			for p in providers:
				name = p[0]
				uri = p[1]
				url = users.create_login_url(dest_url='/studentarea',federated_identity=uri)
				webcode += '''
				<a class="openidauth" href="%s">
					<img src="/static/style/openidimg/%s.png" />
				</a>''' % (url,name)
		webcode += '''<p><b>What is this?</b> By linking your use of this site with one of the above sites, you (the customer) are 
		relieved of needing to remember yet another username and psssword, and we (the web site operators) are 
		revlieved of having to manage usernames and passwords ourselves. It's safer and easier for everyone. The 
		service that you choose to link with us will share only your email address - we can't see any other
		info or use your account in any way.</p>'''
		webcode += '''</div>'''


	return webcode