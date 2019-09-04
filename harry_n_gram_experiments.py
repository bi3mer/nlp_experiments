# @author: Colan Biemer

from tqdm import tqdm
import os

from DataStructures import NGram, RingBuffer

files = ['harry_01.txt', 'harry_02.txt']
# files = ['dummy.txt']
min_grammar_size = 1
max_grammar_size = 6

grammars = [NGram(i) for i in range(min_grammar_size, max_grammar_size)]
buffers = [RingBuffer(i) for i in range(min_grammar_size, max_grammar_size)]

for file_name in tqdm(files):
    file_name = os.path.join('data', file_name)
    f = open(file_name, 'r')
    content = f.read()
    f.close()

    content = content.split(' ')
    for word in tqdm(content):
        for index in range(max_grammar_size - min_grammar_size):
            if buffers[index].full():
                grammars[index].add(buffers[index].buffer, word)

            buffers[index].add(word)

print('')
print('Grammar Generated')

grammars[0].print_detailed_view()
