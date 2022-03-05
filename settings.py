import sys

class Balance:
    def __init__(self, manager):
        self.argvs = manager.read_sys()
        self.data = manager.input_data()
        self.kind = "saldo"
        self.value = 0
        self.comment = ""

    def read_from_list(self, i, balance_sum, goods_dict):
        self.value = int(self.data[i+1])
        if balance_sum:
            balance_sum += int(self.value)
        else:
            balance_sum = int(self.value)   
        self.comment = self.data[i+2]
        i+=3
        return int(i), int(balance_sum)

    def __call__(self):
        print(f"{self.kind}\n{self.value}\n{self.comment}")

    def save_to_file(self, balance_sum, obj_list):
        if len(self.argvs)<3:
            print("not enought arguments")
        else:
            self.value = self.argvs[1]
            self.comment = self.argvs[2]
            if balance_sum + int(self.value) >=0:
                obj_list.append(self)
                self.data.append(self.kind) 
                self.data.append(self.value) 
                self.data.append(self.comment) 
                with open(f"{self.argvs[0]}", "a") as f:
                    f.write("\n") 
                    f.write(f"{self.kind}\n") 
                    f.write(f"{self.value}\n") 
                    f.write(f"{self.comment}") 
            else:
                print("\nyou can not have debit balance!\n")
           

class Sale:
    def __init__(self, manager):
        self.argvs = manager.read_sys()
        self.data = manager.input_data()
        self.kind = "sprzedaz"
        self.id = ""
        self.price = 0
        self.number = 0

    def read_from_list(self, i, balance_sum, goods_dict):
        if self.data[i+1] not in goods_dict:
            print (f"\nwe don't have on stock {self.id}\n") 
        else:
            self.id = self.data[i+1]
            self.price = int(self.data[i+2])
            if goods_dict[self.data[i+1]] - int(self.data[i+3]) < 0:
                print (f"not enough {self.id} on stock")
            else:
                self.number = int(self.data[i+3])
                goods_dict[self.id] -= self.number
                balance_sum += int(self.price) * int(self.number)
                i+=4
        return int(i), int(balance_sum)
    
    def __call__(self):
        print(f"{self.kind}\n{self.id}\n{self.price}\n{self.number}")

    def save_to_file(self, obj_list, goods_dict):
        if len(self.argvs)<4:
            print("not enought arguments")
        else:
            self.id = self.argvs[1]
            self.price = self.argvs[2]
            self.number = self.argvs[3]
            if self.id not in goods_dict:
                print (f"\nwe don't have stock of {self.id} at all\n")
            else:
                if goods_dict[self.id] - int(self.number) <0:
                    print(f"not enough {self.id} on stock")
                else:
                    obj_list.append(self)
                    self.data.append(self.kind) 
                    self.data.append(self.id) 
                    self.data.append(self.price) 
                    self.data.append(self.number) 
                    with open(f"{self.argvs[0]}", "a") as f:
                        f.write("\n") 
                        f.write(f"{self.kind}\n") 
                        f.write(f"{self.id}\n")
                        f.write(f"{self.price}\n")  
                        f.write(f"{self.number}")     


class Purchase:
    def __init__(self, manager):
        self.argvs = manager.read_sys()
        self.data = manager.input_data()
        self.kind = "zakup"
        self.id = ""
        self.price = 0
        self.number = 0

    def read_from_list(self, i, balance_sum, goods_dict):
        self.id = self.data[i+1]
        self.price = int(self.data[i+2])
        self.number = int(self.data[i+3])
        if balance_sum - self.price * self.number <0:
            print("\nyou can not have debit balance!\n")
        else:
            balance_sum -= self.price * self.number 
            if self.id in goods_dict:
                goods_dict[self.id] += self.number
            else:
                goods_dict[self.id] = self.number  
            i+=4
        return int(i), int(balance_sum)

    def __call__(self):
        print(f"{self.kind}\n{self.id}\n{self.price}\n{self.number}")

    def save_to_file(self, balance_sum, obj_list):
        if len(self.argvs)<4:
            print("not enought arguments")
        else:
            self.id = self.argvs[1]
            self.price = self.argvs[2]
            self.number = self.argvs[3]
            if balance_sum - int(self.price) * int(self.number) < 0:
                print("\nyou can not have debit balance!\n")
            else:
                obj_list.append(self)
                self.data.append(self.kind) 
                self.data.append(self.id) 
                self.data.append(self.price) 
                self.data.append(self.number) 
                with open(f"{self.argvs[0]}", "a") as baza:
                    baza.write("\n") 
                    baza.write(f"{self.kind}\n") 
                    baza.write(f"{self.id}\n")
                    baza.write(f"{self.price}\n")  
                    baza.write(f"{self.number}")


