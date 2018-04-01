#Source: https://github.com/alexbers/substitution_cipher_solver
import copy
import re
from itertools import combinations
import os

try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans

MAX_GOODNESS_LEVEL = 7  # 1-7
MAX_BAD_WORDS_RATE = 0.06

ABC = "abcdefghijklmnopqrstuvwxyz"


class WordList:
    MAX_WORD_LENGTH_TO_CACHE = 8

    def __init__(self, max_word_len=MAX_WORD_LENGTH_TO_CACHE):
        # words struct is
        # {(length,different_chars)}=[words] if len > MAX_WORD_LENGTH_TO_CACHE
        # {(length,different_chars)}=set([words and templates]) else

        self.words = {}
        for goodness in range(MAX_GOODNESS_LEVEL):
            for word in open(os.path.dirname(os.path.realpath(__file__)) + "/words/" + str(goodness) + ".txt"):
                word = word.strip()
                word_len = len(word)
                properties = (word_len, len(set(word)))

                if word_len > max_word_len:
                    words = self.words.get(properties, [])
                    words.append(word)
                    self.words[properties] = words
                else:
                    # add all possible combinations of the word and dots
                    words = self.words.get(properties, set([]))
                    for i in range(word_len + 1):
                        for dots_positions in combinations(range(word_len), i):
                            adding_word = list(word)
                            for j in dots_positions:
                                adding_word[j] = '.'

                            words.add(''.join(adding_word))
                    self.words[properties] = words

    def find_word_by_template(self, template, different_chars, max_len_word=MAX_WORD_LENGTH_TO_CACHE):
        """ Finds the word in the dict by template. Template can contain
        alpha characters and dots only """

        properties = (len(template), different_chars)
        if properties not in self.words:
            return False

        words = self.words[properties]

        if properties[0] > max_len_word:
            template = re.compile(template)

            for word in words:
                if template.match(word):
                    return True
        else:
            if template in words:
                return True
        return False


class KeyFinder:
    def __init__(self, enc_words, max_len_word=WordList.MAX_WORD_LENGTH_TO_CACHE, max_bad_words_rate=MAX_BAD_WORDS_RATE):
        self.points_threshhold = int(len(enc_words) * max_bad_words_rate)
        self.dict_wordlist = WordList(max_len_word)
        self.enc_words = enc_words
        self.different_chars = {}
        self.found_keys = {}  # key => bad words
        self.max_len_word = max_len_word
        for enc_word in enc_words:
            self.different_chars[enc_word] = len(set(enc_word))

    def get_key_points(self, key):
        """ The key is 26 byte alpha string with dots on unknown places """

        trans = maketrans(ABC, key)
        points = 0

        for enc_word in self.enc_words:
            different_chars = self.different_chars[enc_word]
            translated_word = enc_word.translate(trans)

            if not self.dict_wordlist.find_word_by_template(translated_word,
                                                            different_chars, self.max_len_word):
                points += 1
        return points

    def recursive_calc_key(self, key, possible_letters, level, verbosity=0, modulo_level_to_print_verbosity_1=5):
        """ Tries to place a possible letters on places with dots """
        if verbosity >= 2:
            print("Level: %3d, key: %s" % (level, key))
        elif verbosity == 1:
            if level % modulo_level_to_print_verbosity_1 == 0:
                print("Level: %3d, key: %s" % (level, key))

        if '.' not in key:
            points = self.get_key_points(key)
            if verbosity == 3:
                print("Found: %s, bad words: %d" % (key, points))
            self.found_keys[key] = points
            return

        nextpos = -1  # a pos with a minimum length of possible letters
        minlen = len(ABC) + 1

        for pos in range(len(ABC)):
            if key[pos] == ".":
                for letter in list(possible_letters[pos]):
                    new_key = key[:pos] + letter + key[pos + 1:]

                    if self.get_key_points(new_key) > self.points_threshhold:
                        possible_letters[pos].remove(letter)
                        if not possible_letters[pos]:
                            return

                if len(possible_letters[pos]) < minlen:
                    minlen = len(possible_letters[pos])
                    nextpos = pos

        while possible_letters[nextpos]:
            letter = possible_letters[nextpos].pop()
            new_possible_letters = copy.deepcopy(possible_letters)
            for pos in range(len(ABC)):
                new_possible_letters[pos] -= set([letter])
            new_possible_letters[nextpos] = set([letter])
            new_key = key[:nextpos] + letter + key[nextpos + 1:]
            self.recursive_calc_key(new_key, new_possible_letters, level + 1, verbosity, modulo_level_to_print_verbosity_1)

    def find(self, verbosity=0, modulo_level_to_print_verbosity_1=5):
        if not self.found_keys:
            possible_letters = [set(ABC) for i in range(len(ABC))]
            self.recursive_calc_key("." * len(ABC), possible_letters, 1, verbosity, modulo_level_to_print_verbosity_1)
        return self.found_keys


