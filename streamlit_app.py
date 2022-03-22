# streamlit

import streamlit as st
import pandas as pd
import json
import time
import pickle
import collections
from rapidfuzz import fuzz
from itertools import islice


st.title("Search Engine")
st.write("""For a given text query search the corpus of the provided documents and return the
most relevant document. Expose the module as API which takes a text input and returns
the most relevant document. API should also have a parameter to get top n relevant
documents instead of just top 1. The dataset will contain 2 fields, text and a unique id,
return both the fields along with the similarity score in the API response.""")

@st.cache(allow_output_mutation=True)
def load_products():
    folder_path = "C:\\Users\\apurnaik\\OneDrive - Deloitte (O365D)\\Commback\\Projects\\Apps\\SearchEngine\\"
    return pickle.load(open(folder_path+'products.pkl',"rb"))

def take(numdocs, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, numdocs))

def find_relevant_docs(searchtext, numdocs):
    d = {fuzz.QRatio(searchtext, item['text']):item for item in products}
    od = collections.OrderedDict(sorted(d.items(), reverse=True))
    res = take(numdocs, od.items())
    df = pd.DataFrame(res, columns = ['similarity_score', 'text'])
    df1 = df['text'].apply(lambda x: pd.Series(x))
    df1['similarity_score'] = df['similarity_score'].copy()
    return df1

products = load_products()
st.write('Corpus loaded, its length:', len(products))

searchtext = st.text_input('Please enter the search string','running shorts')
# more than 5 characters
if len(searchtext) < 5:
    st.error("You can't use less than 5 characters")
else:
    pass

# only alphabets and spaces
if all(x.isalpha() or x.isspace() for x in searchtext):
    pass
else:
    st.error("Only alphabetical letters and spaces")

numdocs = st.number_input('Please enter number of relevant documents to be returned', min_value=1, max_value=20)

if st.checkbox('Return Results'):
    df1 = find_relevant_docs(searchtext , numdocs)
    df1.index += 1 
    st.write(df1)


