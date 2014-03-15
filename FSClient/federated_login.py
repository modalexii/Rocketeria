'''
"page" is content formtted to fit in #main
'''

def make_login_page(users):
	'''
	Return html representing the federated login page.
	Not aware of user authentication state - should only
	be called from make_aware_page()
	'''
	import templates
	openid_auth = '''Sign in with:<br />'''
	providers = [
		('google','https://www.google.com/accounts/o8/id'),
		('yahoo','yahoo.com'),
		('aol','aol.com'),
		('myopenid','myopenid.com'),
		# add more here
	]
	for p in providers:
		provider_name = p[0]
		provider_uri = p[1]
		provider_url = users.create_login_url(dest_url='/studentarea',federated_identity=provider_uri)
		provider_link_template = templates.get("openid_provider_stack")
		openid_auth += provider_link_template.format(**locals())

	auth_links = "" # nothing since client is not authenticated

	template = templates.get("federated_auth_page")

	return template.format(**locals())

def make_loggedin_page(federated_user):
	'''
	Return html representing the "already logged in" page.
	Not aware of user authentication state - should only be
	called from make_aware_page()
	'''
	from google.appengine.api import users
	import templates
	federated_user = users.get_current_user()
	signout_url = users.create_logout_url(dest_url='/lessons/loggedout')
	openid_auth = '''Logged in as <em>%s</em>''' % (federated_user.nickname())

	auth_links_template = templates.get("auth_links")
	auth_links = auth_links_template.format(**locals())

	template = templates.get("federated_auth_page")

	return template.format(**locals())

def make_aware_page(definatelynotloggedin=False):
	'''
	Return blob of html with federated providers and brief
	explaination, or if already logged in, say so and offer
	logout link
	'''
	if definatelynotloggedin:
		webcode = make_login_page
	else:
		from google.appengine.api import users
		federated_user = users.get_current_user()
		try:
			webcode = make_loggedin_page(federated_user)
		except AttributeError:
			# hopefully because federated_user is None
			webcode = make_login_page(users)

	return webcode


'''
"bar" is content formatted to fit in a bar under the header
'''

def make_login_bar(users):
	'''
	Return html representing the federated login bar.
	Not aware of user authentication state - should only
	be called from make_aware_bar()
	'''
	import templates
	openid_auth = '''Hello anonymous user! To book lessons, sign in with your existing account at: &nbsp;'''
	providers = [
		('google','https://www.google.com/accounts/o8/id'),
		('yahoo','yahoo.com'),
		('aol','aol.com'),
		('myopenid','myopenid.com'),
		# add more here
	]
	for p in providers:
		provider_name = p[0]
		provider_uri = p[1]
		provider_url = users.create_login_url(dest_url='/lessons/book',federated_identity=provider_uri)
		provider_link_template = templates.get("openid_provider_inline")
		openid_auth += provider_link_template.format(**locals())

	openid_auth += '''<a href="/lessons/login">&nbsp;&nbsp;<img src="/static/style/help.png"> What is this?</a>'''

	auth_links = "" # nothing since client is not authenticated

	template = templates.get("federated_auth_bar")

	return template.format(**locals())

def make_loggedin_bar(federated_user):
	'''
	Return html representing the "already logged in" bar.
	Not aware of user authentication state - should only be
	called from make_aware_bar()
	'''
	from google.appengine.api import users
	import templates
	federated_user = users.get_current_user()
	signout_url = users.create_logout_url(dest_url='/lessons/loggedout')
	openid_auth = '''Logged in as <em>%s</em>''' % (federated_user.email())

	auth_links_template = templates.get("auth_links")
	auth_links = auth_links_template.format(**locals())

	template = templates.get("federated_auth_bar")

	return template.format(**locals())

def make_aware_bar(definatelynotloggedin=False):
	'''
	Return blob of html with federated providers and brief
	explaination, or if already logged in, say so and offer
	logout link
	'''
	if definatelynotloggedin:
		webcode = make_login_bar
	else:
		from google.appengine.api import users
		federated_user = users.get_current_user()
		try:
			webcode = make_loggedin_bar(federated_user)
		except AttributeError:
			# hopefully because federated_user is None
			webcode = make_login_bar(users)

	return webcode