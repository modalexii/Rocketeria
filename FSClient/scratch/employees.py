
def gethtml(employees):
	'''return html blob consisting of the template filled out for each element in EMPLOYEES'''
	'''expects (NAME : ID) tuples'''
	html = []
	html.append('''	<div id="employees">''')
	for e in employees:
		html.append('''	<div id="employee">''')
		html.append('''		<input type="radio" name="employees" value="%s" />'''	% (e[1]))
		html.append('''		<h2>%s</h2>'''								% (e[0]))
		html.append('''		<img src="/static/img/%s.jpg"></img>'''		% (e[0]))
		html.append('''		<a href="/lessons/instructors#%s" target="_blank">Read my bio</a>'''	% (e[0]))
		html.append('''	</div>''')
	html.append('''	</div>''')
	return u'\n'.join(html)

if __name__ == '__main__':
	print "employees.py doesn't do anything when called directly"
