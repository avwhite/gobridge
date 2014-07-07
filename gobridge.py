import telnetlib, sys, time, argparse

class ListMachine(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def first_state(self): return self.password_state
        
    def password_state(self, code, msg):
        if code == '1' and msg == '1':
            self.conn.write((self.password + '\r\n').encode())
            return self.listgames_state
        return self.password_state

    def listgames_state(self, code, msg):
        if code == '1' and msg == '5':
            self.conn.write(('games' + '\r\n').encode())
            return self.printgames_state
        return self.listgames_state

    def printgames_state(self, code, msg):
        if code == '7':
            print(msg)
            return self.printgames_state
        if code == '1' and msg == '5':
            self.conn.write('quit\r\n'.encode())
            self.conn.close()
            sys.exit()

class ObserveMachine(object):
    def __init__(self, username, password, gamenum):
        self.gamenum = gamenum
        self.username = username
        self.password = password

    def first_state(self): return self.password_state
        
    def password_state(self, code, msg):
        if code == '1' and msg == '1':
            self.conn.write((self.password + '\r\n').encode())
            return self.observegame_state
        return self.password_state

    def observegame_state(self, code, msg):
        if code == '1' and msg == '5':
            self.conn.write(('moves ' + self.gamenum + '\r\n').encode())
            self.conn.write(('observe ' + self.gamenum + '\r\n').encode())
            return self.observing_state
        return self.observegame_state

    def observing_state(self, code, msg):
        if code == '22':
            print('Game over. Awaiting result')
            return self.result_state
        elif code == '15':
            print(msg)
        return self.observing_state

    def result_state(self, code, msg):
        if code == '9':
            print(msg)
            print('Game over')
            self.conn.write('quit\r\n'.encode())
            self.conn.close()
            sys.exit()
        return self.result_state
    
if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("username")
    arg_parser.add_argument("password")

    subparsers = arg_parser.add_subparsers(
        description='use -h to see usage for the diffferent commands',
        title='subcommands')
    parser_list = subparsers.add_parser('list', help='list games on IGS')
    parser_list.set_defaults(command='list')
    parser_observe = subparsers.add_parser('observe', help='Relay a game from IGS to GOS')
    parser_observe.add_argument('gamenum', help='The game number on IGS')
    parser_observe.set_defaults(command='observe')

    arg_parser.parse_args()

    args = arg_parser.parse_args()

    if args.command == 'list':
        m = ListMachine(args.username, args.password)
    elif args.command == 'observe':
        m = ObserveMachine(args.username, args.password, args.gamenum)

    while True:
        host = "igs.joyjoy.net"
        port = 6969
        m.conn = telnetlib.Telnet(host, port)
        print('Connected to remote host')

        m.conn.read_until('Login:'.encode())
        m.conn.write((m.username + '\r\n').encode())
 
        state = m.first_state()
        while True:
            try:
                resp = m.conn.read_until('\r\n'.encode()).decode()
                (code, _, msg) = resp.partition(' ')
                state = state(code.strip(), msg.strip())
            except EOFError:
                m.conn.close()
                print('Disconnected from IGS.')
                print('Trying to reconnect')
                break
