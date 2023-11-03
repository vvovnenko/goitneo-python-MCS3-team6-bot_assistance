import re


def sanitize_args(func):
    def wrapper(arg1, arg2):
        arg1 = sanitize_args(arg1)
        arg2 = sanitize_args(arg2)
        return func(arg1, arg2)

    return wrapper


@sanitize_args
def get_similarity_score(input: str, guess: str):
    score = 0

    if guess.startswith(input) or input.startswith(guess):
        score += 5
    elif count_similar_characters(input, guess) >= max(len(input), len(guess)) - 1:
        score += 5

    if score == 0 and (len(input) < len(guess) / 3):
        return score

    if is_anagram(input, guess):
        score += 3

    if are_substrings(input, guess):
        score += 1

    return score


def is_anagram(str1, str2):
    return sorted(str1) == sorted(str2)


def are_substrings(str1, str2):
    return str1 in str2 or str2 in str1


def count_similar_characters(str1, str2):
    count = 0

    for char1 in str2:
        if char1 in str1:
            count += 1
            str1.replace(char1, '', 1)

    return count


def sanitize_args(input_string):
    return re.sub(r'[^a-zA-Z]', '', input_string)
