import click
import sys
import zmq


@click.command()
@click.option('-i', '--input', type=click.File('rb'), default=sys.stdin.buffer)
@click.option('-b', '--bufsize', type=int, default=1024)
@click.option('-l', '--listen', is_flag=True)
@click.argument('target')
def cli(input, bufsize, listen, target):
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUB)

    if listen:
        sock.bind(target)
    else:
        sock.connect(target)

    while True:
        sock.send(input.read(bufsize))
