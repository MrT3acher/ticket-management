import http.client
import json
import urllib.parse
import argparse
from getpass import getpass

parser = argparse.ArgumentParser(description='Client program of ticket-management project')
parser.add_argument('--host', default='127.0.0.1', help='hostname')
parser.add_argument('--port', default=1104, help='port number of the server', type=int)
parser.add_argument('--verbose', default=False, type=bool)
args = parser.parse_args()

if args.verbose:
    print("[!] Working with %s:%i server" % (args.host, args.port))

token = ""
saved_username = ""
saved_password = ""

def request(function, params={}):
    connection = http.client.HTTPConnection(args.host, args.port)
    headers = {}

    available_requests = {
        'signup': 'POST',
        'login': 'POST',
        'logout': 'POST',
        'sendticket': 'POST',
        'getticketcli': 'GET',
        'closeticket': 'POST',
        'getticketmod': 'GET',
        'restoticketmod': 'POST',
        'changestatus': 'POST'
    }
    method = available_requests[function]

    if token != "":
        params['token'] = token
    url_params = urllib.parse.urlencode(params)

    if args.verbose:
        print("[!] %s request to /%s" % (available_requests[function], function))
        print("[!] request body: " + url_params)

    if method == 'POST':
        headers['Content-type'] = 'application/x-www-form-urlencoded'
        connection.request(method, '/' + function, url_params, headers)
    else:
        connection.request(method, '/' + function + '?' + url_params, headers=headers)

    response = connection.getresponse()
    response_text = response.read().decode()
    if args.verbose:
        print("[!] reponse: " + response_text)
    connection.close()
    return json.loads(response_text)

while token == "":
    what = input("""First you need to Signin or Signup: 
    1. Signin
    2. Signup
select: """)
    if what == '1':
        username = input("Enter username: ")
        saved_username = username
        password = getpass("Enter Password: ")
        saved_password = password
        response = request("login", {'username': username, 'password': password})
        if response['code'] == 200:
            print('[+] ' + response['message'])
        else:
            print('[X] ' + response['message'])
        try:
            token = response['token']
        except:
            pass
    elif what == '2':
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
        response = request("signup", {'username': username, 'password': password, 'firstname': firstname, 'lastname': lastname})
        if response['code'] == 200:
            print('[+] ' + response['message'])
        else:
            print('[X] ' + response['message'])

print("Enter help to see a list of commands available")

class Commands:
    @staticmethod
    def help():
        for key in commands.keys():
            print(" " + key)

    @staticmethod
    def logout():
        response = request("logout", {'username': saved_username, 'password': saved_password})
        if response['code'] == 200:
            print('[+] ' + response['message'])
        else:
            print('[X] ' + response['message'])
        exit()

    @staticmethod
    def sendticket():
        subject = input("Subject: ")
        body = input("Body: ")
        response = request("sendticket", {'subject': subject, 'body': body})
        if response['code'] == 200:
            print('[+] ' + response['message'])
        else:
            print('[X] ' + response['message'])

    @staticmethod
    def getticketcli():
        response = request('getticketcli')
        if response['code'] == 200:
            print('[+] ' + response['message'])
            for key in response:
                if key.find('block') != -1:
                    print("\t - " + str(response[key]))
        else:
            print('[X] ' + response['message'])

    @staticmethod
    def closeticket():
        id = input("Ticket id: ")
        response = request('closeticket', {'id': id})
        if response['code'] == 200:
            print('[+] ' + response['message'])
        else:
            print('[X] ' + response['message'])

    @staticmethod
    def getticketmod():
        response = request('getticketmod')
        if response['code'] == 200:
            print('[+] ' + response['message'])
            for key in response:
                if key.find('block') != -1:
                    print("\t - " + str(response[key]))
        else:
            print('[X] ' + response['message'])

    @staticmethod
    def restoticketmod():
        id = input("Ticket id to response to: ")
        body = input("Body of response: ")
        response = request('restoticketmod', {'id': id, 'body': body})
        if response['code'] == 200:
            print('[+] ' + response['message'])
        else:
            print('[X] ' + response['message'])

    @staticmethod
    def changestatus():
        id = input("Ticket id to change status: ")
        status = ''
        while status not in ['open', 'close', 'check']:
            status = input("New status (open/close/check): ")
        response = request('changestatus', {'id': id, 'status': status})
        if response['code'] == 200:
            print('[+] ' + response['message'])
        else:
            print('[X] ' + response['message'])


commands = {
    'help': Commands.help,
    'logout': Commands.logout,
    'sendticket': Commands.sendticket,
    'getticketcli': Commands.getticketcli,
    'closeticket': Commands.closeticket,
    'getticketmod': Commands.getticketmod,
    'restoticketmod': Commands.restoticketmod,
    'changestatus': Commands.changestatus
}

while 1:
    command = input("> ")

    try:
        commands[command]()
    except KeyError:
        print("[X] Wrong Command")
        continue
