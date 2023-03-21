# Examples of grammar chunks to extract

GRAMMAR_LIST = {
    "GRM1": r"CHUNK1: {<RB><VB*><NN*><.*>*}",
    "GRM2": r"CHUNK2: {(<VBG>|<VB>) <TO> <.*><.*>*<,|.>?}",
    "GRM3": r"CHUNK3: {<DT|PP\$>?<JJ>*<NN>}",
    "GRM4": r"CHUNK4: {<JJ>*<NN>}",
}


MC_LIST = {
    "GRM1": "noun3: {(<NN.*>|<PRP>)(<IN|CC><DT>*<PRP$>*<JJ.*>*<NN.*>)}",
    "GRM2": "noun4: {(<NN.*>|<PRP>)(<IN|CC><DT>*<JJ.*>*<NN.*><CC>*<PRP$>*<NN.*>*)}",
    "GRM3": "noun3: {(<NN.*>|<PRP>)<VBN>*<TO><.*>*<NN.*>*}",
}
