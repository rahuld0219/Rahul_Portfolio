# To load knowledge base
import pickle
# For chatbot ML model
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
# For NER
import spacy
nlp = spacy.load('en_core_web_sm')
# For response processing
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Holds User information
class User:
    name = ''
    likes = []
    dislikes = []

    # Saves a user model to a file
    def log(self):
        dataWrite = 'User Name:\t%s\nLikes:\t\t%s\nDislikes:\t%s' % (self.name, str(self.likes), str(self.dislikes))
        with open('user_%s.dat' % self.name, 'w', encoding='UTF-8') as file:
            file.write(dataWrite)

# Prompts the user to create their User model/profile
def createUser():
    currUser = User()

    print('CarBot:\tHello! I am CarBot. What is your name?\n')
    userName = input('user:\t')

    resp = nlp(userName)                    # NER
    for currEnt in resp.ents:
        if currEnt.label_ == "PERSON":      # Extracts Person entity from response
            currUser.name = currEnt.text
            return currUser

    toks = word_tokenize(userName)
    pos = pos_tag(toks)
    nounName = ''
    for ind in range(len(pos)):                 # If there is no Person entity found, it treats the nouns in the response and maintains any determiners
        if pos[ind][1] in ['NN', 'NNP', 'DT'] and pos[ind][0].lower() not in ['name', 'i']:
            nounName += pos[ind][0] + ' '
    if nounName:
        currUser.name = nounName.strip()
        return currUser

    if 'am' in toks:            #catches edge case if NLTK does not recognize a name as a noun
        currUser.name = userName[userName.index('am') + 2:].strip()
        return currUser

    currUser.name = userName        # If the response has no nouns or determiners just treats the entire response as the name
    return currUser

# Loads in the knowledge base dict
def extractKB():
    with open('knowledge_base.p', 'rb') as pData:
        return pickle.load(pData)

# Initializes and trains the Base chatbot model
def buildBot(name):
    kb = extractKB()

    defResp = 'I\'m sorry, I don\'t know what you\'re asking.'                                              # Response if the bot does not understand
    helpResp = 'This website might have a link that can help: https://auto.howstuffworks.com/car.htm'       # Response if the user requests help

    # Initializes bot
    Bot = ChatBot(
        name,
        logic_adapters = [
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': defResp,
                'maximum_similarity_threshold': 0.5
            },
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'help',
                'output_text': helpResp
            }
        ]
    )

    # Trains bot on knowledge base
    Trainer = ListTrainer(Bot)
    for key in kb:
        Trainer.train(kb[key])

    return Bot, Trainer

# Updates a user's likes
def addLike(currU, trainer, userIn, like):
    currU.likes.append(like)                                # Updates User
    likResp = 'That\'s great! I like ' + like + ' too!'
    trainer.train([userIn, likResp])                        # Trains bot with the new response
    return currU, trainer

# Updates a user's dislikes
def addDislike(currU, trainer, userIn, dislike):
    currU.dislikes.append(dislike)                      # Updates User
    disResp = 'I understand, duly noted.'
    trainer.train([userIn, disResp])                    # Trains bot with the new response
    return currU, trainer

# Has main chat logic
def main():
    botName = 'CarBot'

    Bot, Trainer = buildBot(botName)
    user = createUser()

    # Introduces the user to the bot's functionality
    print('\n%s:\tHello %s, I know about how cars work, so feel free to ask questions. I am here to inform you about engines, transmissions, racing, and other things to do with cars!\n' % (botName, user.name))
    print('%s:\tIf you need additional help, type \'help\'. Type \'close\' if you would like to end the conversation.\n\n%s:\tHow can I help you today?\n' % (botName, botName))

    while True:
        userIn = input('%s:\t' % user.name).lower()         # Standardizes the input to all lowercase

        # Ends the chat
        if userIn == 'close':
            print('\n%s:\tIt was great meeting you! Talk to you later!' % botName)
            user.log()
            return

        # Processses input
        toks = word_tokenize(userIn)
        pos = pos_tag(toks)
        prefPOS = ['NN', 'NNP', 'NNS', 'VB', 'VBG', 'VBP', 'TO', 'JJ', 'JJR']

        try:                                  # Skips if the word like does not exist in the tokenized input
            likeInd = toks.index('like')
            if toks[likeInd-1] == 'i':                      # if the user says they like something
                currLike = ''
                for ind in range(likeInd+1, len(toks)):     # Isolates the subject or action of the sentence
                    if pos[ind][1] in prefPOS:
                        currLike += pos[ind][0] + ' '
                currLike = currLike.strip()                 # adds just the isolated subject to the user model
                user, Trainer = addLike(user, Trainer, userIn, currLike)
            elif toks[likeInd-1] == 'n\'t':                 # If the user dislikes something
                currDislike = ''
                for ind in range(likeInd+1, len(toks)):
                    if pos[ind][1] in prefPOS:
                        currDislike += pos[ind][0] + ' '
                currDislike = currDislike.strip()           # adds just the isolated subject to the user model
                user, Trainer = addDislike(user, Trainer, userIn, currDislike)
        except ValueError:
            pass

        try:                                  # Skips if the word dislike does not exist in the tokenized input
            likeInd = toks.index('dislike')
            if toks[likeInd-1] == 'i':                      # If the user dislikes something
                currDislike = ''
                for ind in range(likeInd+1, len(toks)):     # Isolates the subject or action of the sentence
                    if pos[ind][1] in prefPOS:
                        currDislike += pos[ind][0] + ' '
                currDislike = currDislike.strip()           # adds just the isolated subject to the user model
                user, Trainer = addDislike(user, Trainer, userIn, currDislike)
        except ValueError:
            pass

        # Responds to the user
        botResp = Bot.get_response(userIn)
        print('\n%s:\t%s\n' %  (botName, botResp))

if __name__ == "__main__":
   main()