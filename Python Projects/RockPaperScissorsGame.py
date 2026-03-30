import random as rnd
#*****************************************************************************
def PlayerChoice():
    """
    Prompts the user to choose between Rock, Paper, or Scissors.
    Returns the user's choice as a string.
    Returns:
        str: The user's choice of 'Rock', 'Paper', or 'Scissors'.
    """
    print("Please Choose: \n1- R or Rock\n2- P or Paper\n3- S or Scissors")
    choice = input("Your Choice: ")
    if choice in ['1', 'R', 'r', 'Rock', 'rock']:
        return 'Rock'
    elif choice in ['2', 'P', 'p', 'Paper', 'paper']:
        return 'Paper'
    elif choice in ['3', 'S', 's', 'Scissors', 'scissors']:
        return 'Scissors'
    else:
        print("Invalid choice. Please try again.")
        return PlayerChoice()
#*****************************************************************************
def ComputerChoice():
    """
    Generates a random choice for the computer between Rock, Paper, and Scissors.
    Returns the computer's choice as a string.
    Returns:
        str: The computer's choice of 'Rock', 'Paper', or 'Scissors'.
    """
    options = ['Rock', 'Paper', 'Scissors']
    choices=rnd.choice(options)
    return choices
#*****************************************************************************
def DetermineWinner(player, computer):
    """
    Determines the winner of the Rock-Paper-Scissors game based on the player's and computer's choices.
    Args:
        player (str): The player's choice of 'Rock', 'Paper', or 'Scissors'.
        computer (str): The computer's choice of 'Rock', 'Paper', or 'Scissors'.
    Returns:
        str: The result of the game ('Player', 'Computer', or 'Tie').
    """
    if player == computer:
        return 'Tie'
    elif (player == 'Rock' and computer == 'Scissors') or \
         (player == 'Paper' and computer == 'Rock') or \
         (player == 'Scissors' and computer == 'Paper'):
        return 'Player'
    else:
        return 'Computer'   
#*****************************************************************************
player_choice = PlayerChoice()
computer_choice = ComputerChoice()
print(f"Computer chose: {computer_choice}")
result = DetermineWinner(player_choice, computer_choice)
if result == 'Tie':
    print("It's a tie!")
elif result == 'Player':
    print("Congratulations! You win!")
else:
    print("Computer wins! Better luck next time.")
