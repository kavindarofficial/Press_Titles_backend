# api/utils.py
import pandas as pd
import jellyfish  # For phonetic similarity algorithms (Soundex, Metaphone)
from difflib import SequenceMatcher  # For text similarity
from fuzzywuzzy import fuzz  # For fuzzy matching
from sklearn.feature_extraction.text import TfidfVectorizer  # For vector-based similarity
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Helper functions
profane_words_df = pd.read_csv(r"C:\stuff\Automated-Online-System-to-Verify-Duplicate-Press-Titles\backend\profanity_en.csv")
disallowed_words = profane_words_df['canonical_form_1'].values

# 1. Function to check for phonetic similarity using Soundex or Metaphone
def phonetic_similarity(title1, title2):
    return jellyfish.soundex(title1) == jellyfish.soundex(title2)

# 2. Function to calculate text similarity using Levenshtein distance
def text_similarity(title1, title2):
    return fuzz.ratio(title1.lower(), title2.lower())

# 3. Function to calculate vector-based similarity using TF-IDF and cosine similarity
def vector_similarity(new_title, existing_titles):
    vectorizer = TfidfVectorizer().fit_transform([new_title] + list(existing_titles))
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])
    return np.max(cosine_sim) * 100  # Return percentage similarity

# 4. Check if the title contains disallowed words
def contains_disallowed_words(title):
    for word in disallowed_words:
        if word.lower() in title.lower():
            return True
    return False

# 5. Function to enforce title combination rules
def title_combination_check(new_title, existing_titles):
    for existing_title in existing_titles:
        if new_title.lower() in existing_title.lower():
            return True
    return False

# 6. Function to enforce prefix/suffix rules (can be extended)
disallowed_prefix_suffix = ["The", "India", "Samachar", "News"]  # Example list

def check_disallowed_prefix_suffix(title):
    for prefix in disallowed_prefix_suffix:
        if title.startswith(prefix) or title.endswith(prefix):
            return True
    return False

# 7. Function to calculate the verification probability score
def verification_probability(similarity_score):
    return max(0, 100 - similarity_score)  # Ensures a percentage between 0-100%

# Main Function: Check new title submission
def verify_title(new_title, existing_titles):
    # Check for phonetic similarity
    for existing_title in existing_titles:
        if phonetic_similarity(new_title, existing_title):
            return {"status": "Rejected", "reason": "Phonetic similarity detected", "probability": 0}
    
    # Check for spelling similarity using Levenshtein distance
    for existing_title in existing_titles:
        similarity_score = text_similarity(new_title, existing_title)
        if similarity_score > 80:  # 80% similarity threshold
            return {"status": "Rejected", "reason": f"Too similar to '{existing_title}'", "probability": verification_probability(similarity_score)}
    
    # Check for vector-based similarity
    vector_sim = vector_similarity(new_title, existing_titles)
    if vector_sim > 80:  # 80% threshold for vector similarity
        return {"status": "Rejected", "reason": "Too similar based on vector similarity", "probability": verification_probability(vector_sim)}
    
    # Check for disallowed words
    if contains_disallowed_words(new_title):
        return {"status": "Rejected", "reason": "Contains disallowed words", "probability": 0}
    
    # Check for title combination rules
    if title_combination_check(new_title, existing_titles):
        return {"status": "Rejected", "reason": "Combination of existing titles not allowed", "probability": 0}
    
    # Check for disallowed prefixes or suffixes
    if check_disallowed_prefix_suffix(new_title):
        return {"status": "Rejected", "reason": "Contains disallowed prefix or suffix", "probability": 0}

    # If all checks pass
    return {"status": "Accepted","reason":None, "probability": 100}


# def verify_title(new_title, existing_titles):
#     # Same as your current logic, adapted for Django
#     # Make sure to handle profanity words, disallowed words, etc.
#     return True, "Title is valid", 1.0  # Example output
