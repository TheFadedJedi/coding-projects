#Lab Week 9 in class assignment
def main():
    infile=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\Students.txt','a')
    infile.write("This is a new line. \n")
    infile.write("This is another new line. \n")
    infile.close()
    print("The new lines have been added to Students.txt.")
if __name__=='__main__':
    main()