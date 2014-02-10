def weekdates():
	'''returns dict of lists of date objects for this week and the next 2 weeks'''
	import datetime
	Y = int(datetime.datetime.today().strftime('%Y'))
	m = int(datetime.datetime.today().strftime('%m'))
	d = int(datetime.datetime.today().strftime('%d'))
	today = datetime.date(Y, m, d)
	#today = datetime.date(2014, 03, 1)
	firstdate = 0 - int(today.strftime('%w'))
	lastdate = 7 - int(today.strftime('%w'))
	thisweek = [today + datetime.timedelta(days=i) for i in range(firstdate, lastdate)]

	for day in thisweek:
		nextweek = ([day + datetime.timedelta(days=i+1) for i in range(firstdate, lastdate)])

	for day in nextweek:
		thirdweek = ([day + datetime.timedelta(days=i+1) for i in range(firstdate, lastdate)])

	import pprint
	pprint.pprint(thisweek)
	pprint.pprint(nextweek)
	pprint.pprint(thirdweek)

	return {'thisweek' : thisweek, 'nextweek' : nextweek, 'thirdweek' : thirdweek,}

dates = weekdates()
