
def gethtml(employeeobj):
	'''return html blob consisting of the template filled out for each element in EMPLOYEEOBJ'''
	html = []
	html.append('''	<div id="employees">''')
	html.append('''<h2>Choose an Instructor</h2>''')
	for e in employeeobj:
		html.append('''	<div id="emp%s" class="employee">'''				% (e['id']))
		html.append('''		<input type="radio" id="%s" name="employee" value="%s" />'''	% (e['id'],e['id']))
		html.append('''		<label for="%s">'''							% (e['id']))
		html.append('''			<img src="/static/style/%s%s.png" />'''	% (e['first_name'],e['last_name']))
		html.append('''			%s %s'''								% (e['first_name'],e['last_name']))
		html.append('''		</label>''')
		html.append('''		<p><a href="/lessons/instructors#%s%s">Read my bio</a></p>'''	% (e['first_name'],e['last_name']))
		html.append('''	</div>''')
	html.append('''
	<div id="emp0" class="employee">
		<input type="radio" id="0" name="employee" value="Any" />
		<label for="0">
			<img src="/static/style/Any.png" />
			No Preference
		</label>
		<p><a href="#"></a>Everyone's availability will be shown</p>
	</div>
				''')
	html.append('''	<hr />''')
	html.append('''	</div>''')
	return u'\n'.join(html)

if __name__ == '__main__':
	print "employees.py doesn't do anything when called directly"
