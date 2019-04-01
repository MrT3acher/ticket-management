import tornado.ioloop
import tornado.web
import torndb
from tornado.options import define, options

from webreq import handlers
from webapp import WebApp


define("port", default=1104, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="ticketdb", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="", help="database password")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = WebApp(handlers, options)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()