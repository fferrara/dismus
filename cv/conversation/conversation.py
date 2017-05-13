import json

from cv.conversation.conversation_graph import IntentAnswer, ChoiceAnswer, Node, RandomMessageNode, Question, \
    IntentQuestion
from cv.conversation.intent import Intent, Entity
from ..context import ContextManager
from shared.exceptions import LabelNotFoundException


__author__ = 'Flavio Ferrara'


class Conversation:
    def __init__(self, story, context):
        """

        :param story:
        :param ContextManager context: The context object
        """
        self.story = story  # type: List
        self.context = context
        self.current_index = 0
        self.flags = {}

    def current_node(self) -> Node:
        """
        :return: Node
        """
        return self.story[self.current_index]

    def set_current_node(self, from_node):
        self.current_index = self.story.index(from_node)

    def is_flag_set(self, flag):
        return self.context.is_flag(flag)

    def like_artist(self, artist_id):
        hints = self.context.like_artist(artist_id)
        if not isinstance(hints, list):
            hints = [hints]
        return hints

    def execute_trigger(self, trigger, param):
        trigger_handler = getattr(self.context, trigger)
        trigger_result = trigger_handler(param)

        node = self.next_node()
        messages = self.continue_topic(node)

        return [trigger_result] + messages

    def next_node(self):
        try:
            next_index = self._find_node(self.current_node().next_label)
            self.current_index = next_index
            return self.story[next_index]
        except LabelNotFoundException:
            self.current_index += 1
            return self.story[self.current_index]

    def get_choice_reply(self, choice_sentence) -> Node:
        """

        :param choice_sentence: InputSentence
        :return: :raise ValueError:
        """
        if not isinstance(self.story[self.current_index], Question):
            raise ValueError('Current point in story is not a question')

        question = self.story[self.current_index]
        label = question.get_next(choice_sentence)

        return self.story[self._find_node(label)]

    def get_intent_reply(self, intent_response) -> Node:
        """

            :param intent_response: IntentResponse
            :return:
            """
        if not isinstance(self.story[self.current_index], Question):
            raise ValueError('Current point in story is not a question')

        question = self.story[self.current_index]
        label = question.get_next(intent_response)

        if label is None:
            label = self._get_global_handler(intent_response) or question.fallback

        return self.story[self._find_node(label)]

    def continue_topic(self, from_node=None):
        """
        Iterate the piece of conversation under the same label.
        Return the list of nodes found during iteration.
        If specified, iteration starts from the from_node Node.

        """
        nodes = []
        if from_node is not None:
            self.set_current_node(from_node)

        node = from_node or self.current_node()
        while node is not None:
            nodes.append(node)

            for setter in node.setters:
                self.context.set_flag(setter)

            if isinstance(node, Question):
                break
            node = self.next_node()

        return nodes

    def _find_node(self, label):
        """
        Return index of the node associated to label
        :param label: string
        :return: int
        """
        if label is None:
            raise LabelNotFoundException

        try:
            index = next(i for i, n in enumerate(self.story) if n.label == label)
            return index
        except StopIteration:
            raise LabelNotFoundException

    def _get_global_handler(self, intent_response):
        return 'Handle' + intent_response.intent.name

    @staticmethod
    def load_from_json(encoded, context):
        """
        Instantiate a Conversation object from a JSON string describing its structure
        :param encoded: The JSON string
        :return: :raise TypeError:
        """

        def build_answer(dict):
            if 'intent' in dict:
                return IntentAnswer(
                    dict['next'],
                    Intent(dict['intent']),
                    [Entity(e) for e in dict.get('entities', [])])
            elif 'choice' in dict:
                return ChoiceAnswer(
                    dict['next'],
                    dict['choice'])

        def create_node(dict):
            """
            Create a Node from a dictionary.
            It recursively creates the child Nodes and the Edges between them.
            :param dict:
            :return: The Node
            :rtype: Node
            """
            if 'm' in dict:
                # Is a simple Node
                node = Node(dict['m'], dict.get('label'), dict.get('next'))
            elif 'messages' in dict:
                # Node with multiple messages
                node = RandomMessageNode(dict['messages'], dict.get('label'))
            elif 'q' in dict:
                # Is a question
                if 'answers' not in dict and 'fallback' not in dict:
                    #raise ValueError('Each question must have answers or fallback')
                    # TODO: gestire
                    pass
                answers = 'answers' in dict and [build_answer(a) for a in dict['answers']] or []
                fallback = dict.get('fallback')
                node = IntentQuestion(dict['q'], fallback, answers, dict.get('label'))
            else:
                raise ValueError('Each line must be a message or a question')

            for setter in dict.get('setters', []):
                node.add_setter(setter)

            for checker in dict.get('checkers', []):
                node.add_checker(checker)

            node.set_trigger(dict.get('trigger', None))

            return node

        decoded = json.loads(encoded)

        story = [create_node(record) for record in decoded]
        return Conversation(story, context)


