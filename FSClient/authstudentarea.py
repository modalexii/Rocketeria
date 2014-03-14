import webapp2

class AuthStudentHandler(webapp2.RequestHandler):
    def get(self):
        from google.appengine.api import users

        federated_user = users.get_current_user()
        if not federated_user:  # this should never happen, but just in case?
             self.redirect("/")

        import htmlblob,templates,events,clients,ranges,fs_datetime

        num_weeks = 3 # how many weeks to draw at a time

        self.response.headers['Content-Type'] = 'text/html'
        webcode = templates.get("rocketeria-head")

        federated_nick = federated_user.nickname()
        federated_email = federated_user.email()
        logouturl = users.create_logout_url(dest_url='/lessons/loggedout')

        webcode += '''<p>'''
        webcode += 'Hello <em>%s</em>! ' % (federated_nick)
        webcode += ''' [<a href="%s">Sign Off</a>]''' % logouturl
        webcode += '''</p>'''
        webcode += '''<p><div id="booknow_link">Book A Lesson</div></p><hr/>'''

        fs_client = clients.fs_client_from(federated_email)
        rock_client = clients.RockClient(fs_client,federated_user)

        if fs_client:
            eventlist = []

            fs_range = ranges.getfsrange(offset=0,num_weeks=num_weeks) # always num_weeks=1
            #print "\n\nFS_RANGE FROM AUTHSTUDENTAREA: ",fs_range
        
            events_attended = rock_client.events_attended(fs_range)
            #print "\n\nEVENTS_IN_RANGE #%s from AUTHSTUDENTAREA: " % n,events_in_range

            webcode += '''              <div id="calendar"> '''
            webcode += events.makecal(eventlist=events_attended,num_weeks=num_weeks,labels="existing")
            #webcode += '''              </div> ''' # aah there is an extra div somewhere in makecal() fix this shiiiit

        webcode += templates.get("rocketeria-tail")

        self.response.write(webcode)

application = webapp2.WSGIApplication([
	(r'/studentarea', AuthStudentHandler),
], debug=False)