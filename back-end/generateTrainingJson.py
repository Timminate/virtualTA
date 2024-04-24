# Chatterbot source code for generating training json: https://chatterbot.readthedocs.io/en/latest/_modules/chatterbot/trainers.html
# Alternative github link: https://github.com/gunthercox/ChatterBot/blob/4ff8af28567ed446ae796d37c246bb6a14032fe7/chatterbot/trainers.py#L58

import re
import json
import numpy as np
from rake_nltk import Rake
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import string

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Tune as neeeded
paragraph_similarity_threshold = 0.4 # used in merge_similar_paragraphs()

def strip_latex_formatting(text):
    text = re.sub(r'\\label{[^}]+}\n', '', text)
    text = re.sub(r'\\index{[^}]+}\n+', '', text)
    text = re.sub(r'{\\tt ([^}]+)}', r'\1', text)
    text = re.sub(r'\\url{([^}]+)}', r'\1', text)
    text = re.sub(r'{\\bf\s+(.*?)}\n', r'\1 ', text)
    text = re.sub(r'\\java{([^}]+)}', r'"\1"', text)
    text = re.sub(r'% .*', '', text)
    
    # Remove exercises
    text = re.sub(r'\\section\{Exercise \d+\}.*?(?=\\chapter\{|\\section\{)', '', text, flags=re.DOTALL)
    
    # Remove figures
    text = re.sub(r'\\begin{figure}(.*?)\\end{figure}', '', text, flags=re.DOTALL)
    text = re.sub(r'Figure~(.*?)\.', '', text, flags=re.DOTALL)
    
    # Remove \newcommand
    text = re.sub(r'\\newcommand{(.*)}{(.*)}', '', text)
    
    # Bullet point lists
    text = re.sub(r'\\item\s*\n?\s*', '- ', text)
    
    # Remove "\["
    text = re.sub(r'\s*\n+\\\[\s*(.*?)\s\\\]\n+', r' \1\]', text)
    # Replace "\]" with '. ' or ', '
    text = re.sub(r'\\\]([A-Z])', r'. \1', text)
    text = re.sub(r'\\\]([a-z])', r', \1', text)
    
    # remove $____$
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    
    # Properly replace ∈
    text = re.sub(r' \\in ', ' ∈ ', text)
    
    # Properly replace ≈
    text = re.sub(r' \\approx ', ' ≈ ', text)
    
    # Fix double quote chars
    text = re.sub(r'``([^`\']+)\'\'', r'"\1"', text)
    
    # Get rid of \\emph{} formatting
    text = re.sub(r'\\emph{(.*?)}', r'\1', text)
    
    # Reformat bold
    text = re.sub(r'{\\bf (.*?)}', r'**\1**', text)
    text = re.sub(r'\\textbf{(.*?)}', r'**\1**', text)
    
    # Remove table (for now)
    text = re.sub(r'\\begin{tabular}(.*?)\\end{tabular}', '', text, flags=re.DOTALL)
    
    # Replace ...
    text = re.sub(r'\\ldots', '...', text)
    
    # Get rid of \\ for log and runtime
    text = re.sub(r'\\log', 'log', text)
    text = re.sub(r'\\runtime', 'runtime', text)
    
    # Replace quotes
    text = re.sub(r'\\begin{quote}\n', '"', text)
    text = re.sub(r'\n\\end{quote}', '"', text)
    
    # Combine split-up paragraphs
    text = re.sub(r'([\w",.()*?-]+)[ ]*\n[ ]*([\w",.()*-]+)', r'\1 \2', text)
    
    return text

def organize_paragraphs(content):
    # Split into paragraphs by newline
    paragraphs = content.split('\n')
        
    grouped_paragraphs = []
    current_paragraph = []

    merge_mode = False
    
    unfinished_paragraph = False
    partial_paragraph = ""
    
    for p in paragraphs:
        if p.strip():
            # Merge paragraphs starting at \begin{itemize/enumerate/verbatim}
            if merge_mode:
                if p.strip().startswith(('\\end{itemize}', '\\end{enumerate}', '\\end{verbatim}')):
                    merge_mode = False  # Reached \end{itemize/enumerate/verbatim}
                else:
                    current_paragraph.append(p.rstrip()) 
            else:
                if p.strip().startswith(('\\begin{itemize}', '\\begin{enumerate}', '\\begin{verbatim}')):
                    merge_mode = True  # Reached \begin{itemize/enumerate/verbatim}
                else:
                    # check if is unfinished paragraph (ending with ;)
                    if p[-1] == ';':
                        unfinished_paragraph = True
                    
                    if unfinished_paragraph:
                        partial_paragraph += p.strip()
                        if p[-1] != ';':
                            unfinished_paragraph = False
                    else:
                        current_paragraph.append(p.rstrip())
                    
                    # Append current paragraph
                    if current_paragraph and not unfinished_paragraph:
                        grouped_paragraphs.append('\n'.join(current_paragraph))
                        current_paragraph = []


    # Append the last leftover paragraph, if exists
    if current_paragraph:
        grouped_paragraphs.append('\n'.join(current_paragraph))

    return grouped_paragraphs

def merge_similar_paragraphs(paragraphs):
    if len(paragraphs) == 1:
        return paragraphs
    
    # Initialize Sentence Transformer model
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Compute pairwise cosine similarity between sentence embeddings
    embeddings = model.encode(paragraphs)
    similarity_matrix = cosine_similarity(embeddings)
    
    # merged pagraphs
    merged_paragraphs = []

    i = 0
    while i < len(paragraphs):
        # Find all mergable paragraphs
        end_index = i
        for j in range(i + 1, len(paragraphs)):
            if similarity_matrix[i][j] > paragraph_similarity_threshold:
                end_index = j
            
        # Merge paragraphs
        merged_paragraphs.append('\n'.join(paragraphs[i:end_index+1]))
        i = end_index+1

    return merged_paragraphs

