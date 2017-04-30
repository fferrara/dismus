__author__ = 'Flavio Ferrara'

from functools import partial
import logging

import jsonpickle
from rx.core.py3.observable import Observable
from autobahn.asyncio import WebSocketServerProtocol, WebSocketServerFactory
import rx


asyncio = rx.config['asyncio']


class RxWebSocketProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self.factory = None

    def onConnect(self, request):
        logging.info("NEW CLIENT CONNECTING: {0}".format(request.peer))

    def onOpen(self):
        self.factory.init_client(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            logging.info("Binary message received: {0} bytes".format(len(payload)))
        else:
            logging.info("Text message received: {0}".format(payload.decode('utf8')))
            self.on_text_message(payload.decode('utf-8'))

    def get_message_stream(self):
        return Observable.create(self._create_obs)

    def _create_obs(self, observer):
        self.on_text_message = partial(observer.on_next)

class RxWebSocketServerFactory(WebSocketServerFactory):
    def __init__(self):
        WebSocketServerFactory.__init__(self)
        self._client_stream = Observable.create(self._create_obs)

    def _create_obs(self, observer):
        self.init_client = partial(observer.on_next)

    def get_client_stream(self):
        return self._client_stream