from dataclasses import dataclass

@dataclass
class  Coordinate():
    x : float   = 0.0
    y : float   = 0.0
    z : float   = 0.0

    def __str__(self) -> str:
        Status = f'x: {self.x:.2f}  y: {self.y:.2f} z: {self.z:.2f}'
        return Status

@dataclass
class  RotationalCoordinate():
    x : float   = 0.0
    t : float   = 0.0

    def __str__(self) -> str:
        Status = f'x: {self.x:.2f}  t: {self.t:.2f}'


class MovingComponent():

    def __init__(self, *arg, **kwarg) -> None:
        self.Name = "" if (not "Name" in kwarg) else kwarg['Name']
        # self.Width = 100 if (not "Width" in kwarg) else kwarg['Width']
        # self.Height = 100 if (not "Height" in kwarg) else kwarg['Height']
        
        self.Dimension = Coordinate(x = 100.0, y = 100.0, z = 100)
        self.CurrPos =  Coordinate()
        self.MaxPos = Coordinate()
        self.MinPos = Coordinate()
        self.SIToPixRatio = Coordinate()

        if ("CurrPos" in kwarg and isinstance(kwarg["CurrPos"], Coordinate)):
            self.CurrPos = kwarg["CurrPos"]
        
        if ("MaxPos" in kwarg and isinstance(kwarg["MaxPos"], Coordinate)):
            self.MaxPos = kwarg["MaxPos"]

        if ("MinPos" in kwarg and isinstance(kwarg["MinPos"], Coordinate)):
            self.MinPos = kwarg["MinPos"]

        if ("SIToPixRatio" in kwarg and isinstance(kwarg["SIToPixRatio"], Coordinate)):
            self.SIToPixRatio = kwarg["SIToPixRatio"]

    def __str__(self) -> str:
        Status = f'Name: {self.Name} Width: {self.Width}    Height: {self.Height}\nCurrPos:     {str(self.CurrPos)} \nMax:      {self.MaxPos}\nMin:     {self.MinPos}\nSIToPixRatio:    {self.SIToPixRatio}'
        return Status
    
if __name__ == '__main__':
    # Eye = MovingComponent(Name = "Hand", x = 10, y = 20, z = 30)
    Head = MovingComponent(CurrPos = Coordinate(x = 5.0))
    leg = MovingComponent()
    print(Head)