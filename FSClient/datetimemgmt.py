import datetime

def getweekdates(offset=0):
	'''
	returns list of 7 past or future datetime objects, 
	with the 0th element being a Sunday and the 6th being a Saturday,
	starting OFFSET weeks from the current week.
	'''
	Y = int(datetime.datetime.today().strftime('%Y'))
	m = int(datetime.datetime.today().strftime('%m'))
	d = int(datetime.datetime.today().strftime('%d'))

	today = datetime.date(Y, m, d)
	#today = datetime.date(2014, 03, 1)
	offset = offset * 7

	firstdate = (0 + offset) - int(today.strftime('%w'))
	lastdate = (7 + offset) - int(today.strftime('%w'))
	week = [today + datetime.timedelta(days=i) for i in range(firstdate, lastdate)]

	return week

def getfsrange(offset=0,num_weeks=1):
	'''
	Return a tuple with the after and before days to send to FullSlate 
	FSAFTER will be today + 7(OFFSET) + 1
	FSBEFORE will be <this saturday> + 7(OFFSET) + 7(NUMWEEKS)
	'''
	dates = getweekdates(offset=offset)
	offset_days = 7 * offset
	num_days = 7 * num_weeks

	earliest = datetime.datetime.today() + datetime.timedelta(days = offset_days + 1)
	latest = dates[-1] + datetime.timedelta(days = offset_days + num_days)

	fsafter = earliest.strftime('%Y%m%dT000000Z')
	fsbefore = latest.strftime('%Y%m%dT115959Z')

	return (fsafter,fsbefore)