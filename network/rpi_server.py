from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

import logging
import threading

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M:%S')
logger = logging.getLogger(__name__)


# Test:


@dispatcher.add_method
def echo(echo_msg):
    logger.debug("echo: {}".format(echo_msg))
    return echo_msg


@dispatcher.add_method
def op_test(a, b):
    return a * 10 + b

# Actuators:


@dispatcher.add_method
def move_forward(distance_mm):
    logger.debug("move_forward: {}mm".format(distance_mm))


@dispatcher.add_method
def move_backwards(distance_mm):
    logger.debug("move_backwards: {}mm".format(distance_mm))


@dispatcher.add_method
def open_gripper(timeout_ms=None):
    logger.debug("open_gripper: {}ms".format(timeout_ms))
    if timeout_ms is not None:
        threading.Timer(timeout_ms / 1000.0, stop_gripper).start()


@dispatcher.add_method
def close_gripper(timeout_ms=None):
    logger.debug("close_gripper: {}ms".format(timeout_ms))
    if timeout_ms is not None:
        threading.Timer(timeout_ms / 1000.0, stop_gripper).start()


@dispatcher.add_method
def stop_gripper():
    logger.debug("stop_gripper")

# Sensors:


@dispatcher.add_method
def fetch_sensor_data():
    logger.debug("fetch_sensor_data")
    return dict(accelerometer=[1, 2, 3], ultrasound_distance_mm=0.50)


@Request.application
def rpi_server(request):
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, rpi_server)
