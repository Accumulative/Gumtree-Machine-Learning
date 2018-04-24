# Natural Language Processing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
#dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

# Cleaning the texts
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []

import glob

all_files = glob.glob("out*.csv")     # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f, header=None) for f in all_files)
dataset   = pd.concat(df_from_each_file, ignore_index=True)


for i in range(0, len(dataset)):
    review = re.sub('[^a-zA-Z]', ' ', dataset[1][i])#dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = np.asarray(dataset.iloc[:, 0].values, dtype=np.int64)

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

diffence = [(float(y_pred[i]) - float(y_test[i]))/float(y_test[i])  if float(y_test[i]) != 0 else 10000 for i in range(0, len(y_test))]
diffenceval = [1  if (float(a) < 0.2 and float(a)> -0.2) else 0 for a in diffence]

print(sum(diffenceval)/len(diffenceval))

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, diffenceval)