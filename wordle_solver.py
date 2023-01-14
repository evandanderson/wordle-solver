import json
from collections import defaultdict
from operator import countOf
from time import perf_counter


def get_letter_distribution(words: list) -> dict:
    letter_counts = defaultdict(int)

    for word in words:
        for letter in word:
            letter_counts[letter] += 1

    return dict(sorted(letter_counts.items(), key=lambda item: item[1], reverse=True))


def find_best_guess(words: list) -> str:
    letters = get_letter_distribution(words)
    words_copy = words.copy()

    for letter in letters:
        solutions = [word for word in words_copy if letter in word]
        if len(solutions) == 1:
            return solutions[0]
        elif len(solutions) > 1:
            words_copy = solutions

    return " or ".join(words_copy)


def find_possible_solutions(words: list, guess: str, greens: dict, yellows: dict, limits: dict) -> list:
    solutions = []
    included_letters = list(greens.values()) + list(yellows.values())

    for word in words:
        if (len(word) == len(guess) and
            not any(letter not in word for letter in included_letters) and
            not any(word.count(letter) > limit for letter, limit in limits.items()) and
            not any(word[i] != guess[i] for i in greens) and
            not any(word[i] == guess[i] for i in yellows)):
                solutions.append(word)

    return solutions


def get_limits(greens: dict, yellows: dict, greys: dict) -> dict:
    limits = {}

    for letter in greys.values():
        if letter not in limits:
            limits[letter] = (countOf(greens.values(), letter) + countOf(yellows.values(), letter))

    return limits


def main():
    with open('words.json', 'r') as file:
        words = json.loads(file.read())

    limits = {}

    while len(words) > 1:
        guess = input("Guess: ").lower().strip()
        greens = {int(index) - 1: guess[int(index) - 1]
            for index in input("Greens: ").split()}
        yellows = {int(index) - 1: guess[int(index) - 1]
            for index in input("Yellows: ").split()}
        greys = {int(index): letter for index, letter in enumerate(
            guess) if index not in greens and index not in yellows}
        limits = limits | get_limits(greens, yellows, greys)

        time = perf_counter()
        solutions = find_possible_solutions(words, guess, greens, yellows, limits)
        execution_time = round((perf_counter() - time)*1000, 2)

        print(f"Found {len(solutions)} solution{'s' if len(solutions) != 1 else ''} in {execution_time} ms")
        print(f"Possible solution{'s' if len(solutions) != 1 else ''}: {', '.join(solutions)}")

        if len(solutions) > 1:
            print(f"Best guess: {find_best_guess(solutions)}")

        words = solutions


if __name__ == "__main__":
    main()
