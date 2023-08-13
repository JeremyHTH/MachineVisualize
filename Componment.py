class MovingComponent():

    def __init__(self, *arg, **kwarg) -> None:
        self.Name = "" if (not "Name" in kwarg) else kwarg['Name']
        self.x = 0 if (not "x" in kwarg) else kwarg['x']
        self.y = 0 if (not "y" in kwarg) else kwarg['y']
        self.z = 0 if (not "z" in kwarg) else kwarg['z']
        self.t = 0 if (not "t" in kwarg) else kwarg['t']

    def __str__(self) -> str:
        Status = f'Name : {self.Name} \nx: {self.x} y: {self.y} z: {self.z} t: {self.t}'
        return Status
    
if __name__ == '__main__':
    Eye = MovingComponent(Name = "Hand", x = 10, y = 20, z = 30)
    print(Eye)