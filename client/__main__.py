import http.client
import json
import argparse
from getpass import getpass

parser = argparse.ArgumentParser(description='Client program of ticket-management project')
parser.add_argument('--server', default='localhost:1104', help='server address')
args = parser.parse_args()

token = ""
saved_username = ""
saved_password = ""

def request(function, params):
    connection = http.client.HTTPConnection(args['server'])
    headers = {'Content-type': 'application/json'}

    available_requests = {
        'signup': 'POST',
        'login': 'POST',
        'logout': 'POST',
        'sendticket': 'POST',
        'getticketcli': 'GET',
        'closeticket': 'POST',
        'getticketmod': 'GET',
        'restoticketmod': 'POST',
        'chagestatus': 'POST'
    }

    if token != "":
        params['token'] = token
    json_params = json.dumps(params)
    connection.request(available_requests[function], '/' + function, json_params, headers)

    response = connection.getresponse().read().decode()
    print(response)
    connection.close()
    return json.loads(response)

while token == "":
    what = input("""First you need to Signin or Signup: 
    1. Signin
    2. Signup
        select: """)
    if what == 1:
        username = input("Enter username: ")
        saved_username = username
        password = getpass("Enter Password: ")
        saved_password = password
        response = request("login", {'username': username, 'password': password})
        try:
            token = response['token']
        except:
            pass
    elif what == 2:
        print("The fields with * are necessary")
        username = ""
        while username == "":
            username = input("Enter Username *: ")
            if username == "":
                print("[X] Username can`t be empty")
        password, passwordconfirm = "", ""
        while password == "" or password != passwordconfirm:
            password = getpass("Enter Password *: ")
            passwordconfirm = getpass("Confirm Password *: ")
            if password == "":
                print("[X] Password can`t be empty")
            if password != passwordconfirm:
                print("[X] Password and Confirm Password must be equal")
        firstname = input("Firstname: ")
        lastname = input("Lastname: ")
        request("signup", {'username': username, 'password': password, 'firstname': firstname, 'lastname': lastname})

print("Enter help to see a list of commands available")

class Commands:
    @staticmethod
    def help():
        for key in commands.keys():
            print(" " + key)

    @staticmethod
    def logout():
        request("logout", {'username': saved_username, 'password': saved_password})

    @staticmethod
    def sendticket():
        subject = input("Subject: ")
        body = input("Body: ")
        request("sendticket", {'subject': subject, 'body': body})

    @staticmethod
    def getticketcli():
        request('getticketcli')

    @staticmethod
    def closeticket():
        id = input("Ticket id: ")
        request('closeticket', {'id': id})

    @staticmethod
    def getticketmod():
        request('getticketmod')

    @staticmethod
    def restoticketmod():
        id = input("Ticket id to response to: ")
        body = input("Body of response: ")
        request('restoticketmod', {'id': id, 'body': body})

    @staticmethod
    def chagestatus():
        id = input("Ticket id to change status: ")
        status = ''
        while status not in ['open', 'close', 'check']:
            status = input("New status (open/close/check): ")
        request('chagestatus', {'id': id, 'status': status})


commands = {
    'help': Commands.help,
    'logout': Commands.logout,
    'sendticket': Commands.sendticket,
    'getticketcli': Commands.getticketcli,
    'closeticket': Commands.closeticket,
    'getticketmod': Commands.getticketmod,
    'restoticketmod': Commands.restoticketmod,
    'chagestatus': Commands.chagestatus
}

while 1:
    command = input("> ")

    commands[command]()