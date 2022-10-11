import pickle
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def fileUBGrams(filename):
    file = open(filename)
    rawData = file.read().lower()           # ensures consistency
    file.close()                            # newline stripping unnecessary for tokenizer

    unigrams = word_tokenize(rawData)           # unigrams of specified data file
    bigrams =  list(ngrams(unigrams, 2))        # bigrams of specified data file

    uniCounts = {}
    for tok in unigrams:                        # updates count for current unigram after each instance is found
        if tok not in uniCounts:
            uniCounts[tok] = 1                  # creates new key value pair
        else:
            uniCounts[tok] = uniCounts[tok] + 1 # updates existing pair

    biCounts = {}
    for bi in bigrams:                          # updates count for current bigram after each instance is found
        if bi not in biCounts:
            biCounts[bi] = 1                    # creates new key value pair
        else:
            biCounts[bi] = biCounts[bi] + 1     # updates existing pair

    return uniCounts, biCounts

def main():
    uCount1, bCount1 = fileUBGrams('LangId.train.English')
    uCount2, bCount2 = fileUBGrams('LangId.train.French')
    uCount3, bCount3 = fileUBGrams('LangId.train.Italian')

    pickle.dump(uCount1, open('training_unigrams_english.p', 'wb'))
    pickle.dump(uCount2, open('training_unigrams_french.p', 'wb'))
    pickle.dump(uCount3, open('training_unigrams_italian.p', 'wb'))
    print('\nUnigrams have been pickled.')

    pickle.dump(bCount1, open('training_bigrams_english.p', 'wb'))
    pickle.dump(bCount2, open('training_bigrams_french.p', 'wb'))
    pickle.dump(bCount3, open('training_bigrams_italian.p', 'wb'))
    print('\nBigrams have been pickled.')

if __name__ == "__main__":
   main()