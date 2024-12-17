#import gunicorn

# Change response 'Server' http header
#gunicorn.SERVER = ""

from gunicorn.http import wsgi

# Remove 'Server' http header from response
class Response(wsgi.Response):
    def default_headers(self, *args, **kwargs):
        headers = super(Response, self).default_headers(*args, **kwargs)
        return [h for h in headers if not h.startswith(('Server:', 'Connection:'))]

wsgi.Response = Response
