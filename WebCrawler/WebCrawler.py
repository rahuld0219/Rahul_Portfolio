import pickle                                               # Pickling Final Knowledge Base dict
from bs4 import BeautifulSoup                               # processing page data
import requests                                             # to crawl
import urllib                                               # to request page data
from random import shuffle                                  # For making the link selection more diverse
import re                                                   # For filtering page text
from nltk.tokenize import sent_tokenize, word_tokenize      # For building knowledge base
from nltk.corpus import stopwords                           # For preprocessing texts for knowledge base

# Crawls for similar, relevant links from a specified domain
def crawlUrls(initDom):
    req =  requests.get(initDom)
    content = req.text
    soup = BeautifulSoup(content)       # Reads page data to parse for links
    linkList = [initDom]                # initial domain is included in list of links
    linkCount = 0

    for links in soup.find_all('a'):
        link = str(links.get('href'))               # Isolates HTML hyperlink tags
        if 'Frog' in link or 'frog' in link:        # Ensures relevancy
            if link.startswith('/url?q='):          # removes query characters
                link = link[7:]
                print('modified:',link)

            if '&' in link:
                link = link[link.find('&'):]

            if link.startswith('http') and 'google' not in link and 'archive.org' not in link:          # Prevents tricky links like Google and Wayback Machine
                if 'wikipedia' not in link:                                                             # Makes sure other Wikipedia articles are not used
                    linkCount = linkCount + 1
                    linkList.append(link)

    shuffle(linkList)           # Helps make the selection of links more diverse

    return linkList

# Filters a page's content to extract just the visible text components
def filterText(curr):
    if curr.parent.name in ['style', 'script', '[document]', 'head', 'title', '[endif]']:       # filters out non-text HTML tags
        return False
    elif re.match('<!.*>', str(curr.encode('UTF-8'))):                                          # filters out HTML comments
        return False
    return True

# Scrapes the text data from the links found
def scrapeLinks(linkList, numLinks):
    fileNum = 0
    for link in linkList:                                       # Tries every link until the specified number of links is reached
        if fileNum == numLinks:
            break
        try:
            linkData = urllib.request.urlopen(link)
            soup = BeautifulSoup(linkData)
            pageData = soup.find_all(text = True)               # Extracts page data (including unwanted tag data)

            #Logging
            print(link)

            pageText = list(filter(filterText, pageData))       # Applies filter function to current page data
            dataWrite = ' '.join(pageText)
            fileNum = fileNum + 1
        except Exception as e:                  # If the HTTP request fails for any reason, it logs and skips the link
            print(e)
            continue
        with open('file%d.txt' % fileNum, 'w', encoding='UTF-8') as file:       # Standardized file name ('file#.txt')
            file.write(dataWrite)

# Cleans up scraped text
def procText(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]        # Removes any newlines or tabs
    
    with open('%s_sents.txt' % filename.split('.')[0], 'w', encoding='UTF-8') as file:  # Standardized file name ('file#_sents.txt')
        for line in lines:
            currSents = sent_tokenize(line)
            for sent in currSents:
                file.write('%s\n' % sent)

# Returns the top 40 important terms (by term frequency) from the processed data 
def impTerms(numLinks):
    uniCounts = {}

    # determines the frequency of the unique (non stopword) terms in the data
    for i in range(numLinks):
        with open('file%d_sents.txt' % (i + 1), 'r', encoding='UTF-8') as file:
            data = file.read()

        rawToks = word_tokenize(data)
        unigrams = [tok.lower() for tok in rawToks if tok.isalpha() and tok.lower() not in stopwords.words('english')]
        
        for tok in unigrams:
            if tok not in uniCounts:
                uniCounts[tok] = 1
            else:
                uniCounts[tok] = uniCounts[tok] + 1

    impTerms = sorted(uniCounts, key = uniCounts.get, reverse=True)         # List of keys, sorted by highest value first
    print(impTerms[:40])                                                    # Displays top 40 words to be chosen from

# Builds and pickles the knowledge base (dict: {term: [sentences that include the term]})
def buildKB(termList, numLinks):
    sentList = []
    kBase = {k: [] for k in termList}

    for i in range(numLinks):
        with open('file%d_sents.txt' % (i + 1), 'r', encoding='UTF-8') as file:
            sentList.extend(file.readlines())                                       # Puts all sentences into one list

    for word in termList:
        for sent in sentList:
            if word in sent.lower().split():             # split() ensures that every word match is an exclusive word match
                kBase[word].append(sent.rstrip())        # For example: prevents a sentence with 'asking' to match the term 'skin'

    pickle.dump(kBase, open('frog_knowledge_base.p', 'wb'))

    return kBase

# Parts 1-4: separated from parts 5-6 since the 10 terms need to be chosen manually after the important terms are found
def scrape(url, numLinks):
    links = crawlUrls(url)

    scrapeLinks(links, numLinks)                # Creates Files

    for i in range(numLinks):
        procText('file%d.txt' % (i + 1))        # Creates Files

    impTerms(numLinks)                          # Displays choices of terms

###########################################################################################################################
# No main since parts 1-4 and 5-6 need to be done and toggled manually
url = 'https://en.wikipedia.org/wiki/Frog'
numLinks = 20
# scrape(url, numLinks)             # Commented to prevent any changes to the scraped data corpus

tenTerms = ['frog', 'species', 'tree', 'water', 'eggs', 'amphibians', 'tadpoles', 'toad', 'anura', 'skin']      # Manually chosen
kbDict = buildKB(tenTerms, numLinks)
print(kbDict['skin'])                       # displays one of the elements of the dict for logging