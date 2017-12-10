from werkzeug.serving import run_simple

from rpi_server import rpi_server
from client import JsonRpcClient

import threading

server_thread = threading.Thread(target=lambda: run_simple('localhost', 4000, rpi_server))
server_thread.daemon = True
server_thread.start()
client = JsonRpcClient('http://localhost:4000')


def test_client():
    assert client.call('echo', 'some test_string! ') == 'some test_string! '
    assert client.call('op_test', 5, 1) == 51
