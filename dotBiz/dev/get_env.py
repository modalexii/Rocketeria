def version():
	return "0.90"

def from_url(url):
	if "127.0" in url or "localhost" in url:
		environment = "offline"
	elif "dev" in url:
		environment = "dev"
	elif "//rocketeria.biz" in url:
		environment = "prod"
	else:
		environment = "unknownInstance"

	return environment