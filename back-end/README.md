## How to run for demo
All training data are in training-jsons folder. 
To train & run chatbot use "python bestMatchChatBot.py".

## Backend documentation


### Generate training files (`generateTrainingJson.py`)
1. Parse through textbook latex source, stripping it of the latex formatting
2. For each section of the textbook (1.1, 1.2, etc), parse into paragraphs and merge any consecutive paragraphs that are talking about the same topic into one chunk of text (these related paragraphs are identified based on a calculated similarity score that must reach our specified similarity threshold).
3. I explored 3 different methods to extract keywords for each chunk of text:
   - RAKE (Rapid Automatic Keyword Extraction) – identify keywords/key phrases from text based on frequency
   - Grammar patterns – extract noun phrases & use the most frequent ones as keywords
   - LDA (Latent Dirichlet Allocation): treats text as “bag-of-words” so that the order of words doesn’t matter, converts chunks of text into list of words and adds them to a dictionary to train the model on, we can specify num_topics to limit the number of topics/groups it creates
4. Format these (keywords, chunk-of-text) pairs into json files for chatbot training (it can take multiple json files)

### Chatbot training (`bestMatchChatBot.py`)
- Trained on jsons generated from all 3 methods mentioned above (because all 3 combined has more comprehensive/representative keywords than any of them individually)
- Use BestMatch logic adapter to select the best response
  - Can specify a similarity threshold
- Specify statement_comparison_function to calculate similarity between user input & keywords that will be passed to BestMatch logic adapter
May need to run:
- python -m spacy download en_core_web_lg
- pip3 install "spacy>=2.1,<2.2"


### Further work/improvements needed:
- Improve statement_comparison_function to yield better matches: create custom function using similar logic from ChatterBot’s JaccardSimilarity
- Stripping latex formatting still needs to be refined— for simplicity & time’s sake, code & tables have been excluded (will be processed in later development) 
- Keyword extraction can still be improved/tweaked
- Currently some of the chatbot responses are very long: ideally we can shorten/summarize them to make them more concise responses
