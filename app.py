#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

#tornado imports
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options

define("port", default=9988, help="run on the given port")
define("upload_path", default="/data/web/upload/", help="upload path")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        dirs = os.listdir(options.upload_path)
        files = []
        for file_name in dirs:
            if os.path.isfile(options.upload_path + file_name):
                files.append(file_name)
                
        self.render("index.html", files=files)
    
    def post(self):
        file_dict_list = self.request.files['file']
        for file_dict in file_dict_list:
            filename = file_dict["filename"]
            f = open(options.upload_path + filename, "wb")
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
        handlers = [
            (r"/", MainHandler),
            (r"/download/(.*)", tornado.web.StaticFileHandler, {"path": options.upload_path}),
        ]
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.options.log_file_prefix = r"web.log"
    tornado.options.options.log_file_max_size = 10*1024*1024
    tornado.options.options.logging = "warn"
    tornado.options.parse_command_line()
    
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    print "upload path: %s" % options.upload_path
    if not os.path.isdir(options.upload_path):
        print "dir-%s not exist" % options.upload_path
    else:
        print "Starting HTTP proxy on port %d" % options.port
        main()

