# @author: Colan Biemer

from random import random, shuffle
from colorama import Fore, Style
import math
import json

from . import RingBuffer

class NGram():
    def __init__(self, n):
        assert n >= 2

        self.n = n
        self.grammar = {}
        self.compiled_grammar = None

    def get(self, grammar_input):
        assert self.compiled_grammar != None
        grammar_input = json.dumps(grammar_input)
        assert grammar_input in self.compiled_grammar
        
        indexes = [i for i in range(len(self.compiled_grammar[grammar_input].keys()))]
        shuffle(indexes)

        required_weight = random()
        current_weight = 0

        for index in indexes:
            value = list(self.compiled_grammar[grammar_input].keys())[index]
            current_weight += self.compiled_grammar[grammar_input][value]

            if current_weight >= required_weight:
                return value

        raise EnvironmentError('This should not have happened')

    def get_most_likely(self, grammar_input):
        assert self.compiled_grammar != None
        grammar_input = json.dumps(grammar_input)
        assert grammar_input in self.compiled_grammar
        
        indexes = [i for i in range(len(self.compiled_grammar[grammar_input].keys()))]
        most_likely_percent = 0
        most_likely_value = None

        for index in indexes:
            value = list(self.compiled_grammar[grammar_input].keys())[index]

            if self.compiled_grammar[grammar_input][value] > most_likely_percent:
                most_likely_percent = self.compiled_grammar[grammar_input][value]
                most_likely_value = value

        raise most_likely_value

    def compile(self, weighted=True):
        self.compiled_grammar = {}

        for key in self.grammar:
            self.compiled_grammar[key] = {}
            
            occurrences = 0
            for value in self.grammar[key]:
                if weighted:
                    occurrences += self.grammar[key][value]
                else:
                    self.compiled_grammar[key][value] =  1 / float(len(self.grammar[key]))

            if weighted:
                for value in self.grammar[key]:
                    self.compiled_grammar[key][value] = self.grammar[key][value] / float(occurrences)

    def add(self, key, value):
        assert len(key) == self.n - 1
        key = json.dumps(key)
        
        if key in self.grammar:
            if value in self.grammar[key]:
                self.grammar[key][value] += 1
            else:
                self.grammar[key][value] = 1
        else:
            self.grammar[key] = {}
            self.grammar[key][value] = 1

    def print_detailed_view(self):
        for key in self.grammar:
            values = ''
            
            for value in self.grammar[key]:
                values = f'{values} \n\t\t{value}: {self.grammar[key][value]}'

            print(f'{key} ->{values}')

    def sequence_probability(self, sequence):
        assert len(sequence) > self.n

        rb = RingBuffer(self.n - 1)
        probability = 1

        for word in sequence:
            if rb.full():
                grammar_input = json.dumps(rb.buffer)
                if grammar_input not in self.compiled_grammar:
                    print(f'\n{Fore.RED}{grammar_input} cannot be found in the grammar.{Style.RESET_ALL}')
                elif word not in self.compiled_grammar[grammar_input]:
                    print(f'\n{Fore.RED}{word} cannot be found in the grammar for {grammar_input}{Style.RESET_ALL}')

                probability *= self.compiled_grammar[json.dumps(rb.buffer)][word]

            rb.add(word)

        return probability

    def perplexity(self, sequence):
        denominator = self.sequence_probability(sequence) ** len(sequence)

        if denominator == 0:
            return float('inf')
        return 1 / denominator