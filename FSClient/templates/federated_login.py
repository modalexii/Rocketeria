
'''
not currently in use anywhere
keeping for future need
'''

from google.appengine.api import users
user = users.get_current_user()
if user:  # signed in already
	signout_url = users.create_logout_url(dest_url='/lessons/loggedout')
	openid_auth = '''Logged in as <em>%s</em>''' % (user.nickname())

	auth_links_template = templates.get("auth_links")
	auth_links = auth_links_template.format(**locals())
else: # show authenticators
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
		provider_link_template = templates.get("openid_provider")
		openid_auth += provider_link_template.format(**locals())
		
	auth_links = "" # nothing since client is not authenticated
