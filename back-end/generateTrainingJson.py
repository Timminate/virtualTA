# Chatterbot source code for generating training json: https://chatterbot.readthedocs.io/en/latest/_modules/chatterbot/trainers.html
# Alternative github link: https://github.com/gunthercox/ChatterBot/blob/4ff8af28567ed446ae796d37c246bb6a14032fe7/chatterbot/trainers.py#L58

import re
import json
import numpy as np
from rake_nltk import Rake
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def extract_keywords(text):
    rake = Rake()
    rake.extract_keywords_from_text(text)
    ranked_keywords = rake.get_ranked_phrases()

    keyword_string = ', '.join(ranked_keywords[:3]) # get top 3 phrases
    return keyword_string

def remove_latex_formatting(text):
    text = re.sub(r'\\label{[^}]+}\n', '', text)
    text = re.sub(r'\\index{[^}]+}\n+', '', text)
    text = re.sub(r'\\url{([^}]+)}', r'\1', text)
    text = re.sub(r'{\\bf\s+(.*?)}\n', r'\1 ', text)
    text = re.sub(r'\\java{([^}]+)}', r'"\1"', text)
    
    # Code blocks
    text = re.sub(r'\\begin{verbatim}(.*?)\\end{verbatim}\n\n', '', text, flags=re.DOTALL)

    # Bullet point lists
    text = re.sub(r'\\item\s*', '- ', text)

    # remove leading spaces
    text = re.sub(r'^\s*', '', text, flags=re.MULTILINE)
    
    # Remove "\["
    text = re.sub(r'\s*\n+\\\[\s*(.*?)\s\\\]\n+', r' \1\]', text)
    # Replace "\]" with '. ' or ', '
    text = re.sub(r'\\\]([A-Z])', r'. \1', text)
    text = re.sub(r'\\\]([a-z])', r', \1', text)
    
    # Combines broken-up text into one paragraph
    text = re.sub(r'(?<=[^\.\?!}])\s?\n(?=[^\s\.\?!\\])', ' ', text)
    
    # remove $____$
    text = re.sub(r'\$([^$]+)\$', r'\1', text)
    
    # Properly replace ∈
    text = re.sub(r' \\in ', ' ∈ ', text)
    
    # Fix double quote chars
    text = re.sub(r'``([^`\']+)\'\'', r'"\1"', text)
    
    return text

def organize_paragraphs(content):
    # Split into paragraphs by newline
    paragraphs = content.split('\n')

    grouped_paragraphs = []
    current_paragraph = []

    merge_mode = False

    for p in paragraphs:
        if p.strip():
            # Merge paragraphs starting at \begin{enumerate}
            if merge_mode:
                if p.strip().startswith('\\end{enumerate}'):
                    merge_mode = False  # Reached \end{enumerate>
                else:
                    current_paragraph.append(p.strip()) 
            else:
                if p.strip().startswith('\\begin{enumerate}'):
                    merge_mode = True  # Reached \begin{enumerate}
                else:
                    # Append current paragraph
                    if current_paragraph:
                        grouped_paragraphs.append('\n'.join(current_paragraph))
                        current_paragraph = []

                    # Add the paragraph to the current paragraph
                    current_paragraph.append(p.strip())

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
    
    # Grouped paragraphs
    grouped_indices = set()

    # Store all merged pagraphs
    grouped_paragraphs = []

    for i in range(len(paragraphs)):
        # Skip paragraph if grouped already
        if i in grouped_indices:
            continue  
        
        current_group = [i]  # Start with current paragraph index
        for j in range(i + 1, len(paragraphs)):
            if j not in grouped_indices and similarity_matrix[i][j] > 0.4:
                current_group.append(j)  # Add similar paragraph indices
                grouped_indices.add(j)  # Mark index as grouped
        
        # Add as a merged paragraph
        grouped_paragraphs.append('\n'.join([paragraphs[idx] for idx in current_group]))

    return grouped_paragraphs

def extract_content(tex_file):
    with open(tex_file, 'r') as file:
        content = file.read()
    
    # with open("./before.txt", 'w+', encoding='utf8') as txtfile:
    #     txtfile.write(content)
    content = remove_latex_formatting(content)
    # with open("./after.txt", 'w+', encoding='utf8') as txtfile:
    #     txtfile.write(content)
        
    # Find sections using regex
    section_regex = r'\\section{([^}]+)}\n(.*?)(?=\\section|\Z)'
    sections = re.findall(section_regex, content, re.DOTALL)

    extracted_content = []
    
    for section_title, section_content in sections:
        paragraphs = organize_paragraphs(section_content)
        # print("Num paragraphs:", len(paragraphs))
        # for i in range(len(paragraphs)):
        #     print(paragraphs[i])
        #     print("====")
        # print()
        
        similar_paragraphs = merge_similar_paragraphs(paragraphs)
        # print("Num merged paragraphs:", len(similar_paragraphs))
        # for i in range(len(similar_paragraphs)):
        #     print(similar_paragraphs[i])
        #     print("===============")
        # print("------------------------------------") 
        
        for p in similar_paragraphs:
            extracted_content.append([extract_keywords(p), p])
 
    # print()
    # print()
    return extracted_content

# Based off of ChatterBot trainers.py: _generate_export_data()
def generate_export_data(extracted_content):
    result = []
    for section in extracted_content:
        result.append([section["in_response_to"], section["text"]])

    return result

# Based off of ChatterBot trainers.py: export_for_training()
def export_for_training(extracted_content, file_path='./export.json'):
    #Create a file from the extracted content that can be used to train other chat bots.
    export = {'conversations': extracted_content}
    with open(file_path, 'w+', encoding='utf8') as jsonfile:
        json.dump(export, jsonfile, ensure_ascii=False)

def main():
    tex_file = 'ch2_SectionsOnly.tex' # Full textbook: 'book.tex'
    export_file = './export.json'
    
    extracted_content = extract_content(tex_file)
    export_for_training(extracted_content, export_file)
    
    print(tex_file, 'converted into training json:', export_file)

if __name__ == "__main__":
    main()
