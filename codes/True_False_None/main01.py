class Mydata:
    def __init__(self, value) -> None:
        self.value = 1
    
    def __len__(self):
        return 0
    
    def __bool__(self):
        return True
    
    def __eq__(self, __value: object):
        return False
    

a = Mydata(1)

if a:
    print("True")
else:
    print("False")

if a == None:
    print("a == None")
else:
    print("a != None")