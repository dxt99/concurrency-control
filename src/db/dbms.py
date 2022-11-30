# Abstract dbms class
class DBMS:

    def __init__():
        self.db={}
    
    def put(key:str, value:str):
        self.db[key]=value
    
    def get(key:str) -> str:
        return self.db[key]
    
    def append(key:str, value:str):
        self.db[key] = self.db[key] + value
    
    