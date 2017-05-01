from abc import ABC
import jsonpickle
import json
from rx import Observable
from cv.conversation.conversation_graph import ChoiceAnswer, Question, Node

__author__ = 'Flavio Ferrara'


class TalkManager():
    def __init__(self, conversation):
        self.conversation = conversation

    def say(self, channel, messages):
        """
        The most important method of TalkManager.
        Will output messages to channel.
        :param channel:
        :param List messages: List of DTOs
        """
        print('say {} nodes to {}'.format(len(messages), channel))

        for message in messages:
            data = json.dumps(message.toDTO()).encode('utf8')
            channel.sendMessage(data)

    def start(self, channel):
        nodes = self.conversation.continue_topic()
        print(nodes)
        self.say(channel, nodes)