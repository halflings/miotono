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
def move(distance_mm):
    logger.debug("move: {}mm".format(distance_mm))


@dispatcher.add_method
def turn(angle_radians):
    logger.debug("turn: {}rad".format(angle_radians))


@dispatcher.add_method
def open_gripper(width_mm):
    logger.debug("open_gripper: {}mm".format(width_mm))


@dispatcher.add_method
def close_gripper(width_mm):
    logger.debug("close_gripper: {}mm".format(width_mm))


@dispatcher.add_method
def play_notes():
    logger.debug("play_notes")

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
