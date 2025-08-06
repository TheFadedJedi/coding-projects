#Chapter 3 Examples
#1
num=5
if num>0:
    print("The number is positive")
#2
num=-2
if num>0:
    print("The number is positive")
else:
    print("The number is negative")
#3
str1="Hello"
str2="World"
if str1==str2:
    print("The strings are equal")
else:
    print("The strings are not equal")
#4
score=80
if score>=90:
    print("Grade A")
elif score>=80:
    print("Grade B")
elif score>=70:
    print("Grade C")
elif score>=60:
    print("Grade D")
else:
    print("Grade F")
#5
num=25
if num>0 and num<50:
    print("The number is in the range(0,50).")
else:
    print("The number is outside the range (0,50).")
#6
is_logged_in=False
if is_logged_in:
    print("Welcome to the member's area>")
else:
    print("Please log in to access the member's area.")