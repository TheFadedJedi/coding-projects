#Read a file
def main():
    c=0
    names=[]
    z=open('names.txt','r')
    w=open('names400.txt','w')
    for line in z:
        w.write(line)
        c=c+1
        if c>400:
            break
    z.close()
    w.close()
    print(c)
if __name__=='__main__':
    main()