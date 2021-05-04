import time
from socketserver import BaseRequestHandler, ThreadingUDPServer, ThreadingTCPServer
import sys
import threading
import traceback
from resolver import create_response


class DNSServer():
    def __init__(self, address, port):
        self.servers = [ThreadingUDPServer((address, port), UDPHandler),
                        ThreadingTCPServer((address, port), TCPHandler), ]

    def start(self):
        for server in self.servers:
            threading.Thread(target=server.serve_forever, daemon=True).start()

    def main_loop(self):
        try:
            while True:
                time.sleep(.5)
                sys.stderr.flush()
                sys.stdout.flush()
        except KeyboardInterrupt:
            pass
        finally:
            for server in self.servers:
                server.shutdown()


class Server(BaseRequestHandler):
    def handle(self):
        try:
            self.send_data(create_response(self.get_data()))
        except Exception as e:
            print('Failed to process request', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


class TCPHandler(Server):
    def get_data(self):
        buff = self.request.recv(8192).strip()
        buff_size, size_filed, data = len(buff) - 2, int(buff[:2].hex(), 16), buff[2:]
        if buff_size != size_filed: raise Exception("Invalid TCP packet")
        return data[2:]

    def send_data(self, data):
        return self.request.sendall(bytes.fromhex(hex(len(data))[2:].zfill(4)) + data)


class UDPHandler(Server):
    def get_data(self):
        return self.request[0]

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


if __name__ == '__main__':
    print("Starting TinyDNS nameserver..")
    server = DNSServer('127.0.0.1', 5053)
    server.start()
    print("TinyDNS server running...")
    server.main_loop()
