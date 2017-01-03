# -*- coding: utf-8 -*-
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class TemplateRendering(object):
    """
    A simple class to hold methods for rendering templates.
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

# 就是重新写 BaseHandler 由jinja2模板渲染
class BaseHandler(tornado.web.RequestHandler, TemplateRendering):
    """
    Tornado RequestHandler subclass.
    """
    def initialize(self):
        pass

    def render_html(self, template_name, **kwargs):
        kwargs.update({
          'settings': self.settings,
          'STATIC_URL': self.settings.get('static_url_prefix', '/static/'),
          'request': self.request,
          'current_user': self.current_user,
          'xsrf_token': self.xsrf_token,
          'xsrf_form_html': self.xsrf_form_html,
        })
        content = self.render_template(template_name, **kwargs)
        self.write(content)
    def get(self):
        self.render_html('default.html',a='luoshi',b=u'骆宇天')


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render_html('default.html',a='luoshi')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                difference=noun3)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', BaseHandler), (r'/poem', PoemPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()