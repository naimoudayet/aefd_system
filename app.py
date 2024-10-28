import os
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

def load_text_files(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                texts.append(f.read())
    return texts

# Step 1: Load Text Files
folder_path = './texts.txt'
all_texts = load_text_files(folder_path)

# Step 2: Clean and Extract Hamza Words
def clean_text(text):
    return re.sub(r'[^\u0600-\u06FF\s]', '', text)

def extract_hamza_words(text):
    hamza_regex = r'[\u0621\u0623\u0624\u0626]'  # Match Hamza in different forms
    words = text.split()
    return [word for word in words if re.search(hamza_regex, word)]

cleaned_texts = [clean_text(text) for text in all_texts]
hamza_words = [extract_hamza_words(text) for text in cleaned_texts]

# Step 3: Extract Context and Diacritic Features for Model Training
def get_hamza_context(word):
    hamza_regex = r'[\u0621\u0623\u0624\u0626]'
    for i, char in enumerate(word):
        if re.match(hamza_regex, char):
            before = word[i-1] if i > 0 else ''
            after = word[i+1] if i < len(word)-1 else ''
            return before, char, after

# Extract context and store data
data = []
for words in hamza_words:
    for word in words:
        context = get_hamza_context(word)
        if context:
            data.append({'word': word, 'context': context})

# Define regex to match Hamza followed by any diacritic
diacritic_regex = r'[\u0621\u0623\u0624\u0626]([\u064B-\u0652])'
def extract_diacritic(word):
    match = re.search(diacritic_regex, word)
    if match:
        return match.group(1)  # Diacritic following Hamza
    else:
        return None  # No diacritic or unsupported case

# Sample data transformation
training_data = []
for item in data:
    before, hamza, after = item['context']
    label = extract_diacritic(item['word'])
    training_data.append({'before': before, 'hamza': hamza, 'after': after, 'label': label})

# Filter out None labels
filtered_data = [item for item in training_data if item['label'] is not None]

# Prepare X and y with filtered data
X = [[ord(item['before']) if item['before'] else 0,
      ord(item['hamza']),
      ord(item['after']) if item['after'] else 0] for item in filtered_data]
y = [item['label'] for item in filtered_data]

# Check if a model already exists
model_filename = 'hamza_model.pkl'
if os.path.exists(model_filename):
    with open(model_filename, 'rb') as model_file:
        model = pickle.load(model_file)
else:
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save the trained model to disk
    with open(model_filename, 'wb') as model_file:
        pickle.dump(model, model_file)

    # Evaluate model
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))

# Function to predict diacritics for a given phrase
def predict_diacritics(phrase):
    words = phrase.split()
    results = []
    for word in words:
        hamza_context = get_hamza_context(word)
        if hamza_context:
            before, hamza, after = hamza_context
            features = [[ord(before) if before else 0,
                         ord(hamza),
                         ord(after) if after else 0]]
            predicted_label = model.predict(features)[0]
            results.append(hamza + predicted_label)  # Append the predicted diacritic
        else:
            results.append(word)  # Append the word if no hamza found
    return ' '.join(results)

# Input for testing
#input_phrase = input("Enter a word or phrase to test: ")
#output = predict_diacritics("نبأ")
output = predict_diacritics("النبإ")
print("Predicted diacritics:", output)
