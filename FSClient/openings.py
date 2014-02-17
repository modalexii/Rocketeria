import datetime

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

def makeweek(dates,openingsbyday,today):
	html = []
	for week in dates:
		print ">>> DEBUG: ",dates.index(week),"openings: ",week
		html.append('''<!-- ---------- week %s ---------- -->''' % (dates.index(week)))
		html.append('''<div class="week">''')
		for dow in xrange(0,7):
			thisday = week[dow].strftime('%d')
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
				html.append('''			<li class="green">%s AVAILABLE</li>''' % len(openingsbyday[thisday]))
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
					html.append('''			<li class="green">''')
					html.append('''				<input type="radio" id="%s" name="opening" value="%s" /> ''' % (opening,opening))
					html.append('''				<label for="%s">'''			% (opening))
					html.append('''					%s'''					% (opening))
					html.append('''				</label>''')
					html.append('''			</li>''')
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
	import datetimemgmt
	dates = datetimemgmt.getweekdates()
	openingsbyday = parseopenings(openingobj)
	html = []
	html.append('''				
					<div id="calcontainer">
						<div id="calheader">
							<h2>Choose a Time</h2>
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
					</div> <!--/calcontainer-->
					<div id="calcat">
						<!--<div class="caldot blue"></div><p>NEW CAT1</p>-->
						<!--<div class="caldot yellow"></div><p>NET CAT2</p>-->
						<div class="caldot green"></div><p>Times Available</p>
						<div class="caldot red"></div><p>No Availability</p>
					</div>						
				</div>
			<p></p><!--pushes #main down-->	''')
	return u'\n'.join(html)