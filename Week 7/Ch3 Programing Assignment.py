#Chapter 3 Programing Assignment
#1 Day of the week
num=int(input("Please enter a number 1-7:"))
if num==1:
    print("That is Monday")
elif num==2:
    print("That is Tuesday")
elif num==3:
    print("That is Wednesday")
elif num==4:
    print("That is Thursday")
elif num==5:
    print("That is Friday")
elif num==6:
    print("That is Saturday")
elif num==7:
    print("That is Sunday")
else:
    print("That is not a valid number")
#4 Roman Numerals
num=int(input("Please enter a number 1-10:"))
if num==1:
    print("That looks like I.")
elif num==2:
    print("That looks like II.")
elif num==3:
    print("That looks like III.")
elif num==4:
    print("That looks like IV.")
elif num==5:
    print("That looks like V.")
elif num==6:
    print("That looks like VI.")
elif num==7:
    print("That looks like VII.")
elif num==8:
    print("That looks like VIII.")
elif num==9:
    print("That looks like IX.")
elif num==10:
    print("That looks like X.")
else:
    print("That is not a valid input")
#10 Money Counting Game
quarter=0.25
dime=0.10
nickel=0.05
penny=0.01
def game():
    total=0.00
    goal=1.00
    print("------Game Start------")
    print("Make a dollar by adding coins together.")
    while True:
        menu()
        op=input("Please make a selection:")
        match op:
            case 'a':
                print("Quarters----")
                inputn()
                total+=round(num*quarter,2)
            case 'b':
                print("Dimes----")
                inputn()
                total+=round(num*dime,2)
            case 'c':
                print("Nickels----")
                inputn()
                total+=round(num*nickel,2)
            case 'd':
                print("Pennies----")
                inputn()
                total+=round(num*penny,2)
            case _:
                break
    print("You added up to ",total)
    if total==goal:
        print("Congradulations! You've beat the game.")
    elif total>goal:
        print("Sorry, that isn't correct. Looks like you were", (total-goal), "over. Good luck next time!")
    else:
        print("Sorry, that isn't correct. Looks like you were", (goal-total), "short. Good luck next time!")
def menu():
    print("-----Menu-----")
    print('a) Add Quarters?')
    print('b) Add Dimes?')
    print('c) Add Nickles?')
    print('d) Add Pennies?')
    print('Any other option to end.')
def inputn():
    global num
    num=int(input("Enter number of coins to add:"))
game()