import nltk
from nltk.corpus import *


scrabble_dictionary = []

with open("scrabble_dict.txt") as f:
    for line in f:
        val = line.rstrip().lower()
        scrabble_dictionary.append(val)


def corpus_to_dict(corpus):
    parsed_corpus = []
    for word in corpus:
        current_word = word[0]
        if current_word.lower() in scrabble_dictionary:
            parsed_corpus.append(word[0])
    return set(parsed_corpus)

def corpus_list_to_dict(corpus):
    parsed_corpus = []
    for word in corpus:
        word = word.rstrip()
        current_word = word
        if current_word.lower() in scrabble_dictionary:
            parsed_corpus.append(word)
    return set(parsed_corpus)


h=open('internet.txt','rU')
raw3=h.read()
tokens3 = nltk.word_tokenize(raw3)
internet_text = nltk.Text(tokens3)

#example for email domain
distribution = nltk.FreqDist(internet_text)

most_common_set = distribution.most_common(50000)

internet_words = corpus_to_dict(most_common_set)

with open('sciencewords.txt', errors='ignore') as scicorpus:
    parsed_sci_corpus = corpus_list_to_dict(scicorpus)


with open("government.txt", 'a') as gov:
    for word in gov_words:
        gov.write(word.lower() + '\n')

with open("classics.txt", 'a') as classics:
    for word in classic_words :
        classics.write(word.lower() + '\n')
        
with open("science.txt", 'a') as science:
    for word in parsed_sci_corpus :
        science.write(word.lower() + '\n')

with open("emails.txt", 'a') as emails:
    for word in internet_words :
        emails.write(word.lower() + '\n')


