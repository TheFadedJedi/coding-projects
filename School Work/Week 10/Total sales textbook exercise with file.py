#Total sales textbook exercise with files
def main():
    week={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    amount=[]
    totalsales=0
    for day in range(0,7):
        num=float(input("Type sales amount for "+week[day]+":"))
        amount.append(num)
        totalsales=totalsales+num
        z=open('sales.txt','w')
        z.write(str(amount))
        z.close()
    print(amount)
if __name__=='__main__':
    main()
