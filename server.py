#!/usr/bin/env python
# -*-encoding:utf-8-*-
import socket
import sys
peers = {}
def handle_msg(sock):
    while(True):
        try:
            data, addr = sock.recvfrom(128)
            print addr, data
            peers[addr] = True
            cmd = data.split()
            if(cmd[0] == 'list'):
                peerlist = ''
                for peer in peers.keys():
                    if(peer == addr):
                        peerlist += '[*]'
                    peerlist += peer[0] + ' ' + str(peer[1]) + '\n'
                sock.sendto(peerlist, addr)
            elif(cmd[0] == 'punch'):
                msg = 'punch_from ' + addr[0] + ' ' + str(addr[1])
                punch_ip = cmd[1]
                punch_port = int(cmd[2])
                sock.sendto(msg, (punch_ip, punch_port))
        except KeyboardInterrupt:
            print 'Quiting...'
            break;
        except Exception as e:
            msg = 'Error:' + str(e)
            sock.sendto(msg, addr)

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 6666
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    elif len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        print 'Usage: {} [host] port'.format(sys.argv[0])
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    sock.bind((host, port));

    print 'Server running on {}:{}'.format(host, port)
    handle_msg(sock)

