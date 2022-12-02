import sys, os
from db.dbms import DBMS
from db.simple_dbms import simple
from db.occ_dbms import OCC

algorithms = ["simple", "occ"]

def main():
    if (len(sys.argv)!=3):
        print("Usage: main.py [algorithm=simple/occ] [transaction schedule]")
        return
    if (sys.argv[1] not in algorithms):
        print("Algorithm is not found")
        print("Usage: main.py [algorithm=simple/occ] [transaction schedule]")
        return
    filename = sys.argv[2]
    if (not os.path.isfile(filename)):
        print("File not found")
        print("Usage: main.py [algorithm=simple/occ] [transaction schedule]")
        return
    
    dbms = simple()
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        dbms.parse(line)
        pass

if __name__=='__main__':
    main()