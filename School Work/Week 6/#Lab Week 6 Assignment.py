#Lab Week 6 Assignment
#Question 2
total_sales=float(input("Enter yearly sales report:"))
total_profit=(total_sales*.23)
print("Companies total profit is:","$",total_profit)
#Question 3
sqrft=int(input("Enter total square feet here:"))
total_acres=(sqrft/43560)
print("There are",total_acres,"total acres")
#Question 5
speed=70
distance1=(speed*6)
distance2=(speed*10)
distance3=(speed*15)
print("The distance traveled in 6 hours is:",distance1,"miles")
print("The distance traveled in 10 hours is:",distance2,"miles")
print("The distance traveled in 15 hours is:",distance3,"miles")
#Question 12
num=0
value=0
def main():
    money_on_hand=0
    money_to_buy=0
    print("----------Main----------")
    while True:
        menu()
        op=input("Type your option here: ")
        match op:
            case 'a':
                print("sell---")
                inputn()
                sold_value=(num*value)
                stockbroker_fee=(sold_value*.03)
                money_on_hand=(sold_value-stockbroker_fee)
                print("Joe sold the stock for ",sold_value)
                print("Joe paid a commision fee of", stockbroker_fee)
            case 'b':
                print("buy---")
                inputn()
                bought_value=(num*value)
                stockbroker_fee=(bought_value*.03)
                money_to_buy=(bought_value+stockbroker_fee)
                print("Joe paid ",money_to_buy)
                print("Joe paid a commision fee of ", stockbroker_fee)
            case _:
                print("Thank you for trading with us!")
                break
        profit=(money_on_hand-money_to_buy)
        if (profit>0):
            print("Joe made a profit of ",profit)
        else:
            print("Joe lost this money in the transaction ",profit)
        print("End of main----")
def menu():
    print("----------Menu----------")
    print('a) Selling stocks')
    print('b) Buying stocks')
    print("Enter any other option to stop trading.")
def inputn():
    global num,value
    num=int(input("Enter volume of stock traded:"))
    value=float(input("Enter stock price here:"))
main()