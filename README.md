# Rahul_Portfolio
This is Rahul Das' Portfolio. Rahul is a senior at UT Dallas studying computer science.

#### Running My Programs Locally
Clone this repo locally in a directory of your choice using:

`git clone https://github.com/rahuld0219/Rahul_Portfolio.git`

---

## Overview of NLP
You can see the [document here](Overview_of_NLP.pdf)
### Description
This pdf document gives a general overview of Natural Language Processing.

---

## Text Processing With Python
You can see the [code here](TextProcessing/TextProcessing.py)

### Description
This program parses a CSV file containing employee data to ensure that the data is both standardized and correct. It then pickles the corrected data. Finally, it unpickles the data to print it out properly formatted.

CSV data format: `Last Name,First Name,Middle Initial,ID,Office Phone`

#### Instructions to Run
After cloning this repo locally, open a terminal in the TextProcessing folder. From this terminal, run the following command with the relative filepath of the CSV file as an argument variable:

`python3 TextProcessing.py data/data.csv`

#### Strengths/Weaknesses of Python for Text Processing
Python is a very powerful language and I think it is a great tool to use for text processing. It has vast librarysupport for all kinds of data processing. While I chose not to use it, Python supports a library for processing CSV files. This and many more such libraries make python a versatile took for almost any situation. It also is dynamically typed which makes using the language significantly easier. This, in combination with the versatility and modularity of python's libraries makes it a personal favorite when it comes to languages to use for text processing. There are of course the tradeoffs of python being  slower with more overhead, due to the emphasis on its dynamic and interpreted nature. At the scale that I am working, however, I think these downsides are very reasonable to manage.

#### Skills Exercised
My main experience with this assignment was to refresh my python skills. Working with the python syntax, data structures, and file I/O were all reviews of my past experience with the language. One new skill I picked up was using python's regex capabilities. I had never  worked with regexes in python but I found the `re` module very intuitive.

---

## Exploring NLTK
You can see the [code here](ExploringNLTK/PortfolioAssignment2.ipynb)

### Description
This Jupyter notebook contains explanations and demonstrations of some important functionalities of the NLTK library. Detailed explanations are available in the notebook.

---

## Word Guess Game
You can see the [code here](GuessingGame/GuessingGame.py)

### Description
This project utilized NLTK's parts of speech tagging and stop words to make a Hangman style guessing game with the nouns from a text file. The player starts the game with 5 points. They are given a series of blanks and are tasked with guessing the words a letter at a time. Every correct guess is +1 point and every incorrect guess is -1 point. If the player's score drops below 0, the player loses. Players can quit the game at any time by typing **'!'**. Repeat guesses are ignored.

#### Instructions to Run
After cloning this repo locally, open a terminal in the GuessingGame folder. From this terminal, run the following command with the relative filepath of the TXT file as an argument variable:

`python3 GuessingGame.py anat19.txt`

#### Skills Exercised
This project gave me experience with some of the NLTK tools that we had only learned about earlier. I got hands on experience with filtering stop words, lemmatizing in an actual processing context, and NLTK's parts of speech tagger. It was very helpful for me to actually apply the concepts we only briefly covered or demonstrated earlier.

---

## WordNet
You can see the [code here](WordNet/WordNet.ipynb)

### Description
This project explores NLTK's implementations of WordNet, SentiWordNet, and the Lesk Algorithm to process language. WordNet is a lexical database of English words that are organized into various relational groupings. The words themselves aren't being related to one another. Instead, specific meanings and uses of the words are linked to one another. SentiWordNet is a tool designed to perform sentiment analysis by determining opinion polarity scores for words.

#### Skills Exercised
With this project I was able to actually begin exploring how natural language processing works. I was always curious how language processing can be performed accurately without attempting to understand the intent and sentiment behind the words. I also was curious about how computers account for the nuanced context that comes with structured sentences. Getting to use sentiment analysis, similarity metrics, context analysis, and statistical analysis of texts was very helpful for me to start understanding more about NLP

---

## N-Grams
You can see the [code here](Ngram)

### Description
This project explores N-grams, a useful form of sequence that aids in processing the patterns of language. N-grams can be used to determine probabilistic models for a language based on a training corpus. These models can be used to more accurately generate or interpret natural language since they can account for the natural contexts that words show up in most often.

#### N-grams
N-grams are groupings with a length of n of consecutive words from a text. The value of n can be any integer, such as n =1 (unigrams), n = 2 (bigrams), n = 3 (trigrams), etc. For example, the bigrams of the sentence “Hello my name is Rahul” would be [“Hello my”, “my name”, “name is”, “is Rahul”]. N-grams can be useful because they can provide the context around a word’s usage. By observing the probabilities of a word appearing around other words, we can begin to determine a probabilistic language model of the relationships between the usages of words in a body of text. N-grams can be used in models to interpret natural language, since by knowing the statistical chances of various words, errors and contextual meanings can be better understood. Additionally, by using this model, more natural sounding language can be produced since the model has a better “understanding” of the natural contexts in which words regularly show up. There can be issues with this, however since a probabilistic model will inherently be biased towards its source context text. This can hinder quality based on the quality of the text. 

#### Skills Exercised
Through this project I was able to learn about how probabilistic models can be used for NLP. I have some experience with probabilistic models but I was always curious about how context plays a role in NLP. This project gave me a good introduction to that.

---

## Web Crawler
You can see the [code here](WebCrawler/WebCrawler.py)

### Description
This project explores Web Crawling and Scraping. Web Crawling is the process of finding links of sites that are related to a certain topic or goal. Web Scraping is the process of extracting data from websites that are crawled. Here, we used web crawling and scraping techniques to gather data about a certain topic (in my case, frogs). We then used the gathered data to create a corpus and knowledge base that can be used for other applications, such as a simple chatbot.

#### Skills Exercised
This project introduced a lot of new concepts to me as I have never done any sort of web scraping before. I learned to use python for web scraping and data processing. 

---

## Sentence Parsing
You can see the [document here] (SentenceParsing/SentenceParsing.pdf)

### Description
This project explores the relationships between three forms of sentence parsing commonly used in NLP: PSG Parsing, Dependency Parsing, and SRL Parsing. To demonstrate the similarities and differences between them, the three parses were applied on a moderately complex sentence.

---

## Author Attribution
You can see the [code here](AuthorAttribution/AuthorAttribution.ipynb)

### Description
This project explores the performance of different ML methods for a classification task on bodies of text. The data for testing and training the models comes from `federalist.csv`. The program classifies the ownership of a body of text based on training data. By comparing  the accuracies of various ML models, we can see the benefits and issues of the different models in a practical usage example.