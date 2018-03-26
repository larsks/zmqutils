import click
import logging
import sys
import zmq

LOG = logging.getLogger(__name__)


@click.command()
@click.option('-i', '--input', type=click.File('rb'),
              default=sys.stdin.buffer)
@click.option('-b', '--bufsize', type=int, default=1024)
@click.option('-l', '--listen', is_flag=True)
@click.option('-v', '--verbose', 'loglevel', flag_value='INFO', default=True)
@click.option('-q', '--quiet', 'loglevel', flag_value='WARNING')
@click.argument('target')
def cli(input, bufsize, listen, loglevel, target):
    logging.basicConfig(level=loglevel)

    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)

    if listen:
        LOG.info('listening on %s', target)
        sock.bind(target)
    else:
        LOG.info('connecting to %s', target)
        sock.connect(target)

    LOG.info('sending data')
    while True:
        data = input.read(bufsize)
        if not data:
            break
        sock.send(data)

    LOG.info('closing sockets')
    sock.close()
    ctx.term()

    LOG.info('finished sending')
