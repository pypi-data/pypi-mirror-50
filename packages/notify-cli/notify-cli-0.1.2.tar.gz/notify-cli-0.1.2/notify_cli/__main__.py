import json
import logging
import sys
from argparse import ArgumentParser

from notify_cli.notify_client import NotifyClient

logger = logging.getLogger('notify_cli')


def main():
    parser = ArgumentParser(description='Tool to subscribe to notifications from notify-server')
    parser.add_argument('server', help='Server address to connect to (ie. localhost:8080)')
    subparsers = parser.add_subparsers(dest='action')
    send_parser = subparsers.add_parser('send')
    send_parser.add_argument('event', help='Event type to send')
    send_parser.add_argument('data', help='Data to send with event', nargs='?')
    receive_parser = subparsers.add_parser('receive')
    receive_parser.add_argument('event', help='Event to subscribe to')
    args = parser.parse_args()

    stdout = sys.stdout
    if not sys.stdout.isatty():
        sys.stdout = sys.stderr

    try:
        host, port = args.server.split(':')
        port = int(port)
    except ValueError:
        parser.error('Invalid server address')
        raise SystemExit(1)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%y-%m-%d %H:%M:%S'
    )
    try:
        client = NotifyClient(host, port)
    except ConnectionRefusedError:
        logger.error('Failed to connect to server at {}:{}'.format(host, port))
        raise SystemExit(2)

    if args.action == 'send':
        if args.data is None:
            if not sys.stdin.isatty():
                data = sys.stdin.read().strip()
            else:
                data = ''
        else:
            data = args.data
        try:
            data = json.loads(data)
        except ValueError:
            pass
        client.send(args.event, data)
        logger.info('Sent: {}'.format({'event': args.event, 'data': data}))
    else:
        def on_event(event):
            if sys.stdout.isatty():
                logger.info('{}: {}'.format(event['event'], event['data']))
            else:
                stdout.write(json.dumps(event['data']))
                stdout.flush()

        client.subscribe(args.event, on_event)
        try:
            client.connection_lost_event.wait()
        except KeyboardInterrupt:
            print()
        finally:
            if client.connection_lost_event.is_set():
                logger.error('Server connection lost')
            else:
                client.unsubscribe(args.event, on_event)


if __name__ == '__main__':
    main()
