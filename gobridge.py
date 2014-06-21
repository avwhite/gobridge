import telnetlib, sys, time

class StateMachine(object):
    def __init__(self, username, password, gamenum):
        self.gamenum = gamenum
        self.username = username
        self.password = password

    def run(self):
        host = "igs.joyjoy.net"
        port = 6969
        self.conn = telnetlib.Telnet(host, port)
        print('Connected to remote host')

        self.conn.read_until('Login:'.encode())
        self.conn.write((self.username + '\r\n').encode())

        state = self.password_state
        while True:
            (code, _, msg) = self.conn.read_until('\r\n'.encode()).decode().partition(' ')
            state = state(code.strip(), msg.strip())
        
    def password_state(self, code, msg):
        #print('entering password state', code, msg, file=sys.stderr)
        if code == '1' and msg == '1':
            print('ehj')
            self.conn.write((self.password + '\r\n').encode())
            return self.observegame_state
        return self.password_state

    def observegame_state(self, code, msg):
        #print('entering observegame state', self.gamenum, file=sys.stderr)
        if code == '1' and msg == '5':
            self.conn.write(('moves ' + self.gamenum + '\r\n').encode())
            self.conn.write(('observe ' + self.gamenum + '\r\n').encode())
            return self.observing_state
        return self.observegame_state

    def observing_state(self, code, msg):
        #print('entering observing state', code, msg, file=sys.stderr)
        if code == '22':
            print('Game over. Awaiting result')
            return self.result_state
        elif code == '15':
            print(msg)
        return self.observing_state

    def result_state(self, code, msg):
        #print('entering result state', file=sys.stderr)
        if code == '9':
            print(msg)
            print('Game over')
            conn.write('quit\r\n'.encode())
            conn.close()
            sys.exit()
        return self.result_state
    
if __name__ == "__main__":
    m = StateMachine(sys.argv[1], sys.argv[2], sys.argv[3])
    m.run()
