from abc import ABC, abstractmethod
import json
from typing import List
from dismus.cv.conversation.conversation import Conversation
from dismus.shared.dialogue import Utterance

__author__ = 'Flavio Ferrara'


class TalkAble(ABC):
    # noinspection PyTypeChecker
    @abstractmethod
    def say(self, channel, messages: List[Utterance]):
        """
        The most important method of TalkManager.
        Will output messages to channel.
        :param channel:
        :param List messages: List of Utterances
        """
        raise NotImplementedError()


class TalkManager(TalkAble):
    def __init__(self, conversation: Conversation):
        self.conversation = conversation

    # noinspection PyTypeChecker
    def say(self, channel, messages: List[Utterance]):
        print('say {} nodes to {}'.format(len(messages), channel))

        for message in messages:
            data = json.dumps(message.serialize()).encode('utf8')
            channel.sendMessage(data)

    def start(self, channel):
        nodes = self.conversation.continue_topic()
        self.say(channel, nodes)