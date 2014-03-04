def is_reschedulable(today, event):
	'''
	Determine if an appointment is reschedulable
	TODAY is datetime
	EVENT is fullslate event object with normalized dates
	Returns Bool
	'''
	try:
		event['recurrence']
	except KeyError: # not a recurring appointment
		return False
	if not event['occurrence_at'] >= today: # appointment is today or earlier
		return False
	return True

def makeweek(dates,openings_by_day,today,labels):
	'''
	Returns string of html to show one week in the calendar-like element.
	DATES expected as returned from ranges.getweekdates()
	OPENINGS_BY_DAY expected as returned by openings.byday()
	TODAY is a datetime object
	LABLES - see makecal()

	Todo: replave "openings' verbage with "events" where appropriate
	'''

	import fs_datetime

	html = []
	html.append('''<!-- ------------- week ------------- -->''')
	html.append('''<div class="week">''')

	# accepted values of LABLES - keep mirrored with makecal()
	if labels == "new":
		event = "Available &#187;"
	elif labels == "existing":
		event = "Booked"
	else:
		raise Exception("bad value passed to events.makeweek() lables: %s" % lables)

	for dow in xrange(0,7):
		thisday = dates[dow].strftime('%d')

		if thisday == "01": # 1st of new month
			month_label = dates[dow].strftime('%b')
		else:
			month_label = ""

		if thisday == today.strftime('%d'):
			todayclass = " today" # leading space intentional
		else:
			todayclass = ""

		html.append('''	<div class="day%s">''' % (todayclass))
		html.append('''		<div class="daybar%s"><p>%s %s</p></div>''' % (todayclass, month_label, thisday))
		html.append('''
							<div class="dots">
								<ul>''')

		try: # make green if there are openings today
			html.append('''			<li class="green">%s %s</li>''' % (len(openings_by_day[thisday]),event))
		except KeyError:
			pass # this used to add li.red elements

		html.append('''
								</ul>
							</div> <!--/dots-->	
							<!-- slide open -->
							<div class="open">
								<ul>''')

		try: # list openings if there are any
			# important to catch all potential KeyError in this large try/except
			for o in openings_by_day[thisday]:

				try: # o is fullslate event
					fs_at = fs_datetime.fullslateify(o["occurrence_at"],"%Y-%m-%dT%H:%M:%S-0500")
					start_hhmm = o["occurrence_at"].strftime('%I:%M %p')
					end_hhmm = o['to'].strftime('%I:%M %p')
					'''
					o["to"] may be an issue - it is the end time of the last appointment (if recurrence)
					and it may not reflect the end time of the current appointment
					'''
				except TypeError: # o is datetime
					fs_at = fs_datetime.fullslateify(o,"%Y-%m-%dT%H:%M:%S-0500")
					start_hhmm = o.strftime('%I:%M %p')

				html.append('''			<li class="green event">''')
				try: # o is fullslate event
					html.append('''				<input type="radio" id="%s" name="event" value="%s" /> ''' % (o['id'],o['id']))
					html.append('''				<label for="%s">'''			% (o['id']))
				except TypeError:  # o is datetime
					html.append('''				<input type="radio" id="%s" name="opening" value="%s" /> ''' % (fs_at,fs_datetime.fullslateify(o,"%A %B %d, %I:%M %p")))
					html.append('''				<label for="%s">'''			% start_hhmm)

				try:
					html.append('''					%s-%s'''				% (start_hhmm,end_hhmm))
				except UnboundLocalError: # no end_hhmm - o is datetime
					html.append('''					%s'''					% start_hhmm)

				if labels == "existing":
					html.append(''' Instructor: <br/>%s''' % o['employee']['name'])
					html.append(''' <i>[debug: %s, %s]</i><br/>''' % (o['occurrence_at'].strftime("%Y-%m-%d"), o['attendees'][0]['name']))

					if is_reschedulable(today,o):
						# rechedulable implies reocurring
						html.append(''' <img src="/static/style/repeat.png" class="repeat_ico" title="part of a series of appointments"/>''')
						cancel_class = "reschedule"
						button_val = "cancel/reschedule"
					else:
						cancel_class = "cancel"
						button_val = "cancel"
					html.append(''' 		<form class="cancel" action="#">''')
					html.append(''' 			<input type="submit" class="%s" value="%s" />''' % (cancel_class,button_val))
					html.append(''' 		</form>''')
					html.append(''' 	</label>''')
					html.append(''' </li>''')

		except KeyError as e:
			print '\nGOT KEY ERROR %s\n' % e

		html.append('''
								</ul>
							</div>	<!--/open-->
							<!-- slide closed -->
						</div> <!--/day-->''')

	html.append('''</div> <!--/week-->	''')	

	return u'\n'.join(html)

def makecal(eventlist,num_weeks,labels):
	'''
	Fill out the template for each item in EVENTLIST
	EVENTLIST list of datetime objects
	LABLES is a string that sets the wording used throughout
	Returns a string (of html)
	'''
	import ranges,timezoneconvert,openings
	from datetime import datetime

	# accepted values of LABLES - keep mirrored with makeweek()
	if labels == "new":
		heading = "Choose an Appointment"
	elif labels == "existing":
		heading = "Your Appointments"
	else:
		raise Exception("bad value passed to events.makecal() lables: %s" % lables)

	openings_by_day = openings.byday_full(eventlist)

	html = []
	html.append('''				
					<div id="calcontainer">
						<div id="calheader">
				''')
	html.append('''<h2>%s</h2>''' % heading)
	html.append('''
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

	# Get today's date/time in EST
	EST = timezoneconvert.abbr2zone("EST")
	GMT = EST = timezoneconvert.abbr2zone("GMT")
	today = datetime.today()
	print '\n\nTODAY %d %H:%M: ',today,'  \  ',today.strftime('%d %H:%M')
	today = timezoneconvert.set(today,GMT)
	today = timezoneconvert.convert(today,EST)
	print '\n\nTODAY-CONVERTED %d %H:%M: ',today,'  \  ',today.strftime('%d %H:%M')

	for w in xrange(num_weeks):
		dates = ranges.getweekdates(offset=w)
		htmlweek = makeweek(dates, openings_by_day, today, labels)
		html.append(htmlweek)
	html.append('''
						</div> <!--/daysmonth-->
					</div> <!--/calcontainer-->				
				</div>
				<hr />
			<p></p><!--pushes #main down-->	''')
	return u'\n'.join(html)


