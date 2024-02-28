import difflib
import re

'''while double_space == True:
    if context.find("  ") != -1:
        if context.find("  ") != -1 and context.find("  ") < offsetStart:
            offsetStart -= 1
            context = context.replace('  ', ' ', 1)
        if context.find("  ") > offsetStart:
            context = context.replace('  ', ' ', 1)
    else:
        double_space = False
offsetStart_full_str = p_string.find(context) + offsetStart'''

def find_occurrences(word, text):
    occurrences = []
    word_lower = word.lower()
    text_lower = text.lower()
    # Remove punctuation from text
    text_without_punctuation = re.sub(r"[';:,.!?]", ' ', text_lower)
    #print(text,'\n')
    #print(text_without_punctuation)
    index = -1
    while True:
        index = text_without_punctuation.find(word_lower, index + 1)
        if index == -1:
            break
        occurrences.append(index)
    return occurrences

def contains_special_characters(text):
    for char in text:
        if ord(char) < 32 or ord(char) > 126:
            return True  # Special character found
    return False


def find_closest_number(number, number_list):
    closest = None
    min_difference = float('inf')  # Initialize with infinity

    for num in number_list:
        difference = abs(number - num)
        if difference < min_difference:
            min_difference = difference
            closest = num

    return closest

def longest_common_substrings(full_string, sub_string):
    matches = []
    max_length = 0
    less_word = len(sub_string)
    founded = False
    while not founded:
        if full_string.find(sub_string[:less_word]) != -1:
            return full_string.find(sub_string[:less_word])
        else:
            founded = False
            less_word -= 1
def dif_string_checker(str1, str2):
    modification = 0
    list_modification = []
    for i, s in enumerate(difflib.ndiff(str1, str2)):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            if s[-1] == ' ':
                pass
            else:
                modification += 1
                print(u'Delete "{}" from position {}'.format(s[-1], i))
        elif s[0] == '+':
            modification += 1
            print(u'Add "{}" to position {}'.format(s[-1], i))
    if modification > 1:
        print(str1)
        print(str2)
