import random as rnd

#*****************************************************************************
def ChooseingDifficulty():
    """
    Displays difficulty options to the user, prompts for a choice,
    and generates a random number based on the selected difficulty level.
    Returns the generated random number.
    Returns:
        int: The randomly generated number based on the chosen difficulty.
    """
    print("1- E or Easy (From 0 To 10)\n"
                + "2- M or Mediem (From 0 To 100)\n"
                + "3- H or Hard (From 0 To 1000)")
    Difficulty = input("Please Choose a Difficulty Level: ")
    if Difficulty in ['1', 'E', 'e', 'Easy', 'easy']:
        GuessingNumber = rnd.randint(0, 10)
    elif Difficulty in ['2', 'M', 'm', 'Medium', 'medium']:
        GuessingNumber = rnd.randint(0, 100)
    elif Difficulty in ['3', 'H', 'h', 'Hard', 'hard']:
        GuessingNumber = rnd.randint(0, 1000)
    else:
        print("Invalid difficulty level. Please try again.")
        ChooseingDifficulty()
        return
    return GuessingNumber

#*****************************************************************************
def GuessingCheck(GuessingNumber):
    """
    Docstring for GuessingCheck :param GuessingNumber: Description of GuessingNumber
    This function prompts the user to guess the number until they guess correctly.      
    It provides feedback on whether the guess is too low or too high and counts the number of attempts.
    Args:
        GuessingNumber (int): The number that the user is trying to guess.
    Returns:
        None, It just prints messages to the user.
    """
    count=0
    shouldContinue = True
    
    while shouldContinue:
        print("Please Enter Your Guess:")
        UserGuess = int(input())
        count += 1
        if UserGuess < GuessingNumber:
            print("Your Guess is too Low. Try Again:")
        elif UserGuess > GuessingNumber:
            print("Your Guess is too High. Try Again:")
        else:
            print(f"Congratulations! You've guessed the number {GuessingNumber} correctly in {count} attempts.")
            shouldContinue = False  

#*****************************************************************************
GuessingNumber = ChooseingDifficulty()
GuessingCheck(GuessingNumber)