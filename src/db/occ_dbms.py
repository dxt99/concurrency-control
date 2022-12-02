from db.dbms import DBMS

class OCC(DBMS):
    def __init__(self):
        self.readVals = {} # each transaction's read
        self.writeVals = {} # each transaction's write
        self.completed = {} # transactions that have been completed
        self.started = {} # transaction that have been started
        self.log = {} # list each transaction's commands
        self.globalClock = 0
    
    def parse(self, command:str):
        transaction = command.split(":")[0]
        if transaction not in self.log:
            self.log[transaction] = []
        self.log[transaction].append(command)
        super().parse(command)
        self.globalClock += 1

    def validate(self, transaction:str) -> bool:
        for complete, time in self.completed.items():
            if time < self.started[transaction]:
                continue
            elif self.started[transaction] < time < self.globalClock:
                for read in self.readVals[transaction]:
                    if read in self.writeVals[complete]:
                        return False 
            else:
                return False
        return True

    def start(self, transaction:str) -> bool:
        if (transaction in self.started):
            print(f"Transaction {transaction} started more than once")
            return False
        
        self.started[transaction] = self.globalClock
        self.readVals[transaction] = {}
        self.writeVals[transaction] = {}
        print(f"Started transaction {transaction}")
        return True
    
    def commit(self, transaction:str) -> bool:
        if (transaction in self.completed) or not (transaction in self.started):
            print(f"Transaction {transaction} failed to commit: not yet started or already committed")
            return False
        if (self.validate(transaction)):
            print(f"Validated transaction {transaction}")
            for key, value in self.writeVals[transaction].items():
                self.put(key, value)
                print(f"Transaction {transaction} write {key} with value {value}")
                self.globalClock+=1
            self.completed[transaction] = self.globalClock
            print(f"Committed transaction {transaction}")
            return True
        else:
            # restart transaction
            print(f"Validation failed for transaction {transaction}")
            print(f"Restarting transaction {transaction}")
            self.started.pop(transaction)
            tempLog = [a for a in self.log[transaction]]
            self.log[transaction] = []
            for command in tempLog:
                self.parse(command)
    
    def read(self, transaction:str, key:str) -> (bool, str):
        if (transaction not in self.started or transaction in self.completed):
            print(f"Transaction {transaction} failed to read {key}: not started or completed")
            return (False, None)
        val = self.get(key)
        self.readVals[transaction][key] = val
        print(f"Transaction {transaction} read {key} with value {val}")
        return (True, val)
        
    
    def write(self, transaction:str, key:str, value:str) -> (bool, str):
        if (transaction not in self.started or transaction in self.completed):
            print(f"Transaction {transaction} failed to write {key} with value {value}: not started or completed")
            return (False, None)
        self.writeVals[transaction][key] = value
        print(f"Transaction {transaction} write {key} with value {value} on local state")
        return (True, value)