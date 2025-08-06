#Defining top menu
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
def main():
    op=topmenu()
    print("Value returned from topmenu-->", op)
    if(op==1):
        customer_op=customer_menu()
        print("Value returned from customer menu-->", customer_op)
    if(op==2):
        own_op=owner_menu()
        print("Value returned from owner menu-->", own_op)
    if(op==3):
        print("EXIT, Thank You!")
#---------------------------------------------------------------------------------------------
def topmenu():
    option=0
    while 1:
        print("---Directory---")
        print("1: Customer")
        print("2: Owner")
        print("3: Exit")
        option=int(input("Type your option here:"))
        if (option>=1 and option<=3):
            break
        else:
            print("Invalid option, try again")
    return option
#---------------------------------------------------------------------------------------------
def customer_menu():
    total_price=0.0
    while 1:
        items=0
        c=1
        tline=['','','','','','','']
        print("Welcome to the Restaruant, what will you be having today?")
        z=open("products.txt",'r')
        for line in z:
            temp=str(c)+'.'+line
            print(temp)
            tline[c]=temp
            c=c+1
        z.close()
        maxc=c-1
        inumber=0
        print("Add to cart(A)  Exit(E)")
        customer_option=input("Please select your option:")
        if (customer_option=="E" or customer_option=="e"):
            break
        elif(customer_option=="A" or customer_option=="a"):
            items=items+1
        w=open("bill.txt","a")
        inumber=int(input("Select item number:"))
        if(inumber<1 or inumber>maxc):
            print("Item not found")
        else:
            print("Adding item...",inumber)
            print(tline[inumber])
            price_str = tline[inumber].split()[-1]
            if price_str.startswith('$'):
                    price = float(price_str[1:])
                    total_price += price
            w = open("bill.txt", "a")
            w.write(tline[inumber] + "\n")
            w.close()
    finalize_order(total_price)

def finalize_order(total_price):
    print(f'Total Price: ${total_price:.2f}')
    payment_type=process_payment()
    write_bill(payment_type, total_price)
    save_last_bill_to_report()

def save_last_bill_to_report():
    try:
        with open('bill.txt', 'r') as bill_file:
            lines=bill_file.readlines()
            if lines:
                last_line=lines[-1]
                with open('reports.txt', 'a') as report_file:
                    report_file.write(last_line)
                print("Last bill saved to reports.txt successfully.")
            else:
                print("No entries found in bill.txt.")
    except FileNotFoundError:
        print("Error: The file 'bill.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_payment():
    print("Please select your payment method:")
    print("1. Credit or Debit Card")
    print("2. Cash")
    choice = input("Enter 1 or 2: ")
    if choice == '1':
        print("Please select your card type:")
        print("1. VISA")
        print("2. Mastercard")
        card_choice = input("Enter 1 or 2: ")
        if card_choice == '1':
            card_type = 'VISA'
        elif card_choice == '2':
            card_type = 'Mastercard'
        else:
            print("Invalid selection. Please try again.")
            return process_payment()
        chip_swipe_payment(card_type)
        return f"Credit Card ({card_type})"
    elif choice == '2':
        cash_payment()
    else:
        print("Invalid selection. Please try again.")
        return process_payment()

def chip_swipe_payment(card_type):
    print(f"Please insert or swipe your {card_type} card.")
    response = simulate_payment_terminal()
    if response['status'] == 'success':
        print("Payment successful! Thank you for your purchase.")
    else:
        print("Payment failed. Please try again.")

def simulate_payment_terminal():
    return {"status": "success"}

def cash_payment():
    print("Thank you for choosing to pay with cash. Please hand the cash to the cashier.")
    
def write_bill(payment_type, total_amount):
    current_time = datetime.now()
    date_str = current_time.strftime("%Y-%m-%d")
    time_str = current_time.strftime("%H:%M:%S")
    with open('bill.txt', 'a') as file:
        file.write(f"{date_str}, {time_str}, {payment_type}, ${total_amount:.2f}\n")
#---------------------------------------------------------------------------------------------
def owner_menu():
    while 1:
        print("-------------")
        print("1: Charts")
        print("2: Reports")
        print("3: Exit")
        option=int(input("Type your option here:"))
        if option == 1:
            charts()
        elif option == 2:
            view_sales_reports()
        elif option == 3:
            print("Exiting the owner menu.")
            break
        else:
            print("Invalid option, try again.")

def charts():
    dataFrame=pd.read_csv('reports.txt', delimiter=',')
    print(dataFrame.head())
    print(dataFrame.columns)

    if dataFrame.empty:
        print("The DataFrame is empty.")
        return

    try:
        days_of_week = dataFrame['Day']
        total_payments = dataFrame['Total_Payment']
    except KeyError as e:
        print(f"Column not found: {e}")
        return
    days_of_week=dataFrame['Day']
    total_payments=dataFrame['Total_Payment']
    plt.figure(figsize=(10, 6))
    plt.plot(days_of_week, total_payments, marker='o', linestyle='-', color='blue', label='Total Payments')
    plt.title('Total Daily Payments from reports.txt', fontsize=16)
    plt.xlabel('Days of the Week', fontsize=14)
    plt.ylabel('Total Amount Paid ($)', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.savefig('total_daily_payments_from_reports.png')
    plt.show()

def view_sales_reports():
    file_path='reports.txt'
    try:
        with open(file_path, 'r') as file:
            print("Date, Time, Payment Type, Amount")
            for line in file:
                date, time, payment_type, amount = line.strip().split(',')
                print(f"{date.strip()}, {time.strip()}, {payment_type.strip()}, {amount.strip()}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
#---------------------------------------------------------------------------------------------
if __name__=='__main__':
    main()