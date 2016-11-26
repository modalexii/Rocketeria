# The version must be the first thing between double quotes "" in
# this file or else the update_prod_from_dev script must be edited!

def version():
	return "1.4"

def from_url(url):
	if "127.0" in url or "localhost" in url:
		environment = "offline"
	elif "dev" in url:
		environment = "dev"
	elif "rocketeria.biz" in url:
		environment = "prod"
	else:
		environment = "unknown_instance"

	return environment

def as_hardcoded():
	return "prod"
