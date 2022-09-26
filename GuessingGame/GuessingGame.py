import sys      # For sysarg
import os       # To makefilepath valid for any os used
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from random import randint  # To choose random word
from random import seed
seed(4395)                  # Currently sets a known seed for reproducibility

# Part 1 - reads file specified in sysarg
# Taken and modified from https://github.com/kjmazidi/NLP/blob/master/Xtra_Python_Material/path%20demo/path_demo.py
def crossPlatformFP(filepath):                                  # Ensures filepath work on user's OS
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        fileData = f.read()                                     # Reads and returns data from the file
    
    return fileData

# Part 2 - Uses unique/all tokens formula
def calcLexDiv(rawToks):
    uniToks = set(rawToks)              # Sets don't allow repetition, leaving only unique tokens
    lexDiv = len(uniToks)/len(rawToks)
    
    return lexDiv

# Part 3b
def lemmatizeTokens(tokList):
    lemmatizer = WordNetLemmatizer()                            # Uses NLTK's WordNet Lemmatizer
    lemToks = [lemmatizer.lemmatize(tok) for tok in tokList]    # List comprehension applies lemmatization to all tokens
    
    return lemToks

# Part 3c
def posTagTokens(tokList):      # Returns tokenized POS tags
    posTags = pos_tag(tokList)

    # Logging
    print('\nFirst 20 tagged tokens: ', posTags[0:20])
    
    return posTags

# Part 3d
def extractNouns(posList):
    nounList = [curr[0] for curr in posList if curr[1] in ('NN', 'NNS', 'NNP', 'NNPS')]     # List comprehension selects only all kinds of nouns
    nounRet = set(nounList)                                                                 # Makes a set of unique noun tokens
    
    return nounRet                                                                          # Returns only the words

def preprocessing(raw_text):
    rawTokens = word_tokenize(raw_text)
    procTokens = [tok.lower() for tok in rawTokens if tok.isalpha() and tok.lower() not in stopwords.words('english') and len(tok) > 5]
    lemTokens = lemmatizeTokens(procTokens)
    taggedTokens  = posTagTokens(lemTokens)
    nounTokens = extractNouns(taggedTokens)

    # Part 3e-f
    print("\nNumber of tokens after preprocessing:\t", len(procTokens))
    print("Number of nouns:\t\t\t", len(nounTokens))
    
    return (procTokens, nounTokens)

# Part 4
def buildDict(listTuple):
    tokList = listTuple[0]                                              # Unpacks the list of all tokens
    nounList = listTuple[1]                                             # Unpacks the list of all nouns
    nounDict = {}

    for currNoun in nounList:
        nounDict[currNoun] = tokList.count(currNoun)                    # Dictionary of nouns with their counts
    topDict = sorted(nounDict, key = nounDict.get, reverse = True)      # Sorts the dict into a list of nouns, in descending frequency
    
    return topDict[0:50]                                                # returns top 50 nouns

def randWord(wordList):
    return wordList[randint(0,49)]  # Returns noun at a random index

# Renders the word with guesses and underscores before every round
def renderBoard(word, guesses):
    renderString = ''                                       # String to output
    
    for currChar in word:                                   # iterates through the word and checks if those guesses have been made
        if currChar not in guesses:
            renderString = renderString + '_ '              # Makes non-guessed characters underscores
        else:
            renderString = renderString + currChar + ' '    # Writes correctly guessed character
    print(renderString)

    if '_' not in renderString:     # Indicates that the whole word has been guessed
        return True
    
    return False                    # Otherwise the game continues

# Part 5
def guessingGame(wordList):
    score = 5
    currWord = randWord(wordList)
    playFlag = True                 # Determines if the current game is still active
    correctGuesses = set()          # Repeat guesses don't need to be tracked - set to store unique guesses
    allGuesses = set()              # Stores all the guesses to not penalize repeat guesses
    
    while playFlag:
        gameComplete = renderBoard(currWord, correctGuesses)                    # Tracks if all letters of the word have been found
        if gameComplete:                                                        # Victory message
            print('You solved it!\n\nFinal score: ', score, '\n')               
            break
        
        guess = input('Guess a letter:\t').lower()                              # Makes all guesses lowercase for consistency
        
        if guess == '!':                                                        # Force quit game option
            print('Quitting game.')
            break

        if len(guess) != 1 or not guess.isalpha():                              # Only allows valid letter guesses
            print('\nYour guess is invalid. Please input one character.\n')
            continue
        
        if guess in allGuesses:                                                 # Repeat guess does not affect score
            print('\nYou have already guessed this letter. Guess again.\n')
        elif guess not in currWord:                                             # Incorrect Guess - if the lowercase character is not in the word
            allGuesses.add(guess)
            score = score - 1
            if score < 0:                                                       # Game over
                print('\nSorry, you have lost all your points. You lose.\n')
                print('The word was: %s\n' % currWord)
                break
            else:                                                               # Points remaining
                print('\nSorry, guess again. Score is: ', score, '\n')
        else:                                                                   # Correct Guess - if character is in the word
            allGuesses.add(guess)
            score  = score + 1
            correctGuesses.add(guess)
            print('Right! Score is: ', score, '\n')

def main():
    # Part 1 - File path is assumed to be valid
    if len(sys.argv) > 1:
        path  = sys.argv[1]
        raw_text = crossPlatformFP(path)

        # Part 2 - Lexical diversity of the original text
        tokens = word_tokenize(raw_text)
        lexDiv = calcLexDiv(tokens)
        print('Lexical Diversity of', path, ': %.2f' % lexDiv, '\t')

        # Part 3 - Preprocessing
        proc_nouns = preprocessing(raw_text)

        # Part 4 - Dictionary of nouns and their counts
        top50Nouns = buildDict(proc_nouns)

        print('\n_______________________________________\n')

        # Part 5 - Guessing Game
        print('Let\'s play a word guessing game!\n')
        while True:
            guessingGame(top50Nouns)                                            # Uses top 50 most common nouns from text
            choice = input('\nWould you like to play again? [y/n]: ').lower()   # Makes the letter lowercase to standardize
            if choice == 'n':
                print('\nThanks for playing!')          # Ending game
                break
            elif choice == 'y':                         # Playing again
                print('\nGuess another word')
            else:
                print('\nInvalid choice')
    else:
        # part 1 - if filepath not specified
        sys.exit('No filepath specified.')

if __name__ == "__main__":
   main()