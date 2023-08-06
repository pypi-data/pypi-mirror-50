import atexit
from argparse import ArgumentParser
from threading import Event

from notify_server.event_system import EventSystem
from notify_server.socket_server import SocketServer


def main():
    parser = ArgumentParser(description='A server to transfer notifications')
    parser.add_argument('server_address', help='The address to host the socket server')
    args = parser.parse_args()
    try:
        socket_host, socket_port = args.server_address.split(':')
        socket_port = int(socket_port)
    except ValueError:
        parser.error('Invalid server address')
        raise SystemExit(1)

    event_system = EventSystem()
    socket_server = SocketServer(socket_host, socket_port, event_system)
    socket_server.start()
    atexit.register(socket_server.stop)

    try:
        Event().wait()
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
