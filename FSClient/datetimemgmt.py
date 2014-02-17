import datetime

def getweekdates():
	'''returns list of lists of date objects for this week and the next 2 weeks'''
	Y = int(datetime.datetime.today().strftime('%Y'))
	m = int(datetime.datetime.today().strftime('%m'))
	d = int(datetime.datetime.today().strftime('%d'))
	today = datetime.date(Y, m, d)
	#today = datetime.date(2014, 03, 1)
	firstdate = 0 - int(today.strftime('%w'))
	lastdate = 21 - int(today.strftime('%w'))
	alldays = [today + datetime.timedelta(days=i) for i in range(firstdate, lastdate)]

	dates = []
	dates.append(alldays[0:7])
	dates.append(alldays[7:14])
	dates.append(alldays[14:21])

	return dates

def getfsrange():
	'''return a tuple with the after and before days to send to FullSlate'''
	'''uses datetime.today() and end of last day teturned by getweekdates()'''
	import timezoneconvert
	dates = getweekdates()
	earliest = datetime.datetime.today() + datetime.timedelta(days=1) # tomorrow
	latest = dates[2][-1]
	fsafter = earliest.strftime('%Y%m%dT000000Z')
	fsbefore = latest.strftime('%Y%m%dT115959Z') # end of last day in dates
	return (fsafter,fsbefore)