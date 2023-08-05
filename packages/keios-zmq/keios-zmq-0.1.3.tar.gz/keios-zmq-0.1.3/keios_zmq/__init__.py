import asyncio
import logging
from typing import Callable

import zmq

logging.basicConfig(level=logging.INFO)


class KeiosZMQ:
    """
    server wrapper for keios implementations
    TODO: refactor to threadpool based implementation
    """
    logger = logging.getLogger("keios-py-zmq-connector")

    def __init__(self, port: int, message_handler: Callable[[bytearray], bytearray]):
        self._zmq_context = zmq.Context()
        self._socket = self._zmq_context.socket(zmq.ROUTER)
        self._socket.bind("tcp://*:{}".format(port))
        self._socket.setsockopt(zmq.LINGER, 1)
        self._message_handler = message_handler
        self.stopped = False

    def internal_handler(self):
        while not self.stopped:
            try:
                addr, msg = self.internal_receive_message()
                self.logger.debug("msg received - identity: {}, data: {}".format(addr, msg))
                self.internal_send_message(addr, self._message_handler(msg, addr))
            except zmq.error.ContextTerminated as e:
                pass # this error is expected from .close()

    def internal_receive_message(self):
        """
        Wraps blocking zmq recv
        :return:
        """
        identity, data = self._socket.recv_multipart()
        return [identity, data]

    def internal_send_message(self, identity, message):
        return self._socket.send_multipart([identity,
                                            message])

    def start_server(self):
        self.internal_handler()

    def close(self):
        self.stopped = True
        self._socket.close()
        logger.info('Closed Server Socket')
        self._zmq_context.term()
        logger.info('Terminated Server Context')
