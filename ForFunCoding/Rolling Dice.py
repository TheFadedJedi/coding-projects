#Rolling Dice
import random
def main():
    option=topmenu()
    num_dice=ask_number_of_dice()
    while 1:
        roll_dice(option, num_dice)
        while 1:
            print("\nWhat would you like to do next?:")
            print("1: Roll again with the same dice")
            print("2: Change dice and amount")
            print("3: Exit")
            choice=input("Enter your choice:")
            if choice=='1':
                break
            elif choice=='2':
                option=topmenu()
                num_dice=ask_number_of_dice()
                break
            elif choice=='3':
                print("Thanks for playing!")
                return
            else:
                print("Invalid input. Please enter 1, 2, or 3")
#-------------------------------------------------------
def topmenu():
    option=0
    while 1:
        print("LETS ROLL SOME DICE!")
        print("What dice are you rolling?")
        print("1: D4")
        print("2: D6")
        print("3: D8")
        print("4: D10")
        print("5: D12")
        print("6: D20")
        print("7: D100")
        option=int(input("Type your option here:"))
        if (option>=1 and option<=7):
            break
        else:
            print("Invalid option, try again")
    return option
#-------------------------------------------------------
def ask_number_of_dice():
    while 1:
        num=input("How many dice do you want to roll?:")
        if num.isdigit() and int(num)>=1:
            return int(num)
        else:
            print("Invalid input. Please enter a number >= 1")
#-------------------------------------------------------
def roll_dice(option, count):
    dice_sides={1: 4, 2: 6, 3: 8, 4: 10, 5: 12, 6: 20, 7: 100}
    sides=dice_sides[option]
    rolls=[random.randint(1, sides) for _ in range(count)]
    print(f"You rolled {count} D{sides} dice and got: ")
    for i, roll in enumerate(rolls, 1):
        msg=""
        if sides==20:
            if roll==1:
                msg=" -Aww too bad"
            elif roll==20:
                msg=" -Hell yeah!"
        print(f" Dice {i}: {roll}{msg}")
    print(f"Total sum of rolls: {sum(rolls)}")
#-------------------------------------------------------
if __name__=='__main__':
    main()