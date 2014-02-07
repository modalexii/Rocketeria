import services
from sys import argv

def gethtml(employees):
	'''return html div elements for all employees that offer a given service'''
	for e in employees:
		html = []
		html.append('''	<div id="employee" class="%s">''' 				% (s['name']))
		html.append('''		<h2>%s</h2>'''								% (s['name']))
		html.append('''		<img src="/static/img/%s.jpg"></img>'''		% (s['name']))
		html.append('''		<a href="/lessons/instructors#%s" target="_blank">Read my bio</a>''')	% (s['name']))
		html.append('''	</div>''')
	return u'\n'.join(html)

if __name__ == '__main__':
	employees = services.whooffers(sys.argv[0])