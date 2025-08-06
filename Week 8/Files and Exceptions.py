#example 1 text file
#def main():
#    infile=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\data100.txt','r')
#    contents=infile.read()
#    print('---Contents---')
#    print(contents)
#if __name__=='__main__':
#    main()
#----------------------------------------------
#def main():
#    infile=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\data100.txt','r')
#    line1=infile.readline()
#    line2=infile.readline()
#    line3=infile.readline()
#    infile.close()
#    print(line1)
#    print(line2)
#    print(line3)
#if __name__=='__main__':
#    main()
#----------------------------------------------
def main():
    print('Enter the names of three friends.')
    name1=input('Friend #1:')
    name2=input('Friend #2:')
    name3=input('Friend #3:')
    myfile=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\friends.txt','w')
    myfile.write(name1+'\n')
    myfile.write(name2+'\n')
    myfile.write(name3+'\n')
    myfile.close()
    print('The names were written to friends.txt.')
if __name__=='__main__':
    main()
#----------------------------------------------
#def main():
#    infile=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\data100.txt','r')
#    line1=infile.readline()
#    line2=infile.readline()
#    line3=infile.readline()
#    line1=line1.rstrip('\n')
#    line1=line2.rstrip('\n')
#    line1=line3.rstrip('\n')
#    infile.close()
#    print(line1)
#    print(line2)
#    print(line3)
#if __name__=='__main':
#    main()
#----------------------------------------------
#def main():
#    outfile=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\numbers.txt','w')
#    num1=int(input('Enter a number: '))
#    num2=int(input('Enter another number: '))
#    num3=int(input('Enter another number: '))
#    outfile.write(str(num1)+'\n')
#    outfile.write(str(num2)+'\n')
#    outfile.write(str(num3)+'\n')
#    outfile.close()
#if __name__=='__main__':
#    main()
#----------------------------------------------
#def main():
#    infile=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\numbers.txt','r')
#    num1=int(infile.readline())
#    num2=int(infile.readline())
#    num3=int(infile.readline())
#    infile.close()
#    total=num1+num2+num3
#    print(f'The numbers are: {num1}, {num2}, {num3}')
#    print(f'Their total is: {total}')
#if __name__=='__main__':
#    main()
#----------------------------------------------
#def main():
#    num_days=int(input('For how many days do'+'you have sales?'))
#    sales_file=open('sales.txt','w')
#    for count in range(1,num_days+1):
#        sales=float(input(f'Enter the sales for day #{count}:'))
#        sales_file.write(f'{sales}\n')
#    sales_file.close()
#    print('Data written to sales.txt.')
#if __name__=='__main__':
#    main()
#----------------------------------------------
#def main():
#    sales_file=open('sales.txt','r')
#    line=sales_file.readline{}
#    while line!='':
#        amount=float{line}
#        print(f'{amount:.2f}')
#        line=sales_file.readline{}
#   sales_file.close()
#if __name__=='__main__':
#    main()
#----------------------------------------------
#def main():
#    sales_file=open('sales.txt','r')
#    for line in sales_file:
#        amount=float(line)
#        print(f'{amount:.2f}')
#    sales_file.close()
#if __name__=='__main__':
#    main()