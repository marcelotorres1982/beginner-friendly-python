from datetime import datetime

# User's input data
year_of_birth = int(input("Enter your year of birth: "))
name = input("Enter your name: ")
sex = input("Enter your sex: [M/F] ").upper()
#Calculating age
age = datetime.now().year - year_of_birth

# Set retirement age based on sex
if sex == 'F':
    retirement_age = 62

else:
    retirement_age = 65

# Calculate years left until retirement
years_left = retirement_age - age
if years_left <=0:
    years_left = 0
    retirement_message = 'You are already retired.'
else:
    retirement_message = f'You have {years_left} years left until retirement.'

# Display results
print("\n--- Results ---")
print(f"Name: {name}")
print(f"Sex: {sex}")
print(f"Age: {age}")
print(retirement_message)