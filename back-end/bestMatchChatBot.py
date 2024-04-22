from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import Comparator # SpacySimilarity #JaccardSimilarity
import re
import os
import spacy

# Custom preprocessor for removing punctuation from user inputs
def remove_puncutation(statement):
    statement = statement.replace(',', ' ').replace('.', ' ').replace('?', ' ').replace(':', ' ').replace('!', ' ')
    statement = re.sub(' +', ' ', statement)
    return statement


class CustomSimilarity(Comparator):
    """
    Calculate the similarity of two statements using Spacy models.
    """

    def __init__(self, language):
        language = "en_core_web_lg"
        super().__init__(language)
        try:
            import spacy
        except ImportError:
            message = (
                'Unable to import "spacy".\n'
                'Please install "spacy" before using the SpacySimilarity comparator:\n'
                'pip3 install "spacy>=2.1,<2.2"'
            )
            raise ImportError(message)

        self.nlp = spacy.load(self.language)

    def compare(self, statement_a, statement_b):
        text_a = statement_a.text
        text_b = statement_b.text
        
        # Calculate SpaCy similarity
        doc_statement_a = self.nlp(text_a)
        doc_statement_b = self.nlp(text_b)
        spacy_similarity = doc_statement_a.similarity(doc_statement_b)

        # Calculate Jaccard similarity
        words1 = set(text_a.split())
        words2 = set(text_b.split())
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        jaccard_spacy_similarity = float(intersection) / union if union != 0 else 0

        return (spacy_similarity + jaccard_spacy_similarity) / 2.0

# Training & running chatbot
def main():
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
    
    chatbot = ChatBot(
        "BestMatch ChatterBot",
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.15
            }
        ],
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace',
            'chatterbot.preprocessors.unescape_html',
            'chatterbot.preprocessors.convert_to_ascii'
        ],
        statement_comparison_function=CustomSimilarity #SpacySimilarity #JaccardSimilarity,
        # ^^^ https://chatterbot.readthedocs.io/en/latest/comparisons.html
        # passed to BestMatch
        
        # response_selection_method=get_most_frequent_response
        # ^^^ https://chatterbot.readthedocs.io/en/stable/logic/response_selection.html#:~:text=The%20first%20step%20involves%20searching,responses%20to%20the%20known%20match.
        
        # storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
        # database_uri='mongodb+srv://dbUser:eZyCcpgzLySUVYvO@cluster0.gmqpiib.mongodb.net/sample_airbnb' # mongodb+srv://dbUser:virtualTA12345@cluster0.gqjiiep.mongodb.net/'
    )


    corpus_trainer = ChatterBotCorpusTrainer(chatbot)
    # corpus_trainer.train('chatterbot.corpus.english')
    corpus_trainer.train(
        # "./training-jsons/export_RAKE.json",
        # "./training-jsons/export_grammar pattern.json",
        # "./training-jsons/export_LDA.json"
        "./export.json"
    )

    while True:
        try:
            user_input = input("You: ")
            bot_response = chatbot.get_response(remove_puncutation(user_input))
            print("Bot:", bot_response)
            print()

        except(KeyboardInterrupt, EOFError, SystemExit):
            break
    
if __name__ == "__main__":
    main()