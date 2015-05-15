#!/usr/bin/env python
import sys
import re
import argparse
import gzip
import math
from copy import deepcopy

import numpy

ISNUMBER = re.compile(r'\d+.*')

def norm_word(word):
    """
    :param word:
    :returns ---num---/---punc---/word.lower():
    Check if a word is number/punctuation. It it is a word
    convert to lowercase
    """
    if ISNUMBER.search(word.lower()):
        return '---num---'
    elif re.sub(r'\W+', '', word) == '':
        return '---punc---'
    else:
        return word.lower()

def read_word_vecs(filename):
    """
    :param filename: file name containing vector file
    :returns wordvector: Normalised word vector file
    Read all the word vectors and normalize them
    """
    word_vectors = {}
    if filename.endswith('.gz'):
        file_object = gzip.open(filename, 'r')
    else:
        file_object = open(filename, 'r')
    
    for line in file_object:
        line = line.strip().lower()
        word = line.split()[0]
        word_vectors[word] = numpy.zeros(len(line.split())-1, dtype=float)
    for index, vecVal in enumerate(line.split()[1:]):
      word_vectors[word][index] = float(vecVal)
    #normalize weight vector
    word_vectors[word] /= math.sqrt((word_vectors[word]**2).sum() + 1e-6)
    
    sys.stderr.write("Vectors read from: "+filename+" \n")
    return word_vectors

def save_retrofit( word_vectors, out_file_name):
    """
    :param word_vectors: wordvector dict
    :param out_file_name: file name to write the retrofit data
    Save retrofit to file
    """
    sys.stderr.write('\nWriting down the vectors in '+out_file_name+'\n')
    out_file = open(out_file_name, 'w')  
    for word, values in word_vectors.iteritems():
        out_file.write(word + ' ')
        for val in word_vectors[word]:
            out_file.write('%.4f' %(val) + ' ')
        out_file.write('\n')      
    out_file.close()
  
def read_lexicon(filename):
    """
    :param filename: lexicon file name
    :returns lexicon: lexicon in dict format
    Read the PPDB word relations as a dictionary
    """
    lexicon = {}
    for line in open(filename, 'r'):
        words = line.lower().strip().split()
        lexicon[norm_word(words[0])] = [norm_word(word) for word in words[1:]]
    return lexicon

def retrofit(word_vecs, lexicon, num_iters):
    """
    :param word_vecs: Word vectors as dict
    :param lexicon: lexicon as dict
    Retrofit word vectors to a lexicon
    """
    new_word_vecs = deepcopy(word_vecs)
    wv_vocab = set(new_word_vecs.keys())
    loop_vocab = wv_vocab.intersection(set(lexicon.keys()))
    for it in range(num_iters):
        # loop through every node also in ontology (else just use data estimate)
        for word in loop_vocab:
            word_neighbours = set(lexicon[word]).intersection(wv_vocab)
            num_neighbours = len(word_neighbours)
            #no neighbours, pass - use data estimate
            if num_neighbours == 0:
                continue
            # the weight of the data estimate if the number of neighbours
            new_vec = num_neighbours * word_vecs[word]
            # loop over neighbours and add to new vector (currently with weight 1)
            for pp_word in word_neighbours:
                new_vec += new_word_vecs[pp_word]
            new_word_vecs[word] = new_vec/(2 * num_neighbours)

    return new_word_vecs

def main(args):
    """
    Main function
    """
    wordVecs = read_word_vecs(args.input)
    lexicon = read_lexicon(args.lexicon)
    #lexicon = read_lexicon(args.lexicon, wordVecs)
    numIter = int(args.numiter)
    outFileName = args.output
    ''' Enrich the word vectors using ppdb and print the enriched vectors '''
    save_retrofit(retrofit(wordVecs, lexicon, numIter), outFileName) 
 
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=None, help="Input word vecs")
    parser.add_argument("-l", "--lexicon", type=str, default=None, help="Lexicon file name")
    parser.add_argument("-o", "--output", type=str, help="Output word vecs")
    parser.add_argument("-n", "--numiter", type=int, default=10, help="Num iterations")
    args = parser.parse_args()
    main(args)
