# coding=utf-8

"""
Sentiment-based phrase extraction before passing to the chunking

__author__: Sandeep Shetty
__date__: October 12, 2022

"""
import os
import pandas as pd
import nltk
from grammar_chunks import GRAMMAR_LIST, MC_LIST
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from textblob import TextBlob
from nltkChunkExtractor import nltkDecorator, nltkChunkExtractor


tokenizer = RegexpTokenizer(r"\w+")
nltk.download("punkt")


def sentimentExtractor(doc_list, neg=True, score=0):
    """Returns sentences from a doc that meet a provided sentiment.
        if neg=True --> negative sentiment sentences are returned (with score<0)
        if neg=False --> positive sentiment sentences are returned (with score>0)
        Intensity is not retured and neutral sentiments are ignored.
    Output: Dict: [doc #] = list of sentences
    """
    collect_sent = {}
    for index, doc in enumerate(doc_list):
        text_blob = TextBlob(doc)
        text_list = []
        for sent in text_blob.sentences:
            sentiment = sent.sentiment[0]
            if neg:
                if sentiment < score:
                    text_list.append((sent.raw, sentiment))
            else:
                print("here")
                if sentiment > score:
                    text_list.append((sent.raw, sentiment))
            if len(text_list) > 0:
                collect_sent[index] = text_list
    return collect_sent


# Read data
cprs = pd.read_csv("../../../reconfigured_CPARS_dataset.csv")

# Set arguments for column_extractor()
col = ["Quality", "quality_rating"]
ratings = ["satisfactory", "marginal"]

# Subset data
dataset = nltkDecorator.column_extractor(dat=cprs, col=col, ratings=ratings)
quality_comments = dataset.Quality.to_list()

# Extract sentiments
return_sentiment = sentimentExtractor(quality_comments, score=0.1)
# collect all the statements
sent_bank = []
for a, b in return_sentiment.items():
    for c in b:
        d, e = c
        sent_bank.append(d)


print(quality_comments[:5])
# Grammar
print(GRAMMAR_LIST)
grml1, grml2, grml3, grml4 = GRAMMAR_LIST.values()
grm1, grm2, grm3 = MC_LIST.values()

# instantiate and extract phrases
ce1 = nltkChunkExtractor(grammar=grml1)
ce2 = nltkChunkExtractor(grammar=grml2)
ce3 = nltkChunkExtractor(grammar=grml4)
# ce1._keep_words = 2
ce1._corpus = sent_bank
ce2._corpus = sent_bank
ce3._corpus = sent_bank

# print("POS chunk sequence {}".format(ce1.grammar))
for i in [ce1, ce2, ce3]:
    print("----.{}".format(i.grammar))
    print(i.execute_parse())
