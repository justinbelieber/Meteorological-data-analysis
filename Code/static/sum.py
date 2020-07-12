if __name__=="__main__":
    while True:
        try:
            ls = input("").split(" ")
            x=int(ls[0])
            y=int(ls[1])
            print(x+y)
        except:
            break;