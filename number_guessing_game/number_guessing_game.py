from random import randint

# Generate a random number between 1 and 100
number_to_guess = randint(1, 100)

# Initialize attempts
attempts = 0
chances = 5 # Maximum number of attempts

print("Welcome to the Number Guessing Game!")
print(f"You have {chances} chances to guess the number between 1 and 100.")

# Main game loop
while attempts < chances:
    try:
        guess = int(input("Enter your guess: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    attempts += 1

    if guess < number_to_guess:
        print("Too low!")
    elif guess > number_to_guess:
        print("Too high!")
    else:
        print("Congratulations! You've guessed the number!")
        break
else:
    print(f'Game over! The number was {number_to_guess}.')