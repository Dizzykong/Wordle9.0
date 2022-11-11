import pickle

from numpy import save

def save_object(obj, filename):
    try:
        with open(filename, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported): ", ex)

def load_object(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupportod):", ex)

def wordle_feedback(guess, solution):
    feedback = []
    taken = []
    for gv, sv in zip(guess, solution):
        if gv is sv:
            feedback.append("G")
            taken.append("T")
        else:
            feedback.append("?")
            taken.append("?")
    for i in range(5):
        for j in range(5):
            if guess[i] is solution[j] and i != j and taken[j] != "T" and feedback[i] == "?":
                feedback[i] = "Y"
                taken[j] = "T"
    for i in range(len(feedback)):
        if feedback[i] == "?" or feedback[i] == "C":
            feedback[i] = "B"
    return feedback

def next_guess(curr_solutions, guesses, feedbacks):
        avg_guesses = []
        for guess in guesses:
            num = avg_guess(guess, curr_solutions, feedbacks)
            avg_guesses.append(num)
        for solution in curr_solutions:
            index = guesses.index(solution)
            avg_guesses[index] *= (len(curr_solutions) - 1) / len(curr_solutions)
        best_word = guesses[avg_guesses.index(min(avg_guesses))]
        return best_word

def avg_guess(guess, curr_solutions, feedbacks):
    num_left = []
    for feedback in feedbacks:
        count = 0
        for solution in curr_solutions:
            if wordle_feedback(guess, solution) == feedback:
                count += 1
        num_left.append(count)
    avg = 0
    summation = sum(num_left)
    for num in num_left:
        avg += (num / summation) * num
    return avg

def filter_solutions(guess, tempFeedback, curr_solutions):
    solutions_left = []
    for solution in curr_solutions:
        if wordle_feedback(guess, solution) == tempFeedback:
            solutions_left.append(solution)
    return solutions_left

def grab_guess(guess, list):
    guess_as_list = [letter for letter in guess]
    index = [i for i, v in enumerate(list) if v[0] == guess_as_list][0]
    return list[index][1]

def run_game():
    currGuess = "roate"
    feedbacks = load_object("feedbacks.pkl")
    guesses = load_object("guesses.pkl")
    solutions = load_object("solutions.pkl")
    second_guess = load_object(f"second_guess_{currGuess}.pkl")
    second_guess[125] = (['B', 'B', 'B', 'B', 'B'], 'slimy')
    for i in range(5):
        if i == 1:
            currGuess = grab_guess(currFeedback, second_guess)
        elif i > 1:
            currGuess = next_guess(solutions, guesses, feedbacks)
        if currGuess == "ERROR":
            print("Invalid input. Quitting program.")
            break
        currFeedback = input(
            f"Guess {currGuess} then type in Wordle's output.\n"
            f"B for blank, Y for yellow, and G for green like so: \"GGYBB\"" + "\n")
        tempFeedback = []
        for char in currFeedback:
            tempFeedback.append(char)
        if all(char == "G" for char in tempFeedback):
            break
        solutions = filter_solutions(currGuess, tempFeedback, solutions)
    print("You Won!")

def valid_feedbacks(guess, feedbacks, solutions):
    list = []
    for feedback in feedbacks:
        for solution in solutions:
            if wordle_feedback(guess, solution) == feedback:
                list.append(feedback)
                break
    return list

def main():
    second_guess_roate = load_object("second_guess_roate.pkl")
    run_game()
    # list = []
    # guess = "roate"
    # feedbacks = load_object("feedbacks.pkl")
    # guesses = load_object("guesses.pkl")
    # solutions = load_object("solutions.pkl")
    # feedbacks = valid_feedbacks(guess, feedbacks, solutions)
    print("test")

if __name__ == "__main__":
    main()