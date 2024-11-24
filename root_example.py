import re

def normalize_arabic_verb(verb):
    """
    Normalize an Arabic verb to conform to the format 'فَعَلَ'.
    Adds missing diacritics if needed.
    """
    # Define valid diacritics
    fatha = "\u064E"  # َ

    # Strip spaces and ensure the verb has three root letters
    verb = verb.strip()
    root_letters = re.findall(r"[\u0621-\u064A]", verb)
    
    if len(root_letters) != 3:
        raise ValueError(f"The verb '{verb}' does not have exactly 3 root letters.")

    # Add missing fatha diacritics to conform to 'فَعَلَ' format
    normalized_verb = f"{root_letters[0]}{fatha}{root_letters[1]}{fatha}{root_letters[2]}{fatha}"
    return normalized_verb


def check_hamza_position(verb):
    """
    Check if the hamza (ء) is in the first, middle, or last position of the root.
    Returns a corresponding rule.
    """
    # Normalize the verb
    normalized_verb = normalize_arabic_verb(verb)
    
    # Extract the root letters
    root_letters = re.findall(r"[\u0621-\u064A]", normalized_verb)
    
    # Check hamza position
    if root_letters[0] == "ء":
        return f"إذا كانت الهمزة في أول الجذر فهو فعل مهموز الفاء: {normalized_verb}"
    elif root_letters[1] == "ء":
        return f"إذا كانت الهمزة في وسط الجذر فهو فعل مهموز العين: {normalized_verb}"
    elif root_letters[2] == "ء":
        return f"إذا كانت الهمزة في ٱخر الجذر فهو فعل مهموز اللام: {normalized_verb}"
    else:
        return "لا تحتوي الكلمة على همزة في الجذر"

# Example usage
verbs = ["أكل", "سأل", "درأ", "كتب", "ءمل"]
for verb in verbs:
    try:
        print(check_hamza_position(verb))
    except ValueError as e:
        print(e)
