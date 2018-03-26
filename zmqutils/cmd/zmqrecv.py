import click
import sys
import zmq


@click.command()
@click.option('-o', '--output', type=click.File('wb'), default=sys.stdout.buffer)
@click.option('-l', '--listen', is_flag=True)
@click.option('-s', '--subscribe', multiple=True)
@click.argument('target')
def cli(output, listen, subscribe, target):
    ctx = zmq.Context()
    sock = ctx.socket(zmq.SUB)

    if subscribe:
        for s in subscribe:
            sock.subscribe(s)
    else:
        sock.subscribe('')

    if listen:
        sock.bind(target)
    else:
        sock.connect(target)

    while True:
        output.write(sock.recv())
