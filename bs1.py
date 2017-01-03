# -*- coding: utf-8 -*-
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from datetime import datetime
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):        
        a='http://127.0.0.1'
        self.render('bs1.html',a=a,b=u'骆宇天',c='test123',t=datetime.now())

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([(r"/", LoginHandler)],
        template_path = os.path.join(os.path.dirname(__file__),"templates"),
        static_path =os.path.join(os.path.dirname(__file__), "static"),
        debug = True                      
    )   
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
