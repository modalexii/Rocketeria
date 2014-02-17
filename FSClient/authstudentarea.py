import webapp2
from google.appengine.api import users
import htmlblob

class AuthStudentHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:  # this should never happen, but just in case?
             self.redirect("/")
        self.response.headers['Content-Type'] = 'text/html'
        webcode = htmlblob.get("rocketeria-head",)
        try:
            nickname = user.nickname()
        except:
            nickname = '''<none>'''
        try:
            email = user.email()
        except:
            email = '''<none>'''
        try:
            userid = nickname.user_id()
        except:
            userid = '''<none>'''
        try:
            fid = user.federated_identity()
        except:
            fid = '''<none>'''
        try:
            fprovider = user.federated_provider()
        except:
            fprovider = '''<none>'''
        logouturl = users.create_logout_url(dest_url='/lessons/loggedout')
        webcode += ('Hello <em>%s</em>!<br/>' % (nickname))
        webcode += '''Email: %s<br/>''' % email
        webcode += '''User ID: %s<br/>''' % userid
        webcode += '''Federated Identity: %s<br/>''' % fid
        webcode += '''Federated Provider: %s<br/>''' % fprovider
        webcode += htmlblob.get("rocketeria-tail",)

        self.response.write(webcode)

application = webapp2.WSGIApplication([
	(r'/studentarea', AuthStudentHandler),
], debug=False)