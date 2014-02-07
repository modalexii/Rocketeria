import fsapi

services = fsapi.apirequest('services')

def gethtml():
	'''return html div elements for all services'''
	for s in services:
		html = []
		html.append('''	<div id="service" class="%s">''' 		% (s['name']))
		html.append('''		<h2>%s</h2>'''						% (s['name']))
		html.append('''		<p>%s</p>'''						% (s['description']))
		html.append('''		<h3 class="time">%s min</h3>'''		% (str(s['time'] / 60)))
		html.append('''		<h3 class="price">%s</h3>''' 		% (str(s['price'])))
		html.append('''	</div>''')
	return u'\n'.join(html)

def whooffers(service):
	'''return the names of the employees who offer a given service'''
	employees = [s['employees'] for s in services if s['name'] == service][0]
	names = [e['name'] for e in employees]
	return names

if __name__ == '__main__':
	print "services.py doesn't do anything when called directly"
	#print gethtml()
	#print whooffers('Guitar')