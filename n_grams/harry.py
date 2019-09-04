# @author: Colan Biemer

from tqdm import tqdm
import os

from NGram import NGram

files = ['harry_01.txt', 'harry_02.txt']
min_grammar_size = 1
max_grammar_size = 6


grammars = [NGram(i) for i in range(min_grammar_size, max_grammar_size)]

for file_name in tqdm(files):
    file_name = os.path.join('..', 'data', file_name)
    f = open(file_name, 'r')
    content = f.read()
    f.close()

    content = content.split(' ')
    for word in tqdm(content):
        continue
    
    break

print()