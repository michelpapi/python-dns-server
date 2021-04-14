import time
from socketserver import BaseRequestHandler, ThreadingUDPServer, ThreadingTCPServer
import sys
import threading
import traceback
from resolver import create_response


class Handler(BaseRequestHandler):
    def handle(self):
        try:
            self.send_data(create_response(self.get_data()))
        except Exception as e:
            print('Failed to process request', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


class TCPHandler(Handler):
    def get_data(self):
        data = self.request.recv(8192).strip()
        if len(data) - 2 != int(data[:2].hex(), 16): raise Exception("Invalid TCP packet")
        return data[2:]

    def send_data(self, data):
        return self.request.sendall(bytes.fromhex(hex(len(data))[2:].zfill(4)) + data)


class UDPHandler(Handler):
    def get_data(self):
        return self.request[0]

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


def start_servers():
    servers = [ThreadingUDPServer(('0.0.0.0', 53), UDPHandler),
               ThreadingTCPServer(('0.0.0.0', 53), TCPHandler),]
    for server in servers:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
    return servers


def main_loop(servers):
    try:
        while True:
            time.sleep(.5)
            sys.stderr.flush()
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.shutdown()


if __name__ == '__main__':
    print("Starting TinyDNS nameserver..")
    srvs = start_servers()
    print("TinyDNS server running...")
    main_loop(srvs)
