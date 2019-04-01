import tornado.web
import torndb

class WebApp(tornado.web.Application):
    def __init__(self, handlers, options):

        settings = dict()
        super(WebApp, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)
