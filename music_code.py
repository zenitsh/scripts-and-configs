dct={1:0,2:2,3:4,4:5,5:7,6:9,7:11}


a=input()

s=4
n=0
l=4
strr=""
b=False

for i in range(len(a)):
    if a[i]=='-':
        s+=4
    elif a[i]=='.':
        s-=1
    elif a[i]=='_':
        s=1
    elif a[i]=='[':
        strr=strr+"{%d,%d},"%(n,s)
        s=4
        l=l+1
        b=True
    elif a[i]==']':
        strr=strr+"{%d,%d},"%(n,s)
        s=4
        l=l-1
        b=True
    else:
        if not b:
            strr=strr+"{%d,%d},"%(n,s)
            s=4
        n=int(a[i])
        n=l*12+dct[n]
        b=False

strr=strr+"{%d,%d},"%(n,s)       
print(strr)    

input()
