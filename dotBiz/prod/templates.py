def get(name, extension = "html", bin = "html"):
	'''
	Fetch a file from a child dir of templates
	'''

	with open("templates/{bin}/{name}.{extension}".format(**locals()),"r") as t:
		return t.read()
