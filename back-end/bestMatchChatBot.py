from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import JaccardSimilarity

# from rake_nltk import Rake

# r = Rake()

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
            'maximum_similarity_threshold': 0.1
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
    
    # storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    # database_uri='mongodb+srv://dbUser:eZyCcpgzLySUVYvO@cluster0.gmqpiib.mongodb.net/sample_airbnb' # mongodb+srv://dbUser:virtualTA12345@cluster0.gqjiiep.mongodb.net/'
)


corpus_trainer = ChatterBotCorpusTrainer(chatbot)
# corpus_trainer.train('chatterbot.corpus.english')
corpus_trainer.train(
    "./training-jsons/export_RAKE.json",
    "./training-jsons/export_grammar pattern.json",
    "./training-jsons/export_LDA.json"
)

while True:
    try:
        bot_input = chatbot.get_response(input("You: "))
        print("Bot:", bot_input)
        print()

    except(KeyboardInterrupt, EOFError, SystemExit):
        break