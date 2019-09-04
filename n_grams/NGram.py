# @author: Colan Biemer

class NGram():
    def __init__(self, n):
        self.n = n
        self.grammar = {}

    def compile(self, weighted=True):
        raise NotImplementedError
    
    def add(self, key, value):
        assert len(key) == value
        
        if key in self.grammar:
            if value in self.grammar[key]:
                self.grammar[key][value] += 1
            else:
                self.grammar[key] = {}
                self.grammar[key][value] = 1
        else:
            self.grammar[key] = {}
            self.grammar[key][value] = 1