import random
from collections import defaultdict
from collections import Counter
import nltk
import re


def get_text():
    user_input = input()
    if " " in user_input:
        return user_input
    with open(user_input, 'r', encoding='utf-8') as corpus:
        return corpus.read()


def get_tokens(corpus):
    wst = nltk.tokenize.WhitespaceTokenizer()
    tokens = wst.tokenize(corpus)
    trigrams = nltk.trigrams(tokens)
    return [(h1 + " " + h2, t) for h1, h2, t in trigrams]


def get_model(bigrams):
    heads_defaultdict = defaultdict(list)
    for head, tail in bigrams:
        heads_defaultdict[head].append(tail)
    return {head: Counter(tails) for head, tails in heads_defaultdict.items()}


def generate_text(model):
    generated_text = []
    first_word = ''
    while not re.match(r"^[A-Z].*[^\.\?\!]$", first_word):
        two_words = random.choice(list(model.keys()))
        first_word = two_words.split()[0]
    for _ in range(10):
        pseudo_sentence = two_words.split()
        tail = pseudo_sentence[1]
        while len(pseudo_sentence) < 5 or tail[-1] not in {'.', '!', '?'}:
            tails = list(model[two_words].keys())
            counts = list(model[two_words].values())
            tail = random.choices(tails, weights=counts)[0]
            pseudo_sentence.append(tail)
            two_words = ' '.join(pseudo_sentence[-2:])
        sentence = " ".join(pseudo_sentence)
        two_words = random.choice(list(model.keys()))
        while not re.match(r"^[A-Z].*[^\.\?\!]$", two_words.split()[0]):
            two_words = random.choice(list(model.keys()))
        generated_text.append(sentence)
    return '\n'.join(generated_text)


def main():
    text = get_text()
    tokens = get_tokens(text)
    model = get_model(tokens)
    print(generate_text(model))


if __name__ == '__main__':
    main()
