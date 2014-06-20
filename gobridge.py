import telnetlib, sys, time

def skip_to_prompt(igs):
    (code, _, msg) = igs.read_until('\r\n'.encode()).decode().partition(' ')
    while code.isdigit() and int(code) == 1 and int(msg[0]) == 5:
        line = igs.read_until('\r\n'.encode()).decode()
    
if __name__ == "__main__":
     
     
    host = "igs.joyjoy.net"
    port = 6969
    gamenum = sys.argv[1]
     
    igs = telnetlib.Telnet(host, port)
     
    print('Connected to remote host')

    igs.read_until('Login:'.encode())
    igs.write('vwhite\r\n'.encode())

    observing = False

    while True:
        (code, _, msg) = igs.read_until('\r\n'.encode()).decode().partition(' ')
        if code.isdigit():
            icode = int(code)
            if icode == 1:
                code = int(msg[0])
                if code == 1:
                    igs.write('131172an\r\n'.encode())
                elif code == 5 and observing == False:
                    observing = True
                    igs.write(('moves ' + gamenum + '\r\n').encode())
                    igs.write(('observe ' + gamenum + '\r\n').encode())
            elif icode == 15:
                print(msg)
            elif icode == 22:
                print(msg)
            elif icode == 9:
                print(msg)

    igs.close()
     
#    while True:
#        data = s.read_eager().decode()
#        sys.stdout.write(data)
#            
#        msg = sys.stdin.readline()
#        s.write(msg.encode('utf-8'))
#
#        socket_list = [sys.stdin, s]
#         
#        # Get the list sockets which are readable
#        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
#         
#        for sock in read_sockets:
#            #incoming message from remote server
#            if sock == s:
#                data = sock.recv(4096)
#                if not data :
#                    print 'Connection closed'
#                    sys.exit()
#                else :
#                    #print data
#                    sys.stdout.write(data)
#             
#            #user entered a message
#            else :
#                msg = sys.stdin.readline()
#                s.send(msg)
