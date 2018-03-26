import click
import logging
import sys
import zmq

LOG = logging.getLogger(__name__)


@click.command()
@click.option('-o', '--output', type=click.File('wb'),
              default=sys.stdout.buffer)
@click.option('-l', '--listen', is_flag=True)
@click.option('-s', '--subscribe', multiple=True)
@click.option('-v', '--verbose', 'loglevel', flag_value='INFO', default=True)
@click.option('-q', '--quiet', 'loglevel', flag_value='WARNING')
@click.argument('target')
def cli(output, listen, subscribe, loglevel, target):
    logging.basicConfig(level=loglevel)

    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)

    if subscribe:
        for s in subscribe:
            LOG.info('subscribing to %s', s)
            sock.subscribe(s)
    else:
        LOG.info('subscribing to all messages')
        sock.subscribe('')

    if listen:
        LOG.info('listening on %s', target)
        sock.bind(target)
    else:
        LOG.info('connecting to %s', target)
        sock.connect(target)

    LOG.info('start receiving')
    while True:
        data = sock.recv()
        output.write(data)
    LOG.info('finished receiving')
