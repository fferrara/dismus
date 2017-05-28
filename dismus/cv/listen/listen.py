import json
import logging

from dismus.cv.listen.luis import LUISHandler
from dismus.shared.exceptions import LabelNotFoundException


__author__ = 'Flavio Ferrara'


class InputSentence:
    def __init__(self, _type, text):
        self.type = _type
        self.text = text

    @property
    def sentence_type(self):
        return self.type.upper()

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
    def __init__(self, conversation, intent_handler=None):
        """

        :param Conversation conversation: The conversation object
        """
        self.conversation = conversation
        if intent_handler is not None:
            self.intent_handler = intent_handler
        else:
            self.intent_handler = LUISHandler()

        self.sentence_handlers = {
            'CHOICE': self._handle_choice,
            'LIKE': self._handle_like,
            'MESSAGE': self._handle_message
        }

    def interpret(self, sentence):
        """
        The most important method of ListenManager.
        Will extract Intents, Choices and Entities from text returning an InterpretedText.
        :rtype : InterpretedText
        :param InputSentence sentence: a sentence from the user
        """
        print('interpret {}'.format(sentence.text))

        handler = self.sentence_handlers[sentence.sentence_type]
        return handler(sentence)

    def _handle_choice(self, sentence):
        try:
            node = self.conversation.get_choice_reply(sentence.text)
            return self.conversation.continue_topic(node)
        except LabelNotFoundException:
            logging.warning('Label not found while processing {}'.format(sentence.text))
            return []

    def _handle_like(self, sentence):
        return self.conversation.like_artist(sentence.text)

    def _handle_message(self, sentence):
        if self.conversation.current_node().has_trigger():
            return self.conversation.execute_trigger(self.conversation.current_node().trigger, sentence.text)

        try:
            response = self.intent_handler.process_sentence(sentence)
            node = self.conversation.get_intent_reply(response)
            return self.conversation.continue_topic(node)
        except LabelNotFoundException:
            logging.warning('Label not found while processing {}'.format(sentence.text))
            return []

