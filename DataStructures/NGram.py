# @author: Colan Biemer

class NGram():
    def __init__(self, n):
        self.n = n
        self.grammar = {}

    def compile(self, weighted=True):
        raise NotImplementedError
    
    def add(self, key, value):
        assert len(key) == self.n
        key = str(key)
        
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