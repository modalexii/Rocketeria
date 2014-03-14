def get(name,extension="html"):
	t = open('templates/%s.%s' % (name,extension),'r')
	content = t.read()
	t.close()

	return content