from db.dbms import DBMS

class simple(DBMS):
    def __init__(self):
        self.locks = {} # locks
        self.completed = [] # transactions that have been completed
        self.started = [] # transaction that have been started

    def start(self, transaction:str) -> bool:
        if (transaction in self.started):
            return False
        
        self.started.append(transaction)
        print(f"Started transaction {transaction}")
        return True
    
    def commit(self, transaction:str) -> bool:
        if (transaction in self.completed) or not (transaction in self.started):
            return False
        self.locks = {key:val for key, val in self.locks.items() if val != transaction}
        self.completed.append(transaction)
        print(f"Commited transaction {transaction}")
        return True
    
    def read(self, transaction:str, key:str) -> (bool, str):
        if (transaction not in self.started or transaction in self.completed):
            return (False, None)
        if ((key in self.locks) and self.locks[key]!=transaction):
            return (False, None)
        
        self.locks[key]=transaction
        val = self.get(key)
        print(f"Transaction {transaction} read {key} with value {val}")
        return (True, val)
    
    def write(self, transaction:str, key:str, value:str) -> (bool, str):
        if (transaction not in self.started or transaction in self.completed):
            return (False, None)
        if ((key in self.locks) and self.locks[key]!=transaction):
            return (False, None)
        
        self.locks[key]=transaction
        self.put(key, value)
        print(f"Transaction {transaction} write {key} with value {value}")
        return (True, value)