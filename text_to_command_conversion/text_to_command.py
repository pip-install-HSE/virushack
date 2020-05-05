from typing import List

from word2vec import load
from config import *
from .command_to_kos import morph


def most_common(lst):
    res = dict((lst.count(i), i) for i in set(lst))
    return res[max(res.keys())]


class TextToCommand:
    def __init__(self, coefficient: int = 0.4):
        self.coefficient = coefficient
        print("Starting loading model for word2vec...")
        self.model = load(filename_start)
        print("Successfully loaded!")
        self.tags = ["VERB", "NOUN", "ADV", "DET", "ADJ", "SCONJ", "INTJ", "X", "NUM", "PART", "ADP", "PRON", "X"]
        self.commands = []

    def normalize_word(self, word):
        word = morph.parse(word.lower())[0].normal_form
        # print(word)
        norm_word = None
        for tag in self.tags:
            try:
                norm_word = self.model.similar(f'{word}_{tag}')
                norm_word = f"{word}_{tag}"
                break
            except KeyError:
                continue
        return norm_word

    def normalize_commands(self):
        tmp = []
        for command in self.commands:
            norm_command = self.normalize_word(command)
            if norm_command:
                tmp += [norm_command]
        self.commands = tmp

    def set_commands(self, commands):
        self.commands = commands
        self.normalize_commands()

    def get_command(self, text):
        normalized_words = [self.normalize_word(word) for word in text.split() if self.normalize_word(word)]
        most_similar_command_for_every_word = []
        for norm_word in normalized_words:
            indexes, metrics = self.model.similar(norm_word)
            similar_current_word_list = [item[0] for item in
                                         self.model.generate_response(indexes, metrics).tolist()] + \
                                        [norm_word]

            for command in self.commands:
                similar_current_command_list = []
                for word_similar in similar_current_word_list:
                    distance = self.model.distance(word_similar, command)[0]
                    # print(distance)
                    if distance[2] > self.coefficient:
                        similar_current_command_list.append(distance)
                if similar_current_command_list:
                    # print(similar_current_word_list)
                    similar_current_command_list.sort(key=lambda x: x[2])
                    most_similar_command_for_every_word.append(similar_current_command_list[0][1].split('_')[0])
                else:
                    most_similar_command_for_every_word.append(None)
        return [item for item in most_similar_command_for_every_word]

    # def get_command(self, text):
    #     normalized_words = [self.normalize_word(word) for word in text.split() if self.normalize_word(word)]
    #     most_similar_command_for_every_word = []
    #     for command in self.commands:
    #         for norm_word in normalized_words:
    #             indexes, metrics = self.model.similar(norm_word)
    #             similar_current_word_list = [item[0] for item in
    #                                          self.model.generate_response(indexes, metrics).tolist()] + \
    #                                         [norm_word]
    #             similar_current_command_list = []
    #             for word_similar in similar_current_word_list:
    #                 distance = self.model.distance(word_similar, command)[0]
    #                 # print(distance)
    #                 if distance[2] > self.coefficient:
    #                     similar_current_command_list.append(distance)
    #             if similar_current_command_list:
    #                 # print(similar_current_word_list)
    #                 similar_current_command_list.sort(key=lambda x: x[2])
    #                 most_similar_command_for_every_word.append(similar_current_command_list[0][1].split('_')[0])
    #             else:
    #                 most_similar_command_for_every_word.append(None)
    #     return [item for item in most_similar_command_for_every_word]

# text = 'взвеш'
# similar_current_word_list = ['']
# commands = ['взвесить', 'оплатить', "назад"]
# def get_command(self, text):
#     words = text.split()
#     normalized_words = [self.normalize_word(word) for word in words]
#     for i, word in enumerate(words):
#         for command in self.commands:
#             if word in command:
