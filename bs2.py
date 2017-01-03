# -*- coding: utf-8 -*-
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from tornado.options import define, options
from datetime import datetime

define("port", default=8000, help="run on the given port", type=int)

class TemplateRendering(object):
    """
    A simple class to hold methods for rendering templates.标准代码，不要修改
    """
    def render_template(self, template_name, **kwargs):
        template_dirs = []
        if self.settings.get('template_path', ''):
            template_dirs.append(self.settings['template_path'])
        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(kwargs)
        return content 

# BaseHandler 由jinja2模板渲染
class BaseHandler(tornado.web.RequestHandler, TemplateRendering):
    """
    Tornado RequestHandler subclass.
    """
    def initialize(self):
        pass

    def render_html(self, template_name, **kwargs):
        kwargs.update({
            #下面的变量，通过render字符串传递给模板文件
            'settings': self.settings,
            'static_url': self.settings.get('static_url_prefix', '/static/'),
            'request': self.request,
            'reverse_url': self.reverse_url,
            'headers': self.request.headers,
            'current_user': self.current_user,
            'xsrf_token': self.xsrf_token,
            'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)
    def get(self):
        #下面的变量，通过render字符串传递给模板文件
        a='http://127.0.0.1'        
        self.render_html('bs2.html',a=a,b=u'骆宇天',t=datetime.now(),c='test123')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([(r"/", BaseHandler)],
        #下面的变量，保存在settings字典中传递给模板文件
        template_path = os.path.join(os.path.dirname(__file__),"templates"),
        static_path =os.path.join(os.path.dirname(__file__), "static"),
        abc = 'abc',
        debug = True                      
    )   
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
