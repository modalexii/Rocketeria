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
	<script type="text/javascript" src="/static/bookingflow.js"></script>
	</body>
</html>
				  '''
	elif blobname == "emptycalendardiv":
		webcode = '''
				<div id="cconfirmation">
				</div>
				<div id="calendar">
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
	elif blobname == "client_info_form":
		'''
		Prefill what we know, set explanatory values for anything missing
		DATA is an instance of clients.RockClient(client_info_source="fullslate")

		THIS SHOULD BE MOVED SOMEWHERE ELSE - TOO MUCH PROCESSING FOR BLOB
		'''
		import clients

		rock_client = data

		try:
			first_name = rock_client.first_name
			last_name = rock_client.last_name
		except AttributeError:
			first_name = last_name = ""
		else:
			unpacked_names = clients.unPack_family_names((first_name,last_name))

		try:
			phone_numbers = rock_client.phone_numbers
			# can only update primary phone here
			#print "PHONE_NUMBERS FROM HTMLBLOB GET account_info_form: ",phone_numbers
		except AttributeError:
			phone_number = ""
		else:
			for p in phone_numbers:
				if p["position"] == 1:
					phone_number = p["number"]

		email = rock_client.email # there will always be an email

		try:
			addresses = rock_client.addresses
			#print "ADDRESES FROM HTMLBLOB GET account_info_form: ",addresses
		except AttributeError:
			street1 = street2 = city = state = postal_code = ""
		else:
			for a in addresses:
				if a["position"] == 1:
					try:
						street1 = a["street1"]
					except KeyError:
						street1 = ""
					try:
						street2 = a["street2"]
					except KeyError:
						street2 = ""
					try:
						city = a["city"]
					except KeyError:
						city = ""
					try:
						state = a["state"]
					except KeyError:
						state = ""
					try:
						postal_code = a["postal_code"]
					except KeyError:
						postal_code = ""
		try:
			if rock_client.right_to_contact == True:
				right_to_contact = "checked"
		except AttributeError:
			right_to_contact = ""

		webcode = []
		webcode.append('''<p>''')
		webcode.append('''	<table class="account_info">''')
		webcode.append('''		<tr>''')
		webcode.append('''		<tr colspan=2><td class="subitem">Primary Account Holder</td></tr>''')
		webcode.append('''		<td class="label"><label for="holder1_first">First Name*</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="holder1_first" value="%s" /></td>''' % unpacked_names["holder1_first"])
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="holder1_last">Last Name*</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="holder1_last" value="%s" /></td>''' % unpacked_names["holder1_last"])
		webcode.append('''		</tr>''')
		webcode.append('''		<tr colspan=2><td class="subitem">Secondary Account Holder</td></tr>''')
		webcode.append('''		<td class="label"><label for="holder2_first">First Name</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="holder2_first" value="%s" /></td>''' % unpacked_names["holder2_first"])
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="holder2_last">Last Name</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="holder2_last" value="%s" /></td>''' % unpacked_names["holder2_last"])
		webcode.append('''		</tr>''')
		webcode.append('''		<tr colspan=2><td class="subitem">Contact & Billing</td></tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''<!-- email field is just for show - it is ignored server-side-->''')
		webcode.append('''		<td class="label"><label for="email">Email</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="email" value="%s" disabled/></td>''' % email)
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="phone_number">Daytime Phone</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="phone_number" value="%s" /></td>''' % phone_number)
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="street1">Street Addreess</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="street1" value="%s" /></td>''' % street1)
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="street2">Apt/Ste</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="street2" value="%s" /></td>''' % street2)
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="city">City</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="city" value="%s" /></td>''' % city)
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="state">State</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="state" value="%s" /></td>''' % state)
		webcode.append('''		</tr>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="postal_code">Zip</label></td>''')
		webcode.append('''		<td class="field"><input type="text" class="primary_info" name="postal_code" value="%s" /></td>''' % postal_code)
		webcode.append('''		</tr>''')
		webcode.append('''		<tr colspan=2><td class="subitem">Student Names (if different from account holders above)</td></tr>''')
		webcode.append('''		<div id="students">''')
		for c in unpacked_names["children"]:
			webcode.append('''		<tr>''')
			webcode.append('''			<td class="label"><label for="student">Name</label></td>''')
			webcode.append('''			<td class="field"><input type="text" class="student_name" value="%s" /></td>''' % c)
		webcode.append('''		</tr>''')
		webcode.append('''		</div>''')
		webcode.append('''		<tr>''')
		webcode.append('''		<td class="label"><label for="right_to_contact">Email appointment reminders</label></td>''' )
		webcode.append('''		<td class="field"><input type="checkbox" class="right_to_contact" name="right_to_contact" %s/></td>''' % (right_to_contact))
		webcode.append('''		</tr>''')
		webcode.append('''	</table>''')
		webcode.append('''	</fieldset>		
						</p>
						</hr>
					   ''' )

		webcode = u"\n".join(webcode)

	return webcode