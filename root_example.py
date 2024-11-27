import re
import arabic_reshaper
from bidi.algorithm import get_display  # To handle bidirectional text rendering

def normalize_arabic_verb(verb):
    """
    Normalize an Arabic verb to conform to the format 'فَعَلَ'.
    Adds missing diacritics if needed.
    """
    # Define valid diacritics
    fatha = "\u064E"  # َ

    # Strip spaces and ensure the verb has three root letters
    verb = verb.strip()
    root_letters = re.findall(r"[\u0621-\u064A]", verb)  # Extract only Arabic letters

    if len(root_letters) != 3:
        raise ValueError(f"The verb '{verb}' does not have exactly 3 root letters.")

    # Add missing fatha diacritics to conform to 'فَعَلَ' format
    normalized_verb = f"{root_letters[0]}{fatha}{root_letters[1]}{fatha}{root_letters[2]}{fatha}"
    return normalized_verb


def check_hamza_position(verb):
    """
    Check if the Hamza (أَ) is in the first, middle, or last position of the root.
    Returns a corresponding rule.
    """
    # Normalize the verb
    normalized_verb = normalize_arabic_verb(verb)

    # Extract the root letters
    root_letters = re.findall(r"[\u0621-\u064A]", normalized_verb)  # Only letters

    # Define the specific Hamza with Fatha
    specific_hamza = "أ"

    # Check Hamza position
    if root_letters[0] == specific_hamza:
        return "مهموز الفاء"
    elif root_letters[1] == specific_hamza:
        return "مهموز العين"
    elif root_letters[2] == specific_hamza:
        return "مهموز اللام"
    else:
        return "لا تحتوي الكلمة على همزة من نوع أَ"


# Example usage
verbs = ['أَمَرَ', 'أَخَذَ', 'أَكَلَ', 'أَسَرَ', 'سَأَلَ', 'دَأَبَ', 'رَأَى', 'قَرَأَ', 'نَشَأَ', 'بَدَأَ', 'دَرَأَ']

for verb in verbs:
    try:
        # Get the result for Hamza position
        result = check_hamza_position(verb)
        
        # Reshape both the verb and the result for correct RTL display
        reshaped_verb = arabic_reshaper.reshape(verb)
        reshaped_result = arabic_reshaper.reshape(result)
        
        # Print the verb and result in the correct RTL order
        print(f"Verb: {get_display(reshaped_verb)} - Result: {get_display(reshaped_result)}")
    except ValueError as e:
        print(e)

