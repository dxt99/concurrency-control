# Abstract dbms class
class DBMS:

    def __init__():
        self.db={}
    
    def put(key:str, value:str):
        self.db[key]=value
    
    def get(key:str) -> str:
        return self.db[key]

    def start(transaction:str) -> bool:
        raise NotImplementedError()
    
    def commit(transaction:str) -> bool:
        raise NotImplementedError()
    
    def read(transaction:str, key:str) -> (bool, str):
        raise NotImplementedError()
    
    def write(transaction:str, key:str, value:str) -> (bool, str):
        raise NotImplementedError()
    