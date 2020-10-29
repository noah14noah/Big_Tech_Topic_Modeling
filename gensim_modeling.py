from gensim.models import Phrases
from Import_and_Clean import directory
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.corpora import Dictionary

#NEED list of Unicode strings for phrases
df_columns = ["Title", "Byline", "Date", "Jurisdiction", "Location", "ContentType", "WordLength", "Content", "SourceName"]

with open(directory + "cleaned_corpus") as f:
    clean_corpus = pd.read_csv(f)
    clean_corpus.columns = df_columns

list_of_texts = []
for idx, text in clean_corpus.iterrows():
    list_of_texts.append(text)

bigram = Phrases(list_of_texts, min_count=20)

for idx in range(len(list_of_texts)):
    for token in bigram[list_of_texts[idx]]:
        if '_' in token:
            # Token is a bigram, add to document.
            list_of_texts[idx].append(token)

#Create Dictionary
dictionary = Dictionary(list_of_texts)

# Filter out words that occur less than 20 documents, or more than 50% of the documents.
dictionary.filter_extremes(no_below=20, no_above=0.5)

# Bag-of-words representation of the documents.
corpus = [dictionary.doc2bow(doc) for doc in list_of_texts]













