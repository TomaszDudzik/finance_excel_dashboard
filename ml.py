# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import nltk
from nltk.corpus import stopwords
import string

from etl.bank_etl.ing_csv import ing_csv

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

ing_csv_path = r'C:/Users/dudzi/OneDrive/Python/excel_python/Lista_transakcji_nr_0197050513_061024.csv'

# Preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize and remove stopwords
    tokens = [word for word in text.split() if word not in stop_words]
    
    # Join tokens back into a single string
    return ' '.join(tokens)

# Load your dataset (replace 'your_data.csv' with your actual data file)
df = ing_csv(ing_csv_path)
df = df[['title', 'details']]
df['description'] = df['title'] + ' ' + df['details']
df = df[['description']]

# Preprocess the 'Description' column
df['cleaned_description'] = df['description'].apply(preprocess_text)

# Split the data into features (X) and target (y)
X = df['cleaned_description']
y = df['Category']

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to TF-IDF features
tfidf_vectorizer = TfidfVectorizer(max_features=5000)  # Limit features for performance
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train a Logistic Regression model
lr_model = LogisticRegression(max_iter=100)
lr_model.fit(X_train_tfidf, y_train)

# Make predictions on the test set
y_pred = lr_model.predict(X_test_tfidf)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Optional: Save the trained model and vectorizer for future use
import joblib
joblib.dump(lr_model, 'logistic_regression_model.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')
