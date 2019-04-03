import tornado.web
from hashlib import md5
from random import random

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def check_username(self, username):
        result = self.db.execute_rowcount("SELECT * from `users` where `username`=%s", username)
        if result > 0:
            return True
        else :
            return False
    def check_token(self, token):
        result = self.db.get("SELECT * from `users` where `token`=%s", token)
        if result:
            return result
        else:
            return None
    def check_auth(self, username, password):
        result = self.db.get("SELECT * from `users` where `username`=%s and `password`=%s", username, password)
        if result:
            return result
        else:
            return False

class DefaultHandler(BaseHandler):
    response = {
        'message': 'Wrong Command. You May Use Another Method.',
        'code': 1
    }

    def get(self):
        self.write(self.response)

    def post(self, *args, **kwargs):
        self.write(self.response)

class Signup(BaseHandler):
    def get(self):
        self.write(DefaultHandler.response)

    def post(self):
        username = self.get_argument('username')
        if self.check_username(username):
            self.write({
                'message': 'This Username Exist.',
                'code': 1
            })
        else:
            password = self.get_argument('password')
            firstname = self.get_argument('firstname')
            lastname = self.get_argument('lastname')
            result = self.db.execute(
                "INSERT INTO `users` (`username`, `password`, `firstname`, `lastname`) VALUES (%s, %s, %s, %s)",
                username, password, firstname, lastname)
            if result:
                self.write({
                    'message': 'Signed Up Successfully',
                    'code': 200
                })
            else:
                self.write({
                    'message': 'There Is Some Problem. Try Again.',
                    'code': 2
                })

class Login(BaseHandler):
    def get(self):
        self.write(DefaultHandler.response)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        result = self.check_auth(username, password)
        if result:
            token = result['token']
            if token == "":
                string = username + str(random())
                token = md5(string.encode()).hexdigest()
                self.db.execute("UPDATE `users` SET `token`=%s WHERE `username`=%s AND `password`=%s", token, username,
                            password)
            self.write({
                'message': 'Logged In Successfully',
                'token': token,
                'code': 200
            })
        else:
            self.write({
                'message': 'Wrong Username Or Password',
                'code': 1
            })

class Logout(BaseHandler):
    def get(self):
        self.write(DefaultHandler.response)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        result = self.check_auth(username, password)
        if result:
            self.db.execute("UPDATE `users` SET `token`=%s WHERE `username`=%s AND `password`=%s", "", username,
                            password)
            self.write({
                'message': 'Logged Out Successfully',
                'code': 200
            })
        else:
            self.write({
                'message': 'Wrong Username Or Password',
                'code': 1
            })

class SendTicket(BaseHandler):
    def get(self):
        self.write(DefaultHandler.response)

    def post(self):
        token = self.get_argument('token')
        subject = self.get_argument('subject')
        body = self.get_argument('body')
        user = self.check_token(token)
        if user:
            result = self.db.insert("INSERT INTO `tickets` (`subject`, `body`, `user_id`) VALUES (%s, %s, %d)",
                                    subject, body, user['id'])
            self.write({
                'message': 'Ticket Sent Successfully',
                'id': result,
                'code': 200
            })
        else:
            self.write({
                'message': 'Wrong Token',
                'code': 1
            })

class UserGetTickets(BaseHandler):
    def get(self):
        token = self.get_query_argument('token')
        user = self.check_token(token)
        if user:
            result = self.db.query("SELECT * FROM `tickets` WHERE `user_id`=%d", user['id'])
            response = {
                'message': 'There Are -%d-' % len(result),
                'code': 200
            }
            for i, row in enumerate(result):
                response["block " + str(i)] = row
            self.write(response)
        else:
            self.write({
                'message': 'Wrong Token',
                'code': 1
            })

    def post(self):
        self.write(DefaultHandler.response)

class CloseTicket(BaseHandler):
    def get(self):
        self.write(DefaultHandler.response)

    def post(self):
        id = self.get_argument('id')
        token = self.get_argument('token')
        user = self.check_token(token)
        if user:
            result = self.db.execute("SELECT * FROM `tickets` WHERE `user_id`=%d AND `id`=%d", user['id'], id)
            self.write({
                'message': 'Ticket With id -%d- Closed Successfully' % id,
                'code': 200
            })
        else:
            self.write({
                'message': 'Wrong Token',
                'code': 1
            })

class AdminGetTickets(BaseHandler):
    def get(self):
        token = self.get_query_argument('token')
        user = self.check_token(token)
        if user:
            if user["id"] != 1:
                self.write({
                    'message': 'Premission Denied',
                    'code': 2
                })
            else:
                result = self.db.query("SELECT * FROM `tickets`")
                response = {
                    'message': 'There Are -%d-' % len(result),
                    'code': 200
                }
                for i, row in enumerate(result):
                    response["block " + str(i)] = row
                self.write(response)
        else:
            self.write({
                'message': 'Wrong Token',
                'code': 1
            })

    def post(self):
        self.write(DefaultHandler.response)

class TicketResponse(BaseHandler):
    def get(self):
        self.write(DefaultHandler.response)

    def post(self):
        id = self.get_argument('id')
        body = self.get_argument('body')
        token = self.get_argument('token')
        user = self.check_token(token)
        if user:
            if user["id"] != 1:
                self.write({
                    'message': 'Premission Denied',
                    'code': 2
                })
            else:
                self.db.execute("INSERT INTO `tickets` (`body`, `ticket_id`) VALUES (%s, %d)", body, id)
                self.db.execute("UPDATE `tickets` SET `status`='close' WHERE `id`=%d", id)
                self.write({
                    'message': 'Response to Ticket With id -%d- Sent Successfully' % id,
                    'code': 200
                })
        else:
            self.write({
                'message': 'Wrong Token',
                'code': 1
            })

class TicketChangeStatus(BaseHandler):
    def get(self):
        self.write(DefaultHandler.response)

    def post(self):
        id = self.get_argument('id')
        status = self.get_argument('status')
        token = self.get_argument('token')
        user = self.check_token(token)
        if user:
            if user["id"] != 1:
                self.write({
                    'message': 'Premission Denied',
                    'code': 2
                })
            else:
                self.db.execute("UPDATE `tickets` SET `status`=%s WHERE `id`=%d", status, id)
                self.write({
                    'message': 'Status Ticket With id -%d- Changed Successfully' % id,
                    'code': 200
                })
        else:
            self.write({
                'message': 'Wrong Token',
                'code': 1
            })

handlers = [
    (r"/signup", Signup),
    (r"/login", Login),
    (r"/logout", Logout),
    (r"/sendticket", SendTicket),
    (r"/getticketcli", UserGetTickets),
    (r"/closeticket", CloseTicket),
    (r"/getticketmod", AdminGetTickets),
    (r"/restoticketmod", TicketResponse),
    (r"/changestatus", TicketChangeStatus),
    (r".*", DefaultHandler)
]