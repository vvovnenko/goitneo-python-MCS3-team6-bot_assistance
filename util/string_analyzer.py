def get_similarity_score(input: str, guess: str):
    score = 0

    if guess.startswith(input):
        score += 5

    if score == 0 and (len(input) < len(guess)/3):
        return score

    if is_anagram(input, guess):
        score += 3

    if (are_substrings(input, guess)):
        score += 1

    len_diff = abs(len(input) - len(guess))

    # additional score for less diff in length
    if score > 0:
        if len_diff <= 3:
            score += 4 - len_diff

    return score


def is_anagram(str1, str2):
    return sorted(str1) == sorted(str2)


def are_substrings(str1, str2):
    return str1 in str2 or str2 in str1
