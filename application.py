from threading import Thread
from cv.context import ContextManager
from cv.conversation import Conversation
from cv.listen import ListenManager, InputSentence
from cv.talk import TalkManager
from ws.ws import WebSocketServer
from rest.server import DisMusRest
import logging


def channel_flow(channel, conversation):
    """

    :param RxWebSocketProtocol channel:
    :param listen:
    :param talk:
    """
    print('NEW channel', channel)

    context_manager = ContextManager()
    my_conversation = Conversation.load_from_json(conversation, context_manager)
    listen = ListenManager(my_conversation)
    talk = TalkManager(my_conversation)

    channel.get_message_stream().map(
        lambda msg: InputSentence.build(msg)
    ).map(
        lambda sentence: listen.interpret(sentence)
    ).subscribe(
        lambda response: talk.say(channel, response)
    )

    talk.start(channel)


def main():
    # logging.basicConfig(filename='cv.log', format='%(asctime)s %(message)s', level=logging.INFO)

    with open('res/dismus.json', encoding='utf-8') as f:
        conversation_json = f.read()

    ws = WebSocketServer()
    ws.debug = True

    ws.get_client_stream().subscribe(
        lambda channel: channel_flow(channel, conversation_json)
    )

    ws_server = Thread(target=ws.run)
    ws_server.start()

    api = DisMusRest(ContextManager())

    api_server = Thread(target=api.run)
    api_server.start()


if __name__ == '__main__':
    main()




