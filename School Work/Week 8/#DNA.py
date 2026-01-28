#DNA
def main():
    tnc=0
    ng=0
    nc=0
    z=open('C:\\Users\\kerns\\Documents\\HCC\\Spring2025\\CSC-130\\dna.txt','r')
    for line in z:
        tnc=(tnc+len(line))
        for i in range(0,37):
            if line[i]=='G':
                ng=(ng+1)
            if line[i]=='C':
                nc=(nc+1)
    z.close()
    print(ng)
    print(nc)
    print(tnc)
    GCcontent=((ng+nc)/(tnc))
    print("The total GC content is:",(GCcontent))
if __name__=='__main__':
    main()