import pandas as pd
import random
from difflib import SequenceMatcher


file_path = r"C:\Users\OnatU\Downloads\Chem.csv"
data = pd.read_csv(file_path)


name_col = "Element_Name"
symbol_col = "Symbol"

def is_close(answer, correct, threshold=0.8):
    """Check if two strings are similar enough to count as correct."""
    ratio = SequenceMatcher(None, answer.lower().strip(), correct.lower().strip()).ratio()
    return ratio >= threshold

def run_quiz():
    print("Chemistry Quiz")
    print("Type 'exit' anytime to quit.\n")

    num_questions = int(input("How many questions would you like to answer? "))
    questions = data.sample(num_questions)
    
    score = 0
    results = []

    for _, row in questions.iterrows():
        ask_type = random.choice(["name_to_symbol", "symbol_to_name"])
        element = row[name_col]
        symbol = row[symbol_col]
        
        if ask_type == "name_to_symbol":
            answer = input(f"What is the symbol for {element}? ").strip()
            if answer.lower() == "exit":
                print("\nQuiz exited early.\n")
                break
            correct = symbol
        else:
            answer = input(f"What element has the symbol {symbol}? ").strip()
            if answer.lower() == "exit":
                print("\nQuiz exited early.\n")
                break
            correct = element

        if is_close(answer, correct):
            score += 1
            results.append((True, correct))
        else:
            results.append((False, correct))

    print("\nQuiz Complete!")
    print(f"Your final score: {score}/{len(results)}")

    
    show_answers = input("Would you like to see the correct answers? (y/n): ").lower().strip()
    if show_answers == "y":
        print("\nAnswers:")
        for i, (correct, value) in enumerate(results, 1):
            status = "✓" if correct else "✗"
            print(f"{i}. {value} ({'Correct' if correct else 'Incorrect'})")
    
    again = input("\nWould you like to play again? (y/n): ").lower().strip()
    if again == "y":
        print("\nRestarting...\n")
        run_quiz()
    else:
        print("\nThanks for playing!")


run_quiz()
