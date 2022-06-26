# FTP server to serve a folder in convenience to connect with mobile client
from os import getcwd, getenv, path, system, chdir

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


# Global variables
HOST = '192.168.43.8'
PORT = 2121

USERS = {}  # id: password

ROOT_DIR = getenv('USERPROFILE') + path.join("\\Downloads")


# Main SERVER
def SERVER():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('user', '12345', ROOT_DIR, perm='elradfmwMT')
    # authorizer.add_anonymous(ROOT_DIR)

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "The FTP server is ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    # handler.masquerade_address = '151.25.42.11'
    # handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = (HOST, PORT)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()


# Action thread
def action():
    while True:
        command = input("SERVER Command $_ ").strip().lower()

        if command:
            if command in ['h', 'help', '--h', '-h', '-?', '--?', '?']:
                print('''\n  Available Commands:
    h         : Help.
    cd        : Show current directory path.
    cd <path> : Change directory to <path>.
    dir       : List of files and directories in current directory.
    root      : Make the current directory to be as root dir for the FTP server.
    --x       : [❗] STOP the ftp SERVER and quit.\n''')

            elif command in ['cd', 'dir', 'root']:
                if not command == 'root':
                    system(command)
                    print()
                else:
                    # Updating the ROOT directory
                    global ROOT_DIR
                    ROOT_DIR = getcwd()
                    print(f"OK. Now '{getcwd()}' is serving as the server's root directory.\n")

            elif len(command.split()) == 2 and command.split()[0] == 'cd':
                if path.exists(command.split()[1]):
                    chdir(command.split()[1])
                else:
                    print(f"Path <{command.split()[1]}> doesn't exists.\n"
                          f"Check the case-sensitive path or try another.\n")

            elif command == '--x':
                _ = input("[❗ WARNING] This will STOP the server and exit.\n"
                          "Are you sure to proceed? [Y/N] ").strip()
                print()
                if _ == 'Y':
                    print("Terminating the SERVER...")
                    # break
                    return None

            else:
                print(f"Invalid Command. '{command}' is not recognized as an internal command.")


if __name__ == '__main__':
    SERVER()
    print("Exiting FTP SERVER ADMIN...")
