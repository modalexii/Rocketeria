import datetime
import timezoneconvert

GMT = timezoneconvert.Zone(0,False,'GMT')
EST = timezoneconvert.Zone(-5,False,'EST')

def parseopenings(openingobj):
	'''
	Return dict formatted { day of month : [opening,opening,] } for each object in OPENINGOBJ.
	OPENINGOBJ is list of strings formatted YYYYMMDDTHHMMSSZ, e.g. ['20140214T000000Z',]
	'''

	openingsbyday = {}

	for o in openingobj['openings']:
		# convert from 24-hr GMT string to 12-hr EST string
		obj_in_GMT = datetime.datetime.strptime(o, '%Y%m%dT%H%M%SZ')
		obj_in_GMT = obj_in_GMT.replace(tzinfo=GMT)
		obj_in_EST = obj_in_GMT.astimezone(EST)

		dom = obj_in_EST.strftime('%d')
		hhmm = obj_in_EST.strftime('%I:%M %p')

		try:
			openingsbyday[dom] += [hhmm]
		except KeyError: # first element
			openingsbyday[dom] = [hhmm]

	return openingsbyday

def make_week(dates,openingsbyday,today):
	'''
	Returns string of html to show one week in the calendar-like element.
	DATES expected as returned from datetimemgmt.getweekdates()
	OPENINGSBYDAY expected as returned by parseopenings()
	TODAY expected as datetime.datetime.today().strftime('%d')
	'''
	html = []
	html.append('''<!-- ------------- week ------------- -->''')
	html.append('''<div class="week">''')

	for dow in xrange(0,7):
		thisday = dates[dow].strftime('%d')

		if thisday == "01": # 1st of new month
			month_label = dates[dow].strftime('%b')
		else:
			month_label = ""

		if thisday == today:
			todayclass = " today" # leading space intentional
		else:
			todayclass = ""

		html.append('''	<div class="day%s">''' % (todayclass))
		html.append('''		<div class="daybar%s"><p>%s %s</p></div>''' % (todayclass, month_label, thisday))
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

def make_cal(eventsobj,num_weeks=3):
	'''Fill out the template for each item in EVENTSOBJ'''
	'''EVENTSOBJ is list of strings formatted YYYYMMDD[T]HHMMSS[Z] (literal 'T', 'Z')'''
	import datetimemgmt

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
	today = datetime.datetime.today().replace(tzinfo=GMT).astimezone(EST).strftime('%d') # today %d in EST
	for w in xrange(num_weeks):
		dates = datetimemgmt.getweekdates(offset=w)
		htmlweek = make_week(dates, openingsbyday, today)
		html.append(htmlweek)
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