import re
import emoji
from unidecode import unidecode

def remove_accents(input_string):
    # Remplace les caractères avec accent par leurs équivalents sans accent
    return unidecode(input_string)

def clean_string(input_string):
    input_string = remove_accents(input_string)
    # Supprimer les espaces, les barres obliques et les caractères non acceptés (sauf les emojis)
    cleaned_string = re.sub(r'\s+|/', '_', input_string)
    cleaned_string = emoji.demojize(cleaned_string)
    cleaned_string = re.sub(r'\s+|/|[^a-zA-Z0-9_-]', '_', cleaned_string)
    return cleaned_string
