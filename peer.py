#!/usr/bin/env python
# -*-encoding:utf-8-*-
from socket import *
import sys
import threading

def handle_msg(sock):
    while True:
       data, addr = sock.recvfrom(128)
       print addr, data
       respond = data.split()
       if respond[0] == "punch_from":
           p_addr = respond[1]
           p_port = int(respond[2])
           sock.sendto("punch_ack", (p_addr, p_port))
       elif respond[0] == "punch_ack":
           print 'UDP hole punched ok to {}:{}'.format(addr[0],addr[1])

def run_console(sock, server_addr):
    while(True):
        try:
            line = raw_input('>>>')
            cmd = line.split()
            if len(cmd) < 1:
                continue;
            if(cmd[0] == 'list'):
                sock.sendto('list', server_addr)
            elif(cmd[0] == 'punch'):
                p_host = cmd[1]
                p_port = int(cmd[2])
                peer_msg = 'punch_syn '
                serv_msg = 'punch ' + cmd[1] + ' ' + cmd[2]
                sock.sendto(peer_msg, (p_host, p_port))
                sock.sendto(serv_msg, server_addr)
            elif(cmd[0] == 'send'):
                p_host = cmd[1]
                p_port = int(cmd[2])
                p_msg = cmd[3]
                sock.sendto(p_msg, (p_host, p_port))
            elif(cmd[0] == 'quit'):
                break;

        except Exception as e:
            print 'Input error:' + str(e)

        


if __name__ == '__main__':

    if(len(sys.argv) != 3):
        print 'Usage:{} <server-host> <server-port>'.format(sys.argv[0])
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    server_addr = (host, port)
    
    sock = socket(AF_INET, SOCK_DGRAM)
    # to support two peers on the same machine
    try:
       sock.bind(('', 9900))
    except:
       sock.bind(('', 9901))
    
    recvThread = threading.Thread(target=handle_msg, args=(sock,))
    recvThread.daemon = True
    recvThread.start()
    run_console(sock, server_addr)
    
