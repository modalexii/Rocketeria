
def gethtml(serviceobj):
	'''return html blob consisting of the template filled out for each element in SERVICEOBJ'''
	html = []
	html.append('''<div id="services">''')
	html.append('''<h2>Choose an Instrument</h2>''')
	for s in serviceobj:
		html.append('''	<div id="svc%s" class="service">'''				% (s['id']))
		html.append('''		<input type="radio" id="%s" name="service" value="%s" />'''	% (s['id'],s['id']))
		html.append('''		<label for="%s">'''							% (s['id']))
		html.append('''			<img src="/static/style/%s.png" />'''	% (s['name']))
		html.append('''			%s'''									% (s['name']))
		html.append('''		</label>''')
		html.append('''		<p>%s</p>'''								% (s['description']))
		html.append('''		<h3 class="pricetime">$%s/%s min</h3>'''	% (str(s['price']),str(s['time'] / 60)))
		html.append('''	</div>''')
	html.append('''	<hr />''')
	html.append('''	</div>''')
	return u'\n'.join(html)

def whooffers(serviceid,serviceobj):
	'''return list of IDs of employees in SERVICEOBJ who offer SERVICEID'''
	employees = [s['employees'] for s in serviceobj if s['id'] == int(serviceid)][0]
	ids = [e['id'] for e in employees]
	return ids

if __name__ == '__main__':
	print "services.py doesn't do anything when called directly"