# Used for RAKE: this extracts top phrases from each chunk of text
def extract_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    ranked_keywords = rake.get_ranked_phrases()

    keyword_string = ', '.join(ranked_keywords[:3]) # get top 3 phrases
    return keyword_string

# Function to extract noun phrases from a sentence
def extract_noun_phrases(text):
    # Tokenize the text & remove stopwords
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in stopwords.words('english') and word.isalnum()]
    
    # Tag parts of speech & extract noun phrases
    tagged_words = pos_tag(words)
    grammar = r"""
        NP: {<DT|JJ|NN.*>+<NN.*>}
    """  
    
    # Define grammar pattern for noun phrases
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(tagged_words)
    noun_phrases = []
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        noun_phrases.append(' '.join(word for word, pos in subtree.leaves()))
    return noun_phrases

# Remove punctuation from keywords
def remove_punctuation(keywords):
    keywords = keywords.replace(';', '').replace('** ', '').replace(' **', '').replace('"', '').replace('!', '').replace('http :// thinkdast', ' ').replace('.', ' ').replace('):', ' ').replace('*/', ' ')
    keywords = re.sub(' +', ' ', keywords)
    return keywords

def extract_content(tex_file):
    with open(tex_file, 'r') as file:
        content = file.read()
    
    # Convert LaTeX formatting to text
    content = strip_latex_formatting(content)
        
    # Find sections using regex
    section_regex = r'\\section{([^}]+)}\n(.*?)(?=\\chapter|\\section|\Z)'
    sections = re.findall(section_regex, content, re.DOTALL)

    # txtfile1 = open("./after1.txt", 'w+', encoding='utf8')
    # txtfile2 = open("./after2.txt", 'w+', encoding='utf8')
    extracted_content = []
    for section_title, section_content in sections:
        paragraphs = organize_paragraphs(section_content)

        # Merge broken up paragraphs
        i = len(paragraphs)-2
        while i >= 0:
            if paragraphs[i][-1] is ":" or not (paragraphs[i][-1] is "." or paragraphs[i][-1] is "?" or paragraphs[i][-1] is "!"):
                paragraphs[i:i+2] = ['\n'.join(paragraphs[i:i+2])]
            i -= 1
    
        # print("Num paragraphs:", len(paragraphs))
        # print()
        
        # txtfile1.write('\n-------------------\n'.join(paragraphs))
          
        merged_paragraphs = merge_similar_paragraphs(paragraphs)
        # print("Num merged paragraphs:", len(merged_paragraphs))
        # print("------------------------------------") 
        
        # txtfile2.write('\n-------------------\n'.join(merged_paragraphs))
        
        from gensim import corpora, models

        # Tokenize each paragraph into a list of words & create dictionary and corpus
        tokenized_paragraphs = [[phrase.lower() for phrase in extract_noun_phrases(paragraph)] for paragraph in merged_paragraphs]
        dictionary = corpora.Dictionary(tokenized_paragraphs)
        corpus = [dictionary.doc2bow(paragraph) for paragraph in tokenized_paragraphs]

        # Train LDA model
        lda_model = models.LdaModel(corpus, num_topics=7, id2word=dictionary)

        for p, tokenized_paragraph in zip(merged_paragraphs, tokenized_paragraphs):
            combined_keywords = []
            
            # =============== Method 1: RAKE ==============================
            combined_keywords.append(remove_punctuation(extract_keywords(p)))
            
            # =============== Method 2: Grammar pattern ==================
            # Extract noun phrases from the paragraph
            noun_phrases = extract_noun_phrases(p)
            # Get top 5 frequent noun phrases as keywords
            keywords = ", ".join(noun_phrases[:5])  # Adjust as needed
            
            if keywords is not "":
                combined_keywords.append(remove_punctuation(keywords))
                
            # =============== Method 3: LDA ==============================
            # Get bag-of-words representation
            bow = dictionary.doc2bow(tokenized_paragraph)
            # Get topic distribution of paragraph
            topic_distribution = lda_model[bow]
            
            # Extract top 3 topics (if available)
            sorted_topics = sorted(topic_distribution, key=lambda x: x[1], reverse=True)
            top_topics = sorted_topics[:3]
            
            topic_keywords = []
            for topic in top_topics:
                topic_words = lda_model.show_topic(topic[0])
                # Extract top 5 words from each topic
                words = [word for word, _ in topic_words[:5]]  # Adjust the number of words as needed
                topic_keywords.extend(words)
            
            topic_keywords = list(set(topic_keywords)) # Remove duplicates
            keywords = ", ".join(topic_keywords)
            combined_keywords.append(remove_punctuation(keywords))
            
            # =============== Creating keyword-corpus pairs ===============
            extracted_content.append([', '.join(combined_keywords), p])
 
    return extracted_content

# Based off of ChatterBot trainers.py: export_for_training()
def export_for_training(extracted_content, file_path='./export.json'):
    #Create a file from the extracted content that can be used to train other chat bots.
    export = {'conversations': extracted_content}
    with open(file_path, 'w+', encoding='utf8') as jsonfile:
        json.dump(export, jsonfile, ensure_ascii=False)

def main():
    tex_file = 'book.tex' # Full textbook: 'book.tex'
    export_file = './export.json'
    
    extracted_content = extract_content(tex_file)
    export_for_training(extracted_content, export_file)
    
    print(tex_file, 'converted into training json:', export_file)

if __name__ == "__main__":
    main()
