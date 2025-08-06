#Temperature/Distance/Speed/Weight Converter
def main():
    while True:
        option=topmenu()
        if option==1:
            temperature_conversion()
        elif option==2:
            distance_conversion()
        elif option==3:
            speed_conversion()
        elif option==4:
            weight_conversion()
        elif option==5:
            print("Thanks for using the converter!")
            return
        else:
            print("Invalid input. Please enter 1, 2, 3, or 4")
#-------------------------------------------------------
def topmenu():
    while True:
        print("\nWELCOME TO THE CONVERTER!")
        print("What would you like to do?")
        print("1: Convert Temperature")
        print("2: Convert Distance")
        print("3: Convert Speed")
        print("4: Convert Weight")
        print("5: Exit")
        option=input("Type your option here:")
        if option in ['1', '2', '3', '4', '5']:
            return int(option)
        else:
            print("Invalid option, try again")
#-------------------------------------------------------
def temperature_conversion():
    while True:
        temp=input("Enter the temperature to convert (e.g., 32F or 100C): ")
        if temp[-1].upper()=='F':
            celsius=(float(temp[:-1])-32)*5/9
            print(f"{temp} is equal to {celsius:.2f}C")
        elif temp[-1].upper()=='C':
            fahrenheit=(float(temp[:-1])*9/5)+32
            print(f"{temp} is equal to {fahrenheit:.2f}F")
        else:
            print("Invalid input. Please enter a temperature ending with 'F' or 'C'.")
            continue
        if not ask_continue():
            break
#-------------------------------------------------------
def distance_conversion():
    while True:
        distance=input("Enter the distance to convert (e.g., 10mi or 16km): ")
        if distance[-2:].lower()=='mi':
            kilometers=float(distance[:-2])*1.60934
            print(f"{distance} is equal to {kilometers:.2f}km")
        elif distance[-2:].lower()=='km':
            miles=float(distance[:-2])/1.60934
            print(f"{distance} is equal to {miles:.2f}mi")
        else:
            print("Invalid input. Please enter a distance ending with 'mi' or 'km'.")
            continue
        if not ask_continue():
            break
#-------------------------------------------------------
def speed_conversion():
    while True:
        speed=input("Enter the speed to convert (e.g., 60mph or 100km/h): ")
        if speed[-3:].lower()=='mph':
            kilometers_per_hour=float(speed[:-3])*1.60934
            print(f"{speed} is equal to {kilometers_per_hour:.2f}km/h")
        elif speed[-4:].lower()=='km/h':
            miles_per_hour=float(speed[:-4])/1.60934
            print(f"{speed} is equal to {miles_per_hour:.2f}mph")
        else:
            print("Invalid input. Please enter a speed ending with 'mph' or 'km/h'.")
            continue
        if not ask_continue():
            break
#-------------------------------------------------------
def weight_conversion():
    while True:
        weight=input("Enter the weight to convert (e.g., 150lbs or 70kg): ")
        if weight[-3:].lower()=='lbs':
            kilograms=float(weight[:-3])*0.453592
            print(f"{weight} is equal to {kilograms:.2f}kg")
        elif weight[-2:].lower()=='kg':
            pounds=float(weight[:-2])/0.453592
            print(f"{weight} is equal to {pounds:.2f}lbs")
        else:
            print("Invalid input. Please enter a weight ending with 'lbs' or 'kg'.")
            continue
        if not ask_continue():
            break
#-------------------------------------------------------
def ask_continue():
    while True:
        choice=input("Would you like to convert another value? (y/n): ")
        if choice.lower() in ['y', 'n']:
            return choice.lower()=='y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
#-------------------------------------------------------
if __name__=='__main__':
    main()