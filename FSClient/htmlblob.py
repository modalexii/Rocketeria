import jsblob

def get(blobname,data = None):

	if blobname == "rocketeria-head":
		webcode = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html style="height: 100%;">
<head>
	<link rel="stylesheet" type="text/css" media="all" href="/static/style/rocketeria.css"/>
	<link rel="stylesheet" type="text/css" media="all" href="/static/style/calendar.css"/>
	<link type="text/css" href="http://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
	<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
	<script type="text/javascript" src="http://fullslate.com/api.js"></script>
	<script type="text/javascript" src="/static/bookingflow.js"></script>
	<script type="text/javascript" src="/static/calendar.js"></script>
	<meta name="googlebot" content="noarchive" />
	<title>Lessons :: Rocketeria</title>
</head>
<body style="background-color: #333;" class="gradiant">
	<!--[if gte IE 9]>
		<style type="text/css">
		.gradient {
			filter: none;
		}
		</style>
	<![endif]-->

	<div class="general message">		
		<div id="header">			
			<!--<h1 id="logo-text">ROCKETERIA</h1>-->
			<img src="/static/style/rock_logo_word.png" />
		</div>	
	</div>	
	<div id="menu">		
		<ul>			
			<li>
				<li><a href="/lessons">LESSONS</a>
			</li>			
			<li>				
				<a href="#">STORE</a>			
			</li>			
			<li>				
				<a href="#">RENTALS</a>			
			</li>			
			<li>				
				<a href="#">REPAIRS</a>			
			</li>			
			<li>				
				<a href="#">EVENTS</a>			
			</li>			
			<li>				
				<a href="#">ABOUT</a>			
			</li>
			<li>				
				<a href="#">CONTACT</a>			
			</li>	
	</div>	
	<div id="main">	
				  '''

	elif blobname == "rocketeria-tail":
		webcode = '''
		</div>
	</body>
</html>
				  '''
	elif blobname == "emptycalendardiv":
		webcode = '''
				<div id="calendar">	
					&nbsp;
				</div>
				'''
	elif blobname == "myaccount":
		webcode = ''' '''

	elif blobname == "lessons-main":
		webcode = '''
		<div id="left">
			<p>Presumably, some content.</p>
			<p>Content.</p>
			<p>COOOOOOOOOOOOOOOOOOOOOOONTENT!!!!!!1!<p>
			<a href="/lessons/book">BOOK A LESSON RIGHT NOW WOW!!!1!</a>
		</div>
		<div id="right">
			<div id="openidauth">
				'''
		from google.appengine.api import users
		user = users.get_current_user()
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
			webcode += '''</div>'''
		webcode += '''
			<br/><br/><br/>This is the right side of the page and it is super cool unlike that stupid left side.
			<br/>This is the right side of the page and it is super cool unlike that stupid left side.
			<br/>This is the right side of the page and it is super cool unlike that stupid left side.
		</div>
				  '''
	elif blobname == "loggedout":
		webcode = '''
		<div id="loggedout">
			<h2>You have been logged out of Rocketeria.</h2>
			<h3>However, you are <b><u>still logged in</u></b> to the account you have linked with us!<h3>
			<p>If you are using a computer that is shared with others, you should visit the website that you've linked with Rocketeria and sign out there, too. For example, if you log in to Rocketeria with Google, go to gmail.com and log out; if you signed in with Facebook, go to facebook.com and log out, and so on.</p>
		</div>
				  '''

	return webcode