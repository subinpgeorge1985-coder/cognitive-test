import random
import string

# --------------------------------
# Utility Functions
# --------------------------------

def random_number():
    """
    Single number example:
    7, 3, 9
    """
    return str(random.randint(1, 99))


def random_number_pair():
    """
    Number pair example:
    12, 58, 91
    """
    return str(random.randint(10, 99))


def random_letter():
    """
    Single letter example:
    a, k, t
    """
    return random.choice(string.ascii_lowercase)


def random_letter_pair():
    """
    Letter pair example:
    ab, sg, ef
    """
    return (
        random.choice(string.ascii_lowercase) +
        random.choice(string.ascii_lowercase)
    )


def generate_repeating_question(generator_func, label):
    """
    Generic repeating question generator

    Example:
    Sequence:
    ab   sg   ef   sg   gg

    Question:
    Which one is repeating?
    """

    # Step 1: generate 4 unique values
    unique_items = []

    while len(unique_items) < 4:
        item = generator_func()
        if item not in unique_items:
            unique_items.append(item)

    # Step 2: choose one repeated item
    repeated_item = random.choice(unique_items)

    # Step 3: create visible sequence of 5
    # Example: ab sg ef sg gg
    sequence = unique_items.copy()
    sequence.remove(repeated_item)
    sequence.append(repeated_item)
    sequence.append(repeated_item)

    # keep exactly 5 visible values
    sequence = sequence[:5]

    random.shuffle(sequence)

    # Step 4: options must include repeated item
    options = unique_items.copy()
    random.shuffle(options)

    return {
        "question": f"Sequence: {'   '.join(sequence)}\n\nWhich {label} is repeating?",
        "options": options,
        "answer": chr(65 + options.index(repeated_item))
    }


# --------------------------------
# Specific Question Types
# --------------------------------

def generate_number_question():
    return generate_repeating_question(
        random_number,
        "number"
    )


def generate_number_pair_question():
    return generate_repeating_question(
        random_number_pair,
        "number pair"
    )


def generate_letter_question():
    return generate_repeating_question(
        random_letter,
        "letter"
    )


def generate_letter_pair_question():
    return generate_repeating_question(
        random_letter_pair,
        "letter pair"
    )


# --------------------------------
# MASTER GENERATOR
#
# 10 Number Questions
# 10 Number Pair Questions
# 10 Letter Questions
# 8 Letter Pair Questions
#
# TOTAL = 38 Questions
# --------------------------------

def generate_test():
    test = []

    # 10 number questions
    for _ in range(10):
        test.append(generate_number_question())

    # 10 number pair questions
    for _ in range(10):
        test.append(generate_number_pair_question())

    # 10 letter questions
    for _ in range(10):
        test.append(generate_letter_question())

    # 8 letter pair questions
    for _ in range(8):
        test.append(generate_letter_pair_question())

    # Shuffle final test
    random.shuffle(test)

    return test


# --------------------------------
# Print Test
# --------------------------------

def print_test(test):
    for i, q in enumerate(test, 1):
        print(f"\nQ{i}. {q['question']}")

        for idx, opt in enumerate(q["options"]):
            print(f"  {chr(65 + idx)}) {opt}")

        print(f"Correct Answer: {q['answer']}")


# --------------------------------
# Run
# --------------------------------

if __name__ == "__main__":
    test = generate_test()
    print_test(test)