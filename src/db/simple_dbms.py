from db.dbms import DBMS

class simple(DBMS):
    def __init__(self):
        self.locks = {} # locks
        self.completed = [] # transactions that have been completed
        self.started = [] # transaction that have been started
        self.queue = [] # commands in queue
        self.inQueue = [] # transactions in queue

    def start(self, transaction:str) -> bool:
        if (transaction in self.started):
            print(f"Transaction {transaction} started more than once")
            return False
        
        self.started.append(transaction)
        print(f"Started transaction {transaction}")
        return True
    
    def commit(self, transaction:str) -> bool:
        if (transaction in self.completed) or not (transaction in self.started):
            print(f"Transaction {transaction} failed to commit: not yet started or already committed")
            return False
        if (transaction in self.inQueue):
            print(f"Queued commit transaction {transaction}")
            self.queue.append(f"{transaction}: commit")
            return False
        self.locks = {key:val for key, val in self.locks.items() if val != transaction}
        self.completed.append(transaction)
        print(f"Commited transaction {transaction}")
        self.doQueue()
        return True
    
    def read(self, transaction:str, key:str) -> (bool, str):
        if (transaction not in self.started or transaction in self.completed):
            print(f"Transaction {transaction} failed to read {key}: not started or completed")
            return (False, None)
        if ((key in self.locks) and self.locks[key]!=transaction):
            print(f"Queued transaction {transaction} read {key}")
            self.queue.append(f"{transaction}: read {key}")
            self.inQueue.append(transaction)
            return (False, None)
        
        self.locks[key]=transaction
        val = self.get(key)
        print(f"Transaction {transaction} read {key} with value {val}")
        return (True, val)
    
    def write(self, transaction:str, key:str, value:str) -> (bool, str):
        if (transaction not in self.started or transaction in self.completed):
            print(f"Transaction {transaction} failed to write {key} with value {value}: not started or completed")
            return (False, None)
        if ((key in self.locks) and self.locks[key]!=transaction):
            print(f"Queued transaction {transaction} write {key} with value {value}")
            self.queue.append(f"{transaction}: write {key} {value}")
            self.inQueue.append(transaction)
            return (False, None)
        
        self.locks[key]=transaction
        self.put(key, value)
        print(f"Transaction {transaction} write {key} with value {value}")
        return (True, value)
    
    def doQueue(self):
        if len(self.queue) == 0:
            return
        print("Retrying queued operations")
        tempQueue = [a for a in self.queue]
        self.queue = []
        self.inQueue = []
        for action in tempQueue:
            self.parse(action)