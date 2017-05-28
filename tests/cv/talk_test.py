import unittest
from unittest.mock import Mock, MagicMock
from dismus.cv.conversation.conversation import Conversation
from dismus.cv.talk.talk import TalkManager
from dismus.shared.dialogue import Utterance

__author__ = 'Flavio Ferrara'

class TestTalkManager(unittest.TestCase):
    def setUp(self):
        self.conversation = Mock(spec=Conversation)
        self.talk_manager = TalkManager(self.conversation)
        assert isinstance(self.talk_manager, TalkManager)

        self.channel = Mock()
        self.message = MagicMock(Utterance)
        self.message.serialize.return_value = {}

    def test_say(self):
        self.talk_manager.say(self.channel, [self.message])
        self.channel.sendMessage.assert_called_once_with(b'{}')

    def test_start(self):
        self.conversation.continue_topic.return_value = [self.message]

        self.talk_manager.start(self.channel)
        self.channel.sendMessage.assert_called_once_with(b'{}')


