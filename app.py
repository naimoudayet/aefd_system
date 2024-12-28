import os
import re
import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import arabic_reshaper
from bidi.algorithm import get_display


# Function to load text files from a folder
def load_text_files(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                texts.append(f.read())
    return texts


# Function to clean text by removing non-Arabic characters
def clean_text(text):
    return re.sub(r'[^\u0600-\u06FF\s]', '', text)


# Function to extract words containing Hamza
def extract_hamza_words(text):
    hamza_regex = r'[\u0621\u0623\u0624\u0626]'
    words = text.split()
    return [word for word in words if re.search(hamza_regex, word)]


# Function to extract the context around a Hamza in a word
def get_hamza_context(word):
    hamza_regex = r'[\u0621\u0623\u0624\u0626]'
    for i, char in enumerate(word):
        if re.match(hamza_regex, char):
            before = word[i-1] if i > 0 else ''
            after = word[i+1] if i < len(word)-1 else ''
            return before, char, after
    return None


# Function to extract diacritic following a Hamza
def extract_diacritic(word):
    diacritic_regex = r'[\u0621\u0623\u0624\u0626]([\u064B-\u0652])'
    match = re.search(diacritic_regex, word)
    if match:
        return match.group(1)  # Diacritic following Hamza
    return None


# Function to process a single text file and extract Hamza-related data
def process_text(text):
    cleaned_text = clean_text(text)
    hamza_words = extract_hamza_words(cleaned_text)
    data = []
    for word in hamza_words:
        context = get_hamza_context(word)
        if context:
            before, hamza, after = context
            label = extract_diacritic(word)
            if label:
                data.append({'before': before, 'hamza': hamza, 'after': after, 'label': label})
    return data


def main():
    # Step 1: Load all texts
    folder_path = './texts'
    all_texts = load_text_files(folder_path)

    # Step 2: Process the texts in parallel using ProcessPoolExecutor
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        processed_data = list(executor.map(process_text, all_texts))

    # Flatten the list of data
    data = [item for sublist in processed_data for item in sublist]

    # Prepare the feature set X and labels y
    X = [[ord(item['before']) if item['before'] else 0,
          ord(item['hamza']),
          ord(item['after']) if item['after'] else 0] for item in data]
    y = [item['label'] for item in data]

    # Check if a model already exists
    model_filename = 'hamza_model.pkl'
    if os.path.exists(model_filename):
        with open(model_filename, 'rb') as model_file:
            model = pickle.load(model_file)
    else:
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Save the trained model to disk
        with open(model_filename, 'wb') as model_file:
            pickle.dump(model, model_file)

        # Evaluate the model
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
                results.append(hamza + predicted_label)
            else:
                results.append(word)  # Append the word if no Hamza found
        reshaped_text = '  '.join(results)

        # Reshape Arabic text for correct rendering
        reshaped_text = arabic_reshaper.reshape(reshaped_text)
        return get_display(reshaped_text)  # Display with correct bidirectional support


    # Test the function
    output = predict_diacritics("النبإ")
    print("Predicted diacritics:", output)

    # Measure execution time
    end_time = time.time()
    execution_time = (end_time - start_time) / 60
    print(f"The function took {execution_time:.2f} minutes to execute.")


if __name__ == '__main__':
    main()
