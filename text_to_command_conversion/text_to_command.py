from typing import List

from word2vec import load
from config import *
from pymorphy2 import MorphAnalyzer


def most_common(lst):
    res = dict((lst.count(i), i) for i in set(lst))
    return res[max(res.keys())]


class TextToCommand:
    def __init__(self, commands: List):
        self.morph = MorphAnalyzer()
        self.model = load(filename_start)
        self.commands = [self.normalize_word(command) for command in commands]

    def normalize_word(self, word):
        norm_word = self.morph.parse(word)[0]
        return f"{norm_word.normal_form}_{norm_word.tag.POS}"

    def get_command(self, text):
        words = text.split()
        normalized_words = [self.normalize_word(word) for word in words]
        most_similar_command_for_every_word = []
        for i, word in enumerate(words):
            indexes, metrics = self.model.similar(normalized_words[i])
            similar_current_word_list = self.model.generate_response(indexes, metrics).tolist()
            most_similar_command_for_every_word += most_common([(sorted([self.model.distance(similar, command)[0] for similar in similar_current_word_list], key=lambda x: x[2])[0]) for command in self.commands])
        return most_similar_command_for_every_word

# text = 'взвеш'
# similar_current_word_list = ['']
# commands = ['взвесить', 'оплатить', "назад"]
    # def get_command(self, text):
    #     words = text.split()
    #     normalized_words = [self.normalize_word(word) for word in words]
    #     for i, word in enumerate(words):
    #         for command in self.commands:
    #             if word in command:



