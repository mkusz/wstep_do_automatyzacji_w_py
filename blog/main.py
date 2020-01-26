import gevent
from gevent.pywsgi import WSGIServer
from .zayzafoun import app

app.config.from_object("config")
http_server = WSGIServer(('0.0.0.0', 5000), app)
http_server.start()

app.config.from_object("config2")
http_server2 = WSGIServer(('0.0.0.0', 5001), app)
http_server2.start()

while True:
    print()
    gevent.sleep(60)