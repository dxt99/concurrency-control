# Abstract dbms class
class DBMS:
    
    db = {}

    def put(self, key:str, value:str):
        self.db[key]=value
    
    def get(self, key:str) -> str:
        if key not in self.db:
            self.db[key]=""
        return self.db[key]

    def start(self, transaction:str) -> bool:
        raise NotImplementedError()
    
    def commit(self, transaction:str) -> bool:
        raise NotImplementedError()
    
    def read(self, transaction:str, key:str) -> (bool, str):
        raise NotImplementedError()
    
    def write(self, transaction:str, key:str, value:str) -> (bool, str):
        raise NotImplementedError()
    
    def parse(self, command:str):
        #print(command)
        if not(":" in command):
            return
        temp = command.split(":", 1)
        transaction = temp[0]
        args = temp[1].strip().split(" ")
        if args[0].lower() == 'start' and len(args)==1:
            self.start(transaction)
        elif args[0].lower() == 'write' and len(args)==3:
            self.write(transaction, args[1], args[2])
        elif args[0].lower() == 'read' and len(args)==2:
            self.read(transaction, args[1])
        elif args[0].lower() == 'commit' and len(args)==1:
            self.commit(transaction)