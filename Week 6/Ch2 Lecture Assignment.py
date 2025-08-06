# This program calculates the area of a rectangle
# Input
length = float(input("Enter the length: ")) # Prompt user for length
width = float(input("Enter the width: ")) # Prompt user for width
# Processing
area = length * width # Calculate the area
# Output
print("The area of the rectangle is:", area) # Display the result
#----------------------------------------------------------------------
name = input("Enter your name: ") # Prompt user for name
age = int(input("Enter your age: ")) # Prompt user for age
# Processing
year_of_birth = 2023 - age # Calculate the year of birth
# Output
print("Hello", name, "you were born in", year_of_birth) # Display personalized message
#----------------------------------------------------------------------
# Displaying a simple message
print("Hello, world!")
# Displaying multiple values
name = "John"
age = 25
print("Name:", name, "Age:", age)
# Displaying numerical calculations
result = 5 + 7
print("The result is:", result)
#----------------------------------------------------------------------
# This is a single-line comment
"""
This is a multi-line comment.
It can span multiple lines.
"""
# Example usage of comments in code
# Calculate the sum of two numbers
num1 = 10 # First number
num2 = 5 # Second number
sum = num1 + num2 # Add the numbers
print("The sum is:", sum) # Display the result
#--------------------------------------------------------------------
# Assigning values to variables
name = "Alice"
age = 30
pi = 3.14
# Updating variable values
count = 5
count = count + 1 # Increment count by 1
# Variable reassignment
x = 10
x = 20 # x is now reassigned to a new value
# Using variables in calculations
length = 5
width = 3
area = length * width # Calculate the area using variables
print("The area is:", area) # Display the result
#---------------------------------------------------------------------
# Reading a single input
name = input("Enter your name: ") # Prompt user for name
# Reading multiple inputs
num1 = int(input("Enter the first number: ")) # Prompt user for first number
num2 = int(input("Enter the second number: ")) # Prompt user for second number
# Using keyboard input in calculations
sum = num1 + num2 # Add the numbers
print("The sum is:", sum) # Display the result
#-----------------------------------------------------------------------
# Addition
num1 = 5
num2 = 3
result = num1 + num2
print("The result of addition is:", result)
# Subtraction
num1 = 10
num2 = 7
result = num1 - num2
print("The result of subtraction is:", result)
# Multiplication
num1 = 4
num2 = 6
result = num1 * num2
print("The result of multiplication is:", result)
# Division
num1 = 10
num2 = 2
result = num1 / num2
print("The result of division is:", result)
#--------------------------------------------------------------------
# Concatenating strings
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print("Full name:", full_name)
# Combining strings and numbers
age = 30
message = "I am " + str(age) + " years old."
print(message)
#-----------------------------------------------------------
# Formatting output using placeholders
name = "Alice"
age = 25
print("Name: %s, Age: %d" % (name, age))
# Formatting output using f-strings (Python 3.6+)
name = "Bob"
age = 30
print(f"Name: {name}, Age: {age}")
# Formatting floating-point numbers
pi = 3.141592653589793
print(f"Value of pi: {pi:.2f}") # Display pi with 2 decimal places
#------------------------------------------------------------------
# Using named constants for conversion
METERS_TO_FEET = 3.28084
distance_in_meters = 100
distance_in_feet = distance_in_meters * METERS_TO_FEET
print("Distance in feet:", distance_in_feet)
# Using named constants for fixed values
TAX_RATE = 0.2
income = 5000
tax_amount = income * TAX_RATE
print("Tax amount:", tax_amount)