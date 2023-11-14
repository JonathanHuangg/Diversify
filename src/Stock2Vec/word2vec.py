import pandas as pd
from sklearn.preprocessing import normalize
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize
import string
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
import numpy as np

########## NUM DIMENSION ##########
num_dim = 10


######### HELPER FUNCTIONS #########
def preprocess(text):
    text = text.lower()
    text = ''.join([word for word in text if word not in string.punctuation])
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def vectorize(sentence):
    words = sentence.split()
    words_vecs = [w2v_model.wv[word] for word in words if word in w2v_model.wv]
    if len(words_vecs) == 0:
        return np.zeros(num_dim)
    words_vecs = np.array(words_vecs)
    return words_vecs.mean(axis=0)

######## START OF PREPROCESSING ########

# read scrapped data
data = pd.read_csv('CompanyDescriptions/results/result_wikipedia.csv', header=None)

# preprocess sentences
stop_words = set(stopwords.words('english'))
y_train_preprocessed = data[1].apply(preprocess)

# train word2vec model
sentences = [sentence.split() for sentence in y_train_preprocessed]
w2v_model = Word2Vec(sentences, vector_size=num_dim, window=5, min_count=5, workers=4)

# get stock vector
y_train_vec = np.array([vectorize(sentence) for sentence in y_train_preprocessed])

###### NORMALIZATION ######

# Calculate the Frobenius norm
frobenius_norm = np.linalg.norm(y_train_vec)

# Normalize the matrix
normalized_matrix = y_train_vec / frobenius_norm

#print
normalized_matrix

######## DATA SAVING ########
DF = pd.DataFrame(y_train_vec)
DF.insert(loc=0, column=None, value=data[0])
DF.iloc[1:,:]

##### uncomment to save ####
f_name = f'stock2vec_{num_dim}.csv'
# DF.to_csv(f_name, header=None, index=None)

######## CSV to DF ########

stock_vector = pd.read_csv('f_name', header=None)
# print(stock_vector)

######## For Testing ########

tickerA = 'AAPL'
tickerB = 'MSFT'

a = stock_vector[stock_vector[0] == tickerA].to_numpy()[0][1:]
b = stock_vector[stock_vector[0] == tickerB].to_numpy()[0][1:]
print(tickerA, a)
print(tickerB, b)

dist = np.linalg.norm(a-b)

######## For Printing ########

print(dist)
