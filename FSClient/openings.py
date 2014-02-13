
'''
{"matches":[
	{"at":"20140210T163000Z","day":2227,"time":41400,"label":"Monday, February 10 11:30 AM"},
	{"at":"20140210T213000Z","day":2227,"time":59400,"label":"Monday, February 10 4:30 PM"},
	{"at":"20140211T160000Z","day":2228,"time":39600,"label":"Tuesday, February 11 11:00 AM"},
	{"at":"20140211T210000Z","day":2228,"time":57600,"label":"Tuesday, February 11 4:00 PM"},
	{"at":"20140212T163000Z","day":2229,"time":41400,"label":"Wednesday, February 12 11:30 AM"}],
"tz":"EST",
"success":true}
'''
import datetime

def getweekdates():
	'''returns dict of lists of date objects for this week and the next 2 weeks'''
	Y = int(datetime.datetime.today().strftime('%Y'))
	m = int(datetime.datetime.today().strftime('%m'))
	d = int(datetime.datetime.today().strftime('%d'))
	today = datetime.date(Y, m, d)
	#today = datetime.date(2014, 03, 1)
	firstdate = 0 - int(today.strftime('%w'))
	lastdate = 21 - int(today.strftime('%w'))
	alldays = [today + datetime.timedelta(days=i) for i in range(firstdate, lastdate)]

	#dates = {'current' : alldays[0:7], 'nextweek' : alldays[7:14], 'thirdweek' : alldays[14:21],}
	dates = {}
	dates['current'] = alldays[0:7]
	dates['nextweek'] = alldays[7:14]
	dates['thirdweek'] = alldays[14:21]

	return dates

def parseopenings(openingobj):
	'''OPENINGOBJ is list of strings formatted YYYYMMDD[T]HHMMSS[Z] (literal 'T', 'Z')'''
	import timezoneconvert
	GMT = timezoneconvert.Zone(0,False,'GMT')
	EST = timezoneconvert.Zone(-5,False,'EST')
	openingsbyday = {}
	for o in openingobj['openings']:
		# convert from 24-hr GMT string to 12-hr EST string
		gmttimeobj = datetime.datetime.strptime(o, '%Y%m%dT%H%M%SZ')
		gmttimeobj = gmttimeobj.replace(tzinfo=GMT)
		esttimeobj = gmttimeobj.astimezone(EST)
		dom = esttimeobj.strftime('%d')
		hhmm = esttimeobj.strftime('%I:%M %p')

		try:
			openingsbyday[dom] += [hhmm]
		except KeyError:
			openingsbyday[dom] = [hhmm]
	return openingsbyday

def makeweek(dates, openingsbyday,today):
	html = []
	for week in dates:
		openings = dates[week]
		print ">>> DEBUG ",week,"+",openings
		html.append('''<!-- ---------- %s ---------- -->''' % (week))
		html.append('''<div class="week">''')
		for dow in xrange(0,7):
			thisday = dates[week][dow].strftime('%d')
			if thisday == today:
				todayclass = " today" # leading space intentional
			else:
				todayclass = ""
			html.append('''	<div class="day%s">''' % (todayclass))
			html.append('''		<div class="daybar%s"><p>%s</p></div>''' % (todayclass, thisday))
			html.append('''
								<div class="dots">
									<ul>''')
			try: # make green if there are openings today
				openingsbyday[thisday]
				html.append('''			<li class="green">%s OPEN</li>''' % len(openingsbyday[thisday]))
			except KeyError:
				html.append('''			<li class="red"></li>''')
			html.append('''
									</ul>
								</div> <!--/dots-->	
								<!-- slide open -->
								<div class="open">
									<ul>''')
			try: # list openings if there are any
				for opening in openingsbyday[thisday]:
					html.append('''			<li class="green"><a href="#123"><p>%s</p></a></li> ''' % (opening))
			except KeyError,TypeError:
				pass
			html.append('''
									</ul>
								</div>	<!--/open-->
								<!-- slide closed -->
							</div> <!--/day-->''')
		html.append('''</div> <!--/week-->	''')	
	return u'\n'.join(html)

def gethtml(openingobj):
	'''Fill out the template for each item in OPENINGOBJ'''
	'''OPENINGOBJ is list of strings formatted YYYYMMDD[T]HHMMSS[Z] (literal 'T', 'Z')'''
	dates = getweekdates()
	openingsbyday = parseopenings(openingobj)
	html = []
	html.append('''				
					<div id="calcontainer">
						<div id="calheader">
							<h2></h2>
						</div>
						<div id="daysweek">
							<div class="dayweek brn"><p>Sunday</p></div>
							<div class="dayweek"><p>Monday</p></div>
							<div class="dayweek"><p>Tuesday</p></div>
							<div class="dayweek"><p>Wednesday</p></div>
							<div class="dayweek"><p>Thursday</p></div>
							<div class="dayweek"><p>Friday</p></div>
							<div class="dayweek"><p>Saturday</p></div>
						</div>
						<div id="daysmonth">''')
	today = datetime.datetime.today().strftime('%d')
	html.append(makeweek(dates, openingsbyday, today))
	html.append('''
						</div> <!--/daysmonth-->
						<div id="calcat">
							<!--<div class="caldot blue"></div><p>NEW CAT1</p>-->
							<!--<div class="caldot yellow"></div><p>NET CAT2</p>-->
							<div class="caldot green"></div><p>Times Available</p>
							<div class="caldot red"></div><p>No Availability</p>
						</div>
					</div>	<!--/daysmonth-->								
				</div>	<!--/calcontainer-->''')
	return u'\n'.join(html)