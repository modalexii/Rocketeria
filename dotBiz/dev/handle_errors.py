import logging 
logging.getLogger().setLevel(logging.INFO)

def http403(request, response):
    logging.warning("403 for path \"%s\" from client %s ", request.path, request.remote_addr)
    response.set_status(403)
    #self.redirect("/500")
    response.write("<h1>403</h1>")

def http404(request, response):
    logging.info("404 for path \"%s\" from client %s ", request.path, request.remote_addr)
    response.set_status(404)
    #self.redirect("/404")
    response.write("<h1>404</h1>")

def http500(request, response, exception):
    logging.error(exception)
    response.set_status(500)
    #self.redirect("/500")
    response.write("<h1>Server error</h1>")