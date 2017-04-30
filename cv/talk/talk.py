from abc import ABC
import jsonpickle
import json
from rx import Observable
from cv.conversation.conversation_graph import ChoiceAnswer, Question

__author__ = 'Flavio Ferrara'


class Message(ABC):
    def __init__(self, text, message_type):
        self.text = text
        self.type = message_type

    def __repr__(self):
        return json.dumps({
            'type': self.type,
            'text': self.text
        })

    @staticmethod
    def from_node(node):
        if isinstance(node, Question):
            return QuestionMessage(node)
        else:
            return SimpleMessage(node)


class SimpleMessage(Message):
    def __init__(self, node):
        """

        :param Node node:
        """
        super().__init__(node.message, 'MESSAGE')


class QuestionMessage(Message):
    def __init__(self, question_node):
        """

        :param question: Question
        """
        super().__init__(question_node.question, 'QUESTION')
        self.choices = [a.choice for a in question_node.answers if isinstance(a, ChoiceAnswer)]

    def __repr__(self):
        d = {
            'type': self.type,
            'text': self.text
        }
        if self.choices is not None:
            d['choices'] = self.choices

        return json.dumps(d)


class TalkManager():
    def __init__(self, conversation):
        self.conversation = conversation

    def say(self, channel, nodes):
        """
        The most important method of TalkManager.
        Will output messages contained in nodes to channel.
        :param channel:
        :param List nodes: List of nodes
        """
        print('say {} nodes to {}'.format(len(nodes), channel))

        messages = [Message.from_node(node) for node in nodes]

        for message in messages:
            data = jsonpickle.encode(message, unpicklable=False).encode('utf8')
            channel.sendMessage(data)

    def start(self, channel):
        nodes = self.conversation.continue_topic()
        print(nodes)
        self.say(channel, nodes)
