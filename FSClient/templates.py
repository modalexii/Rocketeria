def get(blockname):

	if blockname == "devroot":
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
		</center>
	</body>
</html>
			'''
	elif blockname == "rocketeria-head":
		webcode = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html style="height: 100%;">
<head>
	<link rel="stylesheet" type="text/css" media="all" href="/static/style/rocketeria.css"/>
	<link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
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
	elif blockname == "rocketeria-tail":
		webcode = '''
		</div>
	</body>
</html>
				  '''
	elif blockname == "myaccount":
		webcode = ''' '''
	elif blockname == "book":
		webcode = '''
		<div id="fs-wrap">
			<div id="fs-embed-7PQgHZyw07"></div>
			<script type="text/javascript">
				(function() {(window.$fs || (window.$fs = [])).push([ "embed", {"root":"fs-embed-7PQgHZyw07","host":"rocketeria2.fullslate.com"} ]);if (!window.$fs._isFullSlate) { var fsscr = document.createElement("script"); fsscr.type = "text/javascript";fsscr.async = true; fsscr.src = ["http", (document.location.protocol == "https:" ? "s" : ""), "://rocketeria2.fullslate.com/api.js"].join("");var other = document.getElementsByTagName("script")[0]; other.parentNode.insertBefore(fsscr, other); }})();
			</script>
			<noscript>
				<p><a title="Online scheduling" href="http://rocketeria2.fullslate.com/?view=bare">Schedule Lesson</a></p>
			</noscript>
		</div>
				  '''
	elif blockname == "lessons-main":
		webcode = '''
		<div id="left">
			<p>Presumably, some content.</p>
			<p>Content.</p>
			<p>COOOOOOOOOOOOOOOOOOOOOOONTENT!!!!!!1!<p>
		</div>
		<div id="right">
			<script type="text/javascript">
				var submitted=false;
			</script>
			<iframe name="redirect_frame" id="redirect_frame" style="display:none;" onload="if(submitted) {window.location='/schedule.html';}"></iframe>
			<h3>Already have an account?</h3>
			<p>Sign in:<br />
				<!--<iframe src="https://rocketeria2.fullslate.com/login"></iframe>-->
				<form action="https://rocketeria2.fullslate.com/login" method="POST" target="redirect_frame" onsubmit="submitted=true;">
					Email: <input name="email" type="text" /><br />
					Pass: <input name="password" type="password" /> <br />
					<input type="submit" name="login" value="Submit">
				</form>
		</div>
				  '''

	return webcode