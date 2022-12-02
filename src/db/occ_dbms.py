from db.dbms import DBMS

class OCC(DBMS):
    def __init__():
        self.states = {} # each transaction's state
        self.completed = [] # transactions that have been completed
        self.started = [] # transaction that have been started

    def start(transaction:str) -> bool:
        if (transaction in self.started):
            return False
        
        self.started.append(transaction)
        return True
    
    def commit(transaction:str) -> bool:
        if (transaction in self.completed) or not (transaction in self.started):
            return False
        # TODO: start validation

    
    def read(transaction:str, key:str) -> (bool, str):
        raise NotImplementedError()
    
    def write(transaction:str, key:str, value:str) -> (bool, str):
        raise NotImplementedError()