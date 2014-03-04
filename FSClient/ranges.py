import datetime

def getweekdates(offset=0):
	'''
	returns list of 7 datetime objects representing a week, 
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
	Return a dict with the after and before days to send to FullSlate 
	FSAFTER will be today + 7(OFFSET)
	FSBEFORE will be FSAFTER + 7(NUMWEEKS)
	'''
	offset_days = 7 * offset

	print "\n\nOFFSET/NUM_WEEKS/OFFSET_DAYS FROM GETFSRANGE: ",offset,' / ',num_weeks,' / ',offset_days

	fsafter = datetime.datetime.today() + datetime.timedelta(days=offset_days)
	fsbefore = fsafter + datetime.timedelta(days = 7 * num_weeks, hours = -12)

	return {"after" : fsafter, "before" : fsbefore}