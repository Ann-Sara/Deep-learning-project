import numpy as np
import tensorflow as tf
from keras.models import load_model
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import joblib
import pandas as pd

stop_word = set(stopwords.words('english'))
stemmer = PorterStemmer()

model = load_model('model.h5')

input_text = 'lowers blood pressure and cholesterol let  s face it , age should be nothing more than a number it  s okay to want to hold on to your young body as long as you can with increasing longevity for an increasing segment of the population , this is the frontier for the new millennium - dr virgil howard view more about a new lifespan enhancement press here we ship right to your door sorry not for me and the twenty trials compared the same lactam all cause fatality the most significant and objective outcome was not reduced by the addition of aminoglycosides clinical and bacteriological failure which may be prone to bias with nonblinded trials and are of much lesser relevance to patients were not significantly different the wind at first sent him spinning away to the south , but he continued to rise until he was above the air currents , and the storm raged far beneath him'

tokens = word_tokenize(input_text)
tokens_wo_punkt = [word for word in tokens if word.isalpha()]
token = [word.lower() for word in tokens_wo_punkt if word.lower() not in stop_word]
stemmed_word = [stemmer.stem(word) for word in token]
text = " ".join(stemmed_word)
print(text)

# Load the pre-trained vectorizer
vectorizer = joblib.load('vectorizer.joblib')

# Transform the text using the pre-trained vectorizer
email_vector = vectorizer.transform([text])
word_counts = np.asarray(email_vector.sum(axis=0)).ravel()

# Define the phishg_word list
phishg_word = ['languag', 'http', 'enron', 'univers', 'use', 'inform', 'one', 'linguist', 'pleas', 'new', 'mail', 'would', 'subject', 'email', 'address', 'work', 'time', 'list', 'get', 'compani', 'paper', 'ect', 'com', 'order', 'de', 'make', 'report', 'may', 'also', 'like', 'includ', 'us', 'name', 'program', 'confer', 'system', 'peopl', 'busi', 'call', 'receiv', 'follow', 'free', 'send', 'need', 'year', 'day', 'research', 'market', 'messag', 'interest', 'know', 'price', 'number', 'gener', 'comput', 'www', 'english', 'first', 'provid', 'fax', 'money', 'see', 'thank', 'take', 'servic', 'want', 'look', 'go', 'word', 'two', 'product', 'state', 'could', 'present', 'chang', 'avail', 'develop', 'form', 'way', 'said', 'edu', 'mani', 'workshop', 'question', 'contact', 'discuss', 'offer', 'site', 'hou', 'book', 'file', 'group', 'process', 'week', 'differ', 'web', 'issu', 'well', 'date', 'even']

# Ensure phishg_word contains exactly 100 words

feature_names = vectorizer.get_feature_names()

# Create DataFrame with 100 columns
new_df = pd.DataFrame(columns=phishg_word)
print(new_df.shape)
# Add a new row to the DataFrame with word count
# Create a dictionary to store word counts
counts_dict = dict(zip(feature_names, word_counts))

# Add a new row to the DataFrame with word counts and corresponding label
row_data = {word: counts_dict[word] for word in phishg_word}
print(row_data)
new_df = new_df.append(row_data, ignore_index=True)
new_df=pd.DataFrame(new_df)
print(type(new_df))
input_data = new_df.values

# Ensure the input data type is float
input_data_float = input_data.astype(float)

# Predict with the loaded model
prediction = model.predict(input_data_float)
print(prediction)
# Print the prediction
print("Model Prediction:")
print(prediction)

pred=int(round(prediction[0][0]))
print(pred)
label=['Phishing email','Safe email']

# Print the prediction
print("Model Prediction:")
print(label[pred])
