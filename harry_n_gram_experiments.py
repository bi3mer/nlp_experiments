# @author: Colan Biemer

from tqdm import tqdm
import json
import os

from DataStructures import NGram, RingBuffer

files = ['harry_01.txt', 'harry_02.txt']
min_grammar_size = 2
max_grammar_size = 10

grammars = [NGram(i) for i in range(min_grammar_size, max_grammar_size)]
buffers = [RingBuffer(i - 1) for i in range(min_grammar_size, max_grammar_size)]

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

if not os.path.exists('dist'):
    os.makedirs('dist')

file_path = os.path.join('dist', 'harry_potter_naive_n_grams.html')

print('Finding the most common occurring key to start a sentence')
best_key = ''
most_occurrences = -1

for key in grammars[-1].grammar:
    key_occurrences = 0
    for value in grammars[-1].grammar[key]:
        key_occurrences += grammars[-1].grammar[key][value]

    if key_occurrences > most_occurrences:
        most_occurrences = key_occurrences
        best_key = key

best_key = json.loads(best_key)

print(f'Generating HTML at {file_path}')
f = open(file_path, 'w')
f.write('<h1>Naive N-Grams with Harry Potter</h1>')

def write_to_html(f, starting_input, compiled_grammar, grammar_size):
    buffer = RingBuffer(grammar_size)
    paragraph = []

    f.write('<p>')
    for key in starting_input:
        f.write(f'{key} ')
        buffer.add(key)
        paragraph.append(key)

    for _ in range(100):
        next_word = compiled_grammar.get(buffer.buffer)
        buffer.add(next_word)
        paragraph.append(next_word)
        f.write(f'{next_word} ')

    f.write('\n<br/>\n<br/>\n')
    f.write(f'<b>Percent Likelihood:</b> {compiled_grammar.compute_sequence_probability(paragraph) * 100}%')

    f.write('\n<br/>\n')
    f.write('</p>\n')

for i in range(len(grammars)):
    grammar_size = i + min_grammar_size - 1
    grammar = grammars[i]

    f.write(f'<h2>N={grammar_size}</h2>')

    f.write(f'<h3>Unweighted Output</h3>')
    grammar.compile(weighted=False)
    write_to_html(f, best_key, grammar, grammar_size)

    f.write(f'<h3>Weighted Output</h3>')
    grammar.compile(weighted=True)
    write_to_html(f, best_key, grammar, grammar_size)

f.write('<br/><br/><br/><br/><br/><br/><br/><br/><br/>')
    

f.close()
os.popen(f'open {file_path}')