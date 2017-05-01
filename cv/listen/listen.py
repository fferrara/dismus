import json
import logging
from cv.listen.luis import LUISHandler
from shared.exceptions import LabelNotFoundException
from ..conversation import Conversation

__author__ = 'Flavio Ferrara'


class InputSentence:
    def __init__(self, _type, text):
        self.type = _type
        self.text = text

    def isChoice(self):
        return self.type.upper() == 'CHOICE'

    @staticmethod
    def build(asJson):
        try:
            asDict = json.loads(asJson)
        except json.decoder.JSONDecodeError:
            raise ValueError('Not JSON. I only get JSON!')

        if 'type' not in asDict or 'text' not in asDict:
            raise ValueError('Invalid sentence')

        return InputSentence(asDict['type'], asDict['text'])


class ListenManager():
    def __init__(self, conversation, handler=None):
        """

        :param Conversation conversation: The conversation object
        """
        self.conversation = conversation
        if handler is not None:
            self.handler = handler
        else:
            self.handler = LUISHandler()

    def interpret(self, sentence):
        """
        The most important method of ListenManager.
        Will extract Intents, Choices and Entities from text returning an InterpretedText.
        :rtype : InterpretedText
        :param string text:
        """
        print('interpret {}'.format(sentence.text))

        if self.conversation.current_node().has_trigger():
            trigger = self.conversation.current_node().trigger
            trigger_messages = self.conversation.execute_trigger(trigger, sentence.text)
            node = self.conversation.next_node()
            trigger_messages.append(node)
            return trigger_messages

        try:
            if sentence.isChoice():
                node = self.conversation.get_choice_reply(sentence.text)
            else:
                response = self.handler.process_sentence(sentence)
                node = self.conversation.get_intent_reply(response)
        except LabelNotFoundException:
            logging.warning('Label not found while processing {}'.format(sentence.text))
            return []

        return self.conversation.continue_topic(node)