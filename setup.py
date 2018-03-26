from setuptools import setup, find_packages


def read(path):
    with open(path) as fd:
        return fd.read().splitlines()


setup(
    name='zmqutils',
    version=0.1,
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='http://github.com/larsks/zmqutils',
    packages=find_packages(),
    install_requires=read('requirements.txt'),
    entry_points={
        'console_scripts': [
            'zmq-send = zmqutils.cmd.zmqsend:cli',
            'zmq-recv = zmqutils.cmd.zmqrecv:cli',
        ]
    }
)
