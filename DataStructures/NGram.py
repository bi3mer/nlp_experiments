# @author: Colan Biemer

from random import random, shuffle
import json

class NGram():
    def __init__(self, n):
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
        assert len(key) == self.n
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