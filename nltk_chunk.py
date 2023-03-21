import os
import pandas as pd
from nltkChunkExtractor import nltkDecorator, nltkChunkExtractor
from grammar_chunks import *

# Read data
cprs = pd.read_csv("../../../CPARS_combined_data.csv")

# Set arguments for column_extractor()
col = ["Quality", "quality_rating"]
ratings = ["satisfactory", "marginal"]

# Subset data
dataset = nltkDecorator.column_extractor(dat=cprs, col=col, ratings=ratings)
quality_comments = dataset.Quality.to_list()

# Define Grammar Chunk to extract
my_grm = r"chunk1: {<DT>?<NN.?>+.*<JJ><NN.?>+}"

print(GRAMMAR_LIST)

# Instantiate class
ce1 = nltkChunkExtractor(grammar=my_grm)
ce1._keep_words = 2
ce1._corpus = quality_comments

print("POS chunk sequence {}".format(ce1.grammar))
c2 = ce1.execute_parse()
print(c2)
