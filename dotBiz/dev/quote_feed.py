import gae_db
from lxml import html
import random

def get_random() :
	'''
	Return a random '.quote_feed' from the contents of '/testimonials'
	If '/testimonials' does not exist (oops!) then return a nice but noticable message
	'''
	try:
		all_content = gae_db.fetch_content(uri = "testimonials")
	except AttributeError:
		quote = 'People are saying some really nice things about us. Click above to see for yourself!'
	else:

		tree = html.fromstring(all_content)
		all_quotes = [e.text_content() for e in tree.xpath('//span[@class="quote_feed"]')]
		quote = random.choice(all_quotes)

	return quote.encode('utf-8', 'xmlcharrefreplace')