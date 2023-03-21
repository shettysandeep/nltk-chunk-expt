# coding=utf-8

"""
Information extraction usinfg NLTK chunking. See Section 2 of https://www.nltk.org/book/ch07.html
Define chunks with regular expressions of parts-of-speech tags. 
E.g: grammar1 = "CHUNK: {<RB><VB*><NN*><.*>*}" 
The term in '{}' is a POS-tag-based regular expression that the code will search through documents
and extract phrases that match this expression

__author__: Sandeep Shetty
__date__: September 29, 2022

"""

import pandas as pd
import nltk
from nltk.tokenize import (
    word_tokenize,
    sent_tokenize,
    RegexpTokenizer,
)  # remove stop words

tokenizer = RegexpTokenizer(r"\w+")
nltk.download("punkt")
# from collections import defaultdict


class nltkDecorator:
    @staticmethod
    def pretty_chunks(func):
        def inner(self, *args):
            doc_chunk = func(self, *args)
            doc_pparse = {}
            for keys in doc_chunk:  # CAN HAVE MORE THAN ONE CHUNK
                # print("----Doc {}".format(keys))
                em = []
                for items in doc_chunk[keys]:  # FOR EACH CHUNK WITHIN A DOCUMENT
                    for sitems in items:  # FOR ITEMS IN EACH CHUNK
                        # print(sitems)
                        a, b = sitems
                        if b in ["RB", "VB", "NN", "NNS", "NNP", "NNPS", "JJ"]:
                            em.append(a)  # APPEND THE ABOVE POS's
                    # print(em)
                if len(em) != 0:
                    doc_pparse[keys] = em
            return doc_pparse

        return inner

    # Dataset - Extracting Columns
    @staticmethod
    def column_extractor(dat, col, ratings):  # pandas dataframe
        """Returns Pandas dataframe"""
        dat = dat[col]
        subset_data = dat.loc[dat[col[1]].isin(ratings)].copy()
        subset_data.dropna(inplace=True)
        subset_data.drop_duplicates(inplace=True)
        return subset_data


class nltkChunkExtractor:
    """Chunk phrased from documents based on POS-tagged regex

    grammar : str
      The POS-based regular expression: e.g "CHUNK: {<RB><VB*><NN*><.*>*}"
    keep_words: int, optional
      Retains phrases that are 3 or more words
    corpus: Pandas Dataframe
      Dataframe of column/s with text data
    chunk_name: string, not required
      The grammar requires a key for the phrases identified.  This is
    important to differentiate the chunks of interest.  Define this
    inside the 'grammar' (e.g. 'CHUNK' above in 'grammar').
    This attribute picks from the grammar.

    Returns
    -------

    dictionary indexed by document with a match, the values are a list of
    strings/phrases (without POS tags)


    """

    def __init__(self, grammar):
        self.grammar = grammar
        self.chunk_name = None
        self.keep_words = 2
        self.corpus = None

    @property
    def keep_words(self):
        return self._keep_words

    @keep_words.setter
    def keep_words(self, value):
        self._keep_words = value

    @property
    def chunk_name(self):
        self._chunk_name = self.grammar.split(":")[0].strip()
        return self._chunk_name

    @chunk_name.setter
    def chunk_name(self, value):
        self._chunk_name = value

    @property
    def corpus(self):
        return self._corpus

    @corpus.setter
    def corpus(self, value):
        self._corpus = value

    @staticmethod
    def pos_tagger(docs):
        """Simple POS tagging
        Input: string
        Output: List of words and POS tags"""
        docs = (lambda x: x[0] if (len(x) > 0 and isinstance(x, list)) else x)(docs)
        sentences = nltk.sent_tokenize(docs)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    def subtree_extract(self, docs):
        # , doc=self.doc, grammar=self.grammar, keep_words=2):
        """
        Returns chunked phrases from the text
        Input: String (with multiple sentences)
        Output: '[(was, 'VB'),..]'
        """
        # print(docs)
        sentence = self.pos_tagger(docs)
        outsubtree = []
        cp = nltk.RegexpParser(self.grammar)
        for sents in sentence:
            tree = cp.parse(sents)
            for subtree in tree.subtrees():
                if (subtree.label() == self.chunk_name) and (
                    len(subtree) > self.keep_words
                ):
                    outsubtree.append(subtree)
        return outsubtree

    @nltkDecorator.pretty_chunks
    def execute_parse(self):
        doc_chunk = {}
        for index, docs in enumerate(self.corpus):
            doc_chunk[index] = self.subtree_extract(docs)
        return doc_chunk
