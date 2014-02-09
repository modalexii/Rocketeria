
def gethtml(servicesobj):
	'''return html blob consisting of the template filled out for each element in SERVICESOBJ'''
	html = []
	html.append('''	<div id="derp">''')
	for s in servicesobj:
		html.append('''	<div id="service">''')
		html.append('''		<input type="radio" name="services" value="%s">'''	% (s['id']))
		html.append('''		<h2 class="instrument">%s</h2>'''	% (s['name']))
		html.append('''		<p>%sTHIS IS WORKING</p>'''						% (s['description']))
		html.append('''		<h3 class="time">%s min</h3>'''		% (str(s['time'] / 60)))
		html.append('''		<h3 class="price">$%s</h3>''' 		% (str(s['price'])))
		html.append('''	</div>''')
	html.append('''	</div>''')
	return u'\n'.join(html)

def whooffers(service,servicesobj):
	'''return list of (NAME : ID) tuples of employees in SERVICESOBJ who offer SERVICE'''
	employees = [s['employees'] for s in servicesobj if s['name'] == service][0]
	names = [e['name'] for e in employees]
	ids = [e['name'] for e in employees]
	return zip(names, ids)

if __name__ == '__main__':
	print "services.py doesn't do anything when called directly"
