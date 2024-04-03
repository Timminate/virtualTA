from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import JaccardSimilarity

# from chatterbot.preprocessors import StopWordsRemovalPreprocessor
from rake_nltk import Rake


# Things to do:
# - how to format textbook into json question-answer pairs (should question just be series of words related to answer?)
#    - implement custom preprocessor to remove stopwords

r = Rake()

# r.extract_keywords_from_text(<text to process>)
# To get keyword phrases ranked highest to lowest.
# r.get_ranked_phrases()
# To get keyword phrases ranked highest to lowest with scores.
# r.get_ranked_phrases_with_scores()

chatbot = ChatBot(
    "BestMatch ChatterBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.70
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    statement_comparison_function=JaccardSimilarity,
    # ^^^ https://chatterbot.readthedocs.io/en/latest/comparisons.html
    # passed to BestMatch
    
    #response_selection_method=chatterbot.response_selection.get_first_response,
    # ^^^ https://chatterbot.readthedocs.io/en/stable/logic/response_selection.html#:~:text=The%20first%20step%20involves%20searching,responses%20to%20the%20known%20match.
    
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    database_uri='mongodb+srv://dbUser:eZyCcpgzLySUVYvO@cluster0.gmqpiib.mongodb.net/sample_airbnb' # mongodb+srv://dbUser:virtualTA12345@cluster0.gqjiiep.mongodb.net/'
)


# List trainer-------------------
# Example format
# training_data = [
#     ("What is the capital of France?", "Paris"),
#     ("Who wrote 'Hamlet'?", "William Shakespeare"),
# ]

# def get_training_data(file_path):
#     training_data = []
#     with open(file_path, 'r') as file:
#         for line in file:
#             pair = line.strip().split(',')
#             training_data.append((pair[0], pair[1]))
#     return training_data

# trainer = ListTrainer(chatbot)
# training_data = get_training_data('FILE PATH HERE');
# trainer.train(training_data)

print("1")

# Corpus trainer ---------------
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
# corpus_trainer.train('chatterbot.corpus.english')
corpus_trainer.train(
    "./export.json"
    #"./data/greetings_corpus/custom.corpus.json",
    #"./data/my_corpus/"
) # TODO: add textbook json file 

# Export training data
# trainer.export_for_training('./my_export.json') # or './export.yml'

print("2")

while True:
    try:
        bot_input = chatbot.get_response(input("You: "))
        print("Bot: ", bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break