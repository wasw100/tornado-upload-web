# -*- coding: utf-8 -*-

import os

#tornado imports
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options

define("port", default=9988, help="run on the given port")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    
    def post(self):
        file_dict_list = self.request.files['file']
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            f = open("/data/web/upload/%s" % filename, "wb")
            f.write(file_dict["body"])
            f.close()
        self.redirect("/")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
                        template_path=os.path.join(os.path.dirname(__file__), "templates"),
                        static_path=os.path.join(os.path.dirname(__file__), "static"),
                        xsrf_cookies=False,
                        cookie_secret="noneed",
                        login_url="/login",
                        autoescape=None,
                        debug=True,
                     )   
        super(Application, self).__init__([(r"/", MainHandler)], **settings)

def main():
    tornado.options.options.log_file_prefix = r"web.log"
    tornado.options.options.log_file_max_size = 10*1024*1024
    tornado.options.options.logging = "warn"
    tornado.options.parse_command_line()
    
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