class Manager: 
    types = {"zakup":Purchase, "saldo":Balance, "sprzedaz":Sale}  
    
    def __init__(self):
        self.actions = {}
        self.data = []
    
    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate
        
    def execute(self, name):
        if name not in self.actions:
            print("Action not defined")
        else:
            self.actions[name](self)

    def read_sys(self):
        try:
            self.argvs = sys.argv[1:]
        except IndexError:
            print("no arguments were given")
        return self.argvs   

    def input_data(self):
        if not self.argvs:
            print("no arguments were given")
        else:
            with open(f"{self.argvs[0]}") as f:
                self.data = []
                for line in f:
                    self.data.append(line.strip())
                return self.data  

    def main(self):
        i = 0 
        goods_dict = {}
        obj_list = []
        self.read_sys()
        operation_list = self.input_data()
        balance_sum = 0  
        while i < len(operation_list):
            type = ""
            type = operation_list[i]
            if type == "":
                i+=1
                continue
            if type not in self.types:
                print("zonk")
                break
            obj = self.types[type](self)
            i, balance_sum = obj.read_from_list(i, balance_sum, goods_dict)
            obj_list.append(obj) 
        return goods_dict, obj_list, balance_sum
     

def store_manager():
    manager = Manager()
    @manager.assign("warehouse") 
    def inventory_query(manager):
        Manager.read_sys(manager)
        if len(manager.argvs) == 1:
            print("no goods were given")
        else:    
            for i in manager.argvs[1:]:
                goods_dict, obj_list, balance_sum = manager.main()
                if i in goods_dict:
                    print(f"quantity of {i} is: {goods_dict[i]}")  
                else:
                    print(f"quantity of {i} is: 0")

    @manager.assign("log") 
    def log_query(manager):
        Manager.read_sys(manager)
        goods_dict, obj_list, balance_sum = manager.main()
        if len(manager.argvs) < 2:
            print("no arguments were given")
        elif len(manager.argvs) == 2:
            for i in obj_list:
                i()
        elif len(manager.argvs) > 2:
            from_range = int(manager.argvs[1])-1
            range_to = int(manager.argvs[2])
            if range_to >= len(obj_list):
                range_to = len(obj_list)
            for i in obj_list[from_range:range_to]:
                i()

    @manager.assign("account")
    def account_query(manager):
        Manager.read_sys(manager)
        if len(manager.argvs)>=1:
            goods_dict, obj_list, balance_sum = manager.main()
            print(f"The balance is {balance_sum}")

    @manager.assign("balance")
    def balance_query(manager):
        obj = Balance(manager)
        Manager.read_sys(manager)
        goods_dict, obj_list, balance_sum = manager.main()
        obj.save_to_file(balance_sum, obj_list)        

    @manager.assign("sale") 
    def sale_query(manager):
        Manager.read_sys(manager)
        if len(manager.argvs)>=1:
            goods_dict, obj_list, balance_sum = manager.main()
            obj = Sale(manager)
            obj.save_to_file(obj_list, goods_dict)

    @manager.assign("purchase") 
    def purchase_query(manager):
        Manager.read_sys(manager)
        if len(manager.argvs) >= 1:
            goods_dict, obj_list, balance_sum = manager.main()
            obj = Purchase(manager)
            obj.save_to_file(balance_sum, obj_list)
    return manager