import json
import re
import unicodedata
import contractions
import inflect as inflect
import os
from nltk.corpus import stopwords
import csv
stopwords = (stopwords.words('english'))
# stopwords = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
import unidecode
from bs4 import BeautifulSoup
from spacy.lemmatizer import Lemmatizer
import spacy
import ijson
import pandas as pd
from spacy.lookups import Lookups



# STEP 1: Access just bodytext of document in order to clean
# doc_content = df["value"][0]["Document"]["Content"]  # type = str

class Row_object:
    def __init__(self, Jurisdiction, Location, ContentType, Byline, WordLength, Date, Title, Content, SourceName):
        self.Jurisdiction = Jurisdiction
        self.Location = Location
        self.ContentType = ContentType
        self.Byline = Byline
        self.WordLength = WordLength
        self.Date = Date
        self.Title = Title
        self.Content = Content
        self.SourceName = SourceName

# Pre-Tokenization functions
def Soup_to_bodyText(text):
    soup1 = BeautifulSoup(text, "html.parser")
    doc_content = str(soup1.find("nitf:body.content"))
    print(type(doc_content))
    #remove urls
    soup2 = BeautifulSoup(doc_content, "html.parser")
    for s in soup2.select("url"):
        s.extract()
    print(soup2)
    #remove
    return str(soup2)

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def remove_accented_chars(text):
    """remove accented characters from text, e.g. café"""
    text = unidecode.unidecode(text)
    return text


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)

def remove_new_line_characters(text):
    """Replace new line characters"""
    return re.sub('\s+', ' ', text)

def remove_bracketed_text(text):
    doc_content = re.sub("[\(\[].*?[\)\]]", " ", text)
    return doc_content


# def remove_long_short_words(text): #This should be done after stop words and punctuation
#     list_of_removed = []
#     for word in text.split():
#         if len(word) > 20 or len(word) < 2:
#             list_of_removed.append(word)
#             text = text.replace(word, "")
#     print(list_of_removed)
#     return text
# doc_content = remove_long_short_words(doc_content)


# #TODO: POST-Tokenization _____________________
# Tokenize words
# Using Spacy's English tokenizer
# nlp = spacy.load("en_core_web_sm")
# doc = nlp(doc_content)
# print(type(doc))
# #lemmatize
# for token in doc:
#     print(token.text, token.pos_, token.lemma)
# doc_content = Lemmatizer(doc)

lookups = Lookups()
lookups.add_table("lemma_rules", {"noun": [["s", ""]]})
lemmatizer = Lemmatizer(lookups)
#
# doc_content = doc_content.split()

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


# def replace_numbers(words):
#     """Replace all interger occurrences in list of tokenized words with textual representation"""
#     p = inflect.engine()
#     new_words = []
#     for word in words:
#         if word.isdigit():
#             print(word)
#             new_word = p.number_to_words(word)
#             new_words.append(new_word)
#         else:
#             new_words.append(word)
#     return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords:
            new_words.append(word.strip())
    return new_words

def LDA_clean(input_content):

    soup_content = Soup_to_bodyText(input_content)
    html_content = remove_html_tags(soup_content)
    accented_content = remove_accented_chars(html_content)
    contract_content = replace_contractions(accented_content)
    new_line_content = remove_new_line_characters(contract_content)
    token_input = remove_bracketed_text(new_line_content)
    ##TOKENIZE
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(token_input)
    doc = [token.lemma_ if token.lemma_ != '-PRON-' else token.text for token in doc]
    non_ascii = remove_non_ascii(doc)
    lower_content = to_lowercase(non_ascii)
    sans_punctuation = remove_punctuation(lower_content)
    # sans_numbers = replace_numbers(sans_punctuation)
    sans_stops = remove_stopwords(sans_punctuation)
    return " ".join(sans_stops)
#TODO: SOMETHING IS WRONG WITH THE DATES/NUMBERS/MOONTHS IN THE TEXTBODY>>>FIX
#TODO: Delete duplicates, might have to be in pandas dataframe
#TODO: remove single character words

directory = '/Users/njjones14/PycharmProjects/Big_Tech_Regulation/Big_Tech_Regulation_data/'


# with open("/Users/njjones14/PycharmProjects/Big_Tech_Regulation/practice_json.json", encoding='utf-8') as f:
#     content = ijson.items(f, "value")
#     for o in content:
#         for i in range(0,1):
#             soup_content = Soup_to_bodyText(o[i]["Document"]["Content"])
#             print(soup_content)
#             html_content = remove_html_tags(soup_content)
#             print(html_content)
#             accented_content = remove_accented_chars(html_content)
#             print(accented_content)
#             contract_content = replace_contractions(accented_content)
#             print(contract_content)
#             new_line_content = remove_new_line_characters(contract_content)
#             print(new_line_content)
#             token_input = remove_bracketed_text(new_line_content)
#             print(token_input)
#             ##TOKENIZE
#             nlp = spacy.load("en_core_web_sm")
#             doc = nlp(token_input)
#             token_list = [token.orth_ for token in doc]
#             non_ascii = remove_non_ascii(token_list)
#             lower_content = to_lowercase(non_ascii)
#             sans_punctuation = remove_punctuation(lower_content)
#             # sans_numbers = replace_numbers(sans_punctuation)
#             sans_stops = remove_stopwords(sans_punctuation)



# # TODO: THIS WORKS
def parse_single_file(filename):
    with open("/Users/njjones14/PycharmProjects/Big_Tech_Regulation/Big_Tech_Regulation_data/" + filename) as f:
        content = ijson.items(f, "value")
        row_list = []
        for o in content:
            print(type(o))
            for i in range(0, len(o)):
                print(filename)
                print(i)
                if o[i]["Document"]["Content"] is not None: #TODO: or I could drop this document, figure this out
                    row_list.append(Row_object(o[i]["Jurisdiction"], o[i]["Location"], o[i]["ContentType"], o[i]["Byline"],
                                           o[i]["WordLength"],
                                           o[i]["Date"],
                                           o[i]["Title"],
                                           LDA_clean(o[i]["Document"]["Content"]),
                                           o[i]["Source"]["Name"]))
    return row_list

list_of_files = []

for file in os.listdir(directory):
    list_of_files.append(file)

# for filename in list_of_files[0:10]:
#     list_of_row_objects = parse_single_file(filename)
#     with open("/Users/njjones14/PycharmProjects/Big_Tech_Regulation/cleaned_csv_files/" + filename + ".csv",
#               "w") as csvfile:
#         row_writer = csv.writer(csvfile)
#         for i in list_of_row_objects:
#             row_writer.writerow(
#                 [i.Title, i.Byline, i.Date, i.Jurisdiction, i.Location, i.ContentType, i.WordLength, i.Content,
#                  i.SourceName])

if __name__ == "__main__":
    for filename in os.listdir(directory):
        
        list_of_row_objects = parse_single_file(filename)
        with open("/Users/njjones14/PycharmProjects/Big_Tech_Regulation/cleaned_csv_files/" + filename + ".csv",
                  "w") as csvfile:
            row_writer = csv.writer(csvfile)
            for i in list_of_row_objects:
                row_writer.writerow(
                    [i.Title, i.Byline, i.Date, i.Jurisdiction, i.Location, i.ContentType, i.WordLength, i.Content,
                     i.SourceName])
    csv_list = []
    for csv_file in os.listdir("/Users/njjones14/PycharmProjects/Big_Tech_Regulation/cleaned_csv_files/"):
        df = pd.read_csv(csv_file)
        csv_list.append(df)
    result = pd.concat(csv_list)
    result.to_csv("/Users/njjones14/PycharmProjects/Big_Tech_Regulation/corpus_cleaned")
















