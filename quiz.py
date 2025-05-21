#!/usr/bin/env python3
import json
import random
import argparse
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)

def load_quiz_data(file_paths):
    """Load quiz data from one or more JSON files."""
    all_quizzes = []
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                quiz_data = json.load(f)
                all_quizzes.append(quiz_data)
                print(f"Loaded quiz: {quiz_data.get('Questionnaire name', 'Unnamed Quiz')}")
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: {file_path} contains invalid JSON.{Style.RESET_ALL}")
            continue
        except FileNotFoundError:
            print(f"{Fore.RED}Error: {file_path} not found.{Style.RESET_ALL}")
            continue
    
    return all_quizzes

def display_welcome(quizzes):
    """Display welcome message and quiz options."""
    print(f"\n{Fore.CYAN}===== TERMINAL QUIZ GAME ====={Style.RESET_ALL}")
    
    if not quizzes:
        print(f"{Fore.RED}No valid quiz data loaded. Exiting.{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"\n{Fore.YELLOW}Available Quizzes:{Style.RESET_ALL}")
    for i, quiz in enumerate(quizzes, 1):
        name = quiz.get('Questionnaire name', f'Quiz {i}')
        question_count = len(quiz.get('Questions', []))
        print(f"{i}. {name} ({question_count} questions)")
    
    return quizzes

def select_quiz(quizzes):
    """Allow user to select which quiz to take."""
    while True:
        try:
            selection = input(f"\n{Fore.GREEN}Enter quiz number to start (or 'q' to quit): {Style.RESET_ALL}")
            
            if selection.lower() == 'q':
                print(f"{Fore.YELLOW}Thanks for playing!{Style.RESET_ALL}")
                sys.exit(0)
            
            index = int(selection) - 1
            if 0 <= index < len(quizzes):
                return quizzes[index]
            else:
                print(f"{Fore.RED}Invalid selection. Please enter a number between 1 and {len(quizzes)}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

def run_quiz(quiz_data):
    """Run the selected quiz."""
    quiz_name = quiz_data.get('Questionnaire name', 'Unnamed Quiz')
    questions = quiz_data.get('Questions', [])
    
    if not questions:
        print(f"{Fore.RED}This quiz has no questions!{Style.RESET_ALL}")
        return 0, 0
    
    # Randomize the order of questions
    random.shuffle(questions)
    
    print(f"\n{Fore.CYAN}=== Starting Quiz: {quiz_name} ==={Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total questions: {len(questions)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Answer by typing the letter (a, b, c, d) and pressing Enter.{Style.RESET_ALL}")
    input(f"{Fore.GREEN}Press Enter to start...{Style.RESET_ALL}")
    
    score = 0
    total_questions = len(questions)
    
    for i, question_data in enumerate(questions, 1):
        question = question_data.get('Question', f'Question {i}')
        answers = question_data.get('Answers', {})
        correct_answer = question_data.get('Correct Answer', '').lower()
        
        # Clear some space between questions
        print("\n" + "-" * 60)
        print(f"{Fore.CYAN}Question {i}/{total_questions}:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{question}{Style.RESET_ALL}")
        
        # Display answer choices
        for key, value in answers.items():
            print(f"{Fore.YELLOW}{key}) {Style.RESET_ALL}{value}")
        
        # Get user answer
        while True:
            user_answer = input(f"\n{Fore.GREEN}Your answer: {Style.RESET_ALL}").lower()
            if user_answer in ['a', 'b', 'c', 'd']:
                break
            print(f"{Fore.RED}Invalid input. Please enter a, b, c, or d.{Style.RESET_ALL}")
        
        # Check answer
        if user_answer == correct_answer:
            score += 1
            print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
        else:
            correct_text = answers.get(correct_answer, "Unknown")
            print(f"{Fore.RED}Incorrect. The correct answer is {correct_answer}) {correct_text}{Style.RESET_ALL}")
        
    return score, total_questions

def display_results(score, total_questions):
    """Display the final quiz results."""
    if total_questions == 0:
        return
    
    percentage = (score / total_questions) * 100
    
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}===== QUIZ RESULTS ====={Style.RESET_ALL}")
    print(f"You scored: {Fore.GREEN}{score}/{total_questions} ({percentage:.1f}%){Style.RESET_ALL}")
    
    # Generate a performance message
    if percentage >= 90:
        message = f"{Fore.GREEN}Excellent! You're a quiz master!{Style.RESET_ALL}"
    elif percentage >= 70:
        message = f"{Fore.YELLOW}Good job! You know your stuff!{Style.RESET_ALL}"
    elif percentage >= 50:
        message = f"{Fore.YELLOW}Not bad, but there's room for improvement.{Style.RESET_ALL}"
    else:
        message = f"{Fore.RED}You might want to study more and try again.{Style.RESET_ALL}"
    
    print(message)

def main():
    parser = argparse.ArgumentParser(description='Terminal Quiz Game')
    parser.add_argument('quiz_files', nargs='+', help='Path to one or more JSON quiz files')
    args = parser.parse_args()
    
    print(f"{Fore.CYAN}Loading quiz data...{Style.RESET_ALL}")
    quizzes = load_quiz_data(args.quiz_files)
    
    play_again = True
    while play_again:
        quizzes = display_welcome(quizzes)
        selected_quiz = select_quiz(quizzes)
        score, total = run_quiz(selected_quiz)
        display_results(score, total)
        
        replay = input(f"\n{Fore.YELLOW}Would you like to play another quiz? (y/n): {Style.RESET_ALL}").lower()
        play_again = replay.startswith('y')
    
    print(f"\n{Fore.CYAN}Thanks for playing Terminal Quiz Game!{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Quiz game terminated by user. Goodbye!{Style.RESET_ALL}")
        sys.exit(0)