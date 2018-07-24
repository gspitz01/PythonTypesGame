from random import randrange, uniform, choice
import sys
import datetime


# List of type prompts paired with the conversion functions for that type
possible_types_with_functions = [("integer", int), ("float", float), ("string", str), ("boolean", bool)]
# File name of the high scores file
high_scores_file_name = "high_scores.txt"


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


def made_high_scores(score):
    """Asks the user to write their name for the high score, returns a tuple for the record"""
    print("You made it onto the high scores!")
    user_name = input("Please enter your name: ")
    return score, user_name, datetime.date.today()


def enter_score_into_high_scores(high_scores, score):
    """Writes a high score into the high score file"""
    with open(high_scores_file_name, "w") as high_scores_file:
        high_scores.append(made_high_scores(score))
        high_scores.sort(key=lambda high_score: high_score[0], reverse=True)
        for high_score_tuple in high_scores:
            high_scores_file.write("%d %s %s\n" % (high_score_tuple[0], high_score_tuple[1], high_score_tuple[2]))


def check_score(score):
    """Checks to see if a score belongs in the high scores list"""
    # If score isn't more than 0, don't bother recording it
    if score <= 0:
        return
    made_list = False
    high_scores = []
    # Open the high score file
    with open(high_scores_file_name, "r") as high_scores_file:
        # Read the lines
        high_score_lines = high_scores_file.readlines()
        for line in high_score_lines:
            record_parts = line.split(' ')
            # Put the lines into a list of tuples, making sure to strip off whitespace
            high_scores.append((int(record_parts[0].strip()), record_parts[1].strip(), record_parts[2].strip()))
    # Only keep 5 scores, if there are fewer, automatically made it
    if len(high_scores) < 5:
        enter_score_into_high_scores(high_scores, score)
        made_list = True
    else:
        # If there are 5 scores, need to be greater than the lowest
        high_scores.sort(key=lambda high_score: high_score[0])
        if score > high_scores[0][0]:
            enter_score_into_high_scores(high_scores, score)
            made_list = True
    if made_list:
        display_high_scores()


def play_game():
    """Plays the game until user gets one wrong"""
    print("Let's begin...")
    score = 0
    correct = 1
    while correct:
        print("\nCurrent score: %d" % score)
        correct = choose_game()
        score += correct
    print("Good work. You scored %d" % score)
    # Check high scores to see if this run made it
    check_score(score)


def display_high_scores():
    """Displays the high scores from the high score txt file"""
    print("\n%s High Scores %s" % ("-" * 20, "-" * 20))
    with open(high_scores_file_name, "r") as high_score_file:
        print(high_score_file.read())


def exit_game():
    """Exits the game"""
    sys.exit(0)


def display_menu():
    menu_options = [("Play the game", play_game), ("View High Scores", display_high_scores), ("Exit", exit_game)]
    print("")
    for index, menu_option in enumerate(menu_options):
        print("%d) %s" % ((index + 1), menu_option[0]))
    menu_choice = input("What would you like to do? ")
    try:
        menu_choice_function = menu_options[int(menu_choice) - 1][1]
        return menu_choice_function
    except (ValueError, IndexError):
        print("Menu choice must be an integer of one of the choices")
        return None


def main():
    print("Welcome to the Python types game.")
    print("In this game you will either be given a type literal and asked to identify what type it is or")
    print("\tyou will be asked to provide an example of a certain type.")
    while True:
        menu_choice_function = display_menu()
        if menu_choice_function is not None:
            menu_choice_function()


if __name__ == "__main__":
    main()
