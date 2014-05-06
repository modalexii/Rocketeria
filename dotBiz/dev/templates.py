def get(name, extension = "html"):
	'''
	Fetch a file from a child dir of templates with the same name as the file extension.
	'''

	with open("templates/{extension}/{name}.{extension}".format(**locals()),"r") as t:
		return t.read()


'''
This was used when we thought embedded-everything was cool.
It might have utility in the future.
def get(name, tag = None, tag_type = None, extension = "html", comment = False):

	with open("templates/{extension}/{name}.{extension}".format(**locals()),"r") as t:
		content = t.read()

	if tag and tag_type:
		content = '<{tag} type="{tag_type}">{content}</{tag}>'.format(**locals())
	elif tag and not tag_type:
		content = '<{tag}>{content}</{tag}>'.format(**locals())

	if comment:
		content = '<!-- {content} -->'.format(**locals())

	return content
'''