import pickle
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

# Preprocesses the data from a file and returns it as a list of lines
def dataProc(filepath):
    file = open(filepath, encoding='UTF-8')
    text = file.read().lower()                          # enforces consistency
    file.close()

    dataLines = text.split('\n')
    dataLines = [line for line in dataLines if line]    # strips empty elements
    return dataLines

# calculates the probability of a line of text
def calcProb(line, uniDict, biDict, v):
    uniLine = word_tokenize(line)           # unigrams of current line
    biLine = list(ngrams(uniLine, 2))       # bigrams of current line
    prob = 1                                # Laplace Formula = (b+1)/(u+v)

    for bi in biLine:
        b = biDict[bi] if bi in biDict else 0               # count of current bigram
        u = uniDict[bi[0]] if bi[0] in uniDict else 0       # count of  first unigram in the bigram
        prob  = prob * ((b + 1) / (u + v))                  # updates sentence probability for each bigram
    
    return prob

# calculates accuracy of the probabilistic model
def calcAcc(probFile, compFile):
    file = open(probFile, encoding='UTF-8')

    #creates a list of lists of the line number and classification pairs
    prob = [[data for data in line.split(' ')] for line in file.read().split('\n') if line]

    #creates a list of lists for the result validation data
    file = open(compFile, encoding='UTF-8')
    comp = [[data for data in line.split(' ')] for line in file.read().split('\n') if line]

    file.close()

    incorrClasses = []                          # tracks misclassification line numbers
    corrClass = 0                               # tracks num of correct classifications
    for ind in range(len(comp)):
        if prob[ind][1] == comp[ind][1]:        # compares classification to validation
            corrClass = corrClass + 1
        else:
            incorrClasses.append(prob[ind][0])  # tracks misclassifications

    return corrClass / len(comp) * 100, incorrClasses

def main():
    # Test data file
    test = dataProc('LangId.test')

    # English ngram dicts
    engUni = pickle.load(open('training_unigrams_english.p', 'rb'))
    engBi = pickle.load(open('training_bigrams_english.p', 'rb'))

    # French ngram dicts
    freUni = pickle.load(open('training_unigrams_french.p', 'rb'))
    freBi = pickle.load(open('training_bigrams_french.p', 'rb'))

    # Italian ngram dicts
    itaUni = pickle.load(open('training_unigrams_italian.p', 'rb'))
    itaBi = pickle.load(open('training_bigrams_italian.p', 'rb'))

    vocabSize = len(engUni) + len(freUni) + len(itaUni)     # v for probability calculation

    file = open('highProbs.data', mode='w')                     # creates file to store classifications
    probDict = {'English': 0, 'French': 0, 'Italian': 0}        # tracks current probabilities of each class
    for line in range(len(test)):
        probDict['English'] = calcProb(test[line], engUni, engBi, vocabSize)
        probDict['French'] = calcProb(test[line], freUni, freBi, vocabSize)
        probDict['Italian'] = calcProb(test[line], itaUni, itaBi, vocabSize)

        maxLang = max(probDict, key=probDict.get)       # finds key of key-value pair with maximum value

        currStr = '%d %s\n' % (line+1, maxLang)         # puts in classification in format "line_number class"
        file.write(currStr)
    file.close()

    # Output
    # Accuracy: 98.0%
    # Misclassified line numbers: ['24', '187', '191', '247', '277', '279']
    acc, misclass = calcAcc('highProbs.data', 'LangId.sol')
    print('Accuracy:', acc, '%\nMisclassified line numbers:', misclass)

if __name__ == "__main__":
   main()