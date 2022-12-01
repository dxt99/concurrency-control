import sys, os

def main():
    if (len(sys.argv)!=2):
        print("Usage: main.py [transaction schedule]")
        return
    filename = sys.argv[1]
    if (not os.path.isfile(filename)):
        print("File not found")
        return
    
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        #TODO: parse action to dbms
        pass

if __name__=='__main__':
    main()