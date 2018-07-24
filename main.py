from random import randrange, uniform, choice


# List of type prompts paired with the conversion functions for that type
possible_types_with_functions = [("integer", int), ("float", float), ("string", str), ("boolean", bool)]


def get_random_string():
    """Return a random string from a list"""
    possible_strings = ["'Jimmy cracked corn'", "'Arlo the aardvark'", "\"Cheese is yummy\"", "'$%$#%$'", "\"Art\"",
                        "'Time perplexes me.'", "\"Ice cream is also yummy\"",
                        "\"There's no escape from the Matrix DVD box set\"", "'Sometimes I just have to laugh.'",
                        "'$4.55'", "\"Argyle\"", "'Aaaaarrrrrgyle'", "'Elephants remember'", "\"Lists are fun\"",
                        "'Math is fun... sometimes'", "\"Break me off a piece of that Kit-Kat bar!\"", "'41 kg'",
                        "\"RED ALERT\"", "'Timmy the Tank says BOOM!'", "\"555.4555\""]
    return choice(possible_strings)


def name_the_type():
    """Asks the user to name the type of a certain literal. Returns 1 if correct, 0 if incorrect"""
    # Choose randomly from the list of possible types, ignoring the function part
    chosen_type, _ = possible_types_with_functions[randrange(len(possible_types_with_functions))]
    # Ask for the response from the user
    print("What type is this?")
    if chosen_type == "integer":
        value = randrange(-999999, 999999)
    elif chosen_type == "float":
        value = uniform(-999999.99999, 999999.99999)
    elif chosen_type == "string":
        value = get_random_string()
    elif chosen_type == "boolean":
        value = choice([True, False])
    else:
        value = 0
    response = input(str(value) + "\n")
    # Compare the response to the answer, ignoring case (uppercase or lowercase)
    if response.lower() == chosen_type.lower():
        # if they are the same, the response was correct
        print("Correct! Great job!")
        return 1
    else:
        # Otherwise the response was incorrect
        if chosen_type == "integer":
            indefinite_article = "an"
        else:
            indefinite_article = "a"
        print("Incorrect. That was %s %s." % (indefinite_article, chosen_type))
        return 0


def give_an_example():
    """Asks the user to give an example of a certain type. Returns 1 if correct, 0 if incorrect"""
    # Choose randomly from the list of possible types
    prompt, answer = possible_types_with_functions[randrange(len(possible_types_with_functions))]
    # Ask for the response from the user
    response = input("Please give me an example of a %s: " % prompt)
    try:
        # Try to do the conversion with the function
        # This will raise a ValueError if the conversion cannot be done
        answer(response)
        # Float is an exceptional case because numbers without decimals can be converted to floats
        # So need to make sure there is a decimal point in the response
        if answer == float:
            if "." not in response:
                print("Incorrect! Floats must include a decimal point.")
                return 0
        # Make sure strings are wrapped in single or double quotes
        elif answer == str:
            string_incorrect_message = "Incorrect! Please wrap strings in single or double quotes."
            if response[0] == "'":
                if response[-1] != "'":
                    print(string_incorrect_message)
                    return 0
            elif response[0] == "\"":
                if response[-1] != "\"":
                    print(string_incorrect_message)
                    return 0
            else:
                print(string_incorrect_message)
                return 0
        # Boolean is another exceptional case because many other types can be converted to booleans
        elif answer == bool:
            if response != "True" and response != "False":
                if response == "true" or response == "false":
                    print("Incorrect! Booleans in Python must be capitalized.")
                else:
                    print("Incorrect!")
                return 0
        # If no exception was raised, the response was correct
        print("Correct! Great work!")
        return 1
    except ValueError:
        # If an exception was raised, the response was incorrect
        print("Incorrect!")
        return 0


def choose_game():
    """Chooses randomly between name_the_type() and give_an_example()"""
    random_game = choice([name_the_type, give_an_example])
    return random_game()


def main():
    print("Welcome to the Python types game.")
    print("In this game you will either be given a type literal and asked to identify what type it is or")
    print("\tyou will be asked to provide an example of a certain type.")
    print("Let's begin...")
    score = 0
    while score < 10:
        print("\nCurrent score: %d" % score)
        score += choose_game()
    print("You win! Score: %d" % score)


if __name__ == "__main__":
    main()
