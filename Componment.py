from dataclasses import dataclass
import numpy
import abc

@dataclass()
class  Coordinate():
    x : float   = 0.0
    y : float   = 0.0
    z : float   = 0.0

    def __str__(self) -> str:
        Status = f'{"x:":>8}{self.x:10.2f}{"y:":>8}{self.y:10.2f}{"z:":>8}{self.z:10.2f}'
        return Status

@dataclass
class  RotationalCoordinate():
    x : float   = 0.0
    t : float   = 0.0

    def __str__(self) -> str:
        Status = f'x: {self.x:.2f}  t: {self.t:.2f}'
        return Status

class MovingComponent():
    def __init__(self) -> None:
        self.Name = "No name"
        self.Dimension = None
        self.CurrPos =  None
        self.MaxPos = None
        self.MinPos = None
        self.MaxPixPos = None
        self.MinPixPos = None
        self.SIToPix : list[list] = [] # Ax + b
    
    def CalibrateSIToPix(self):
        return


    def GetPixelPos(self):
        return [0, 0, 0]

class CartesianComponent(MovingComponent):

    def __init__(self, *arg, **kwarg) -> None:
        super().__init__()
        if ('Name' in kwarg):
            self.Name = kwarg['Name'] # "" if (not "Name" in kwarg) else kwarg['Name']
        # self.Width = 100 if (not "Width" in kwarg) else kwarg['Width']
        # self.Height = 100 if (not "Height" in kwarg) else kwarg['Height']

        if ("Dimension" in kwarg):
            if (isinstance(kwarg["Dimension"], Coordinate)):
                self.Dimension = kwarg["Dimension"]
            elif (isinstance(kwarg["Dimension"], dict)):
                self.Dimension = Coordinate(**kwarg["Dimension"])
        
        if (not self.Dimension):
            self.Dimension = Coordinate(100,100,50)

        if ("CurrPos" in kwarg):
            if (isinstance(kwarg["CurrPos"], Coordinate)):
                self.CurrPos = kwarg["CurrPos"]
            elif (isinstance(kwarg["CurrPos"], dict)):
                self.CurrPos = Coordinate(**kwarg["CurrPos"])
        
        if (not self.CurrPos):
            self.CurrPos = Coordinate()

        if ("MaxPos" in kwarg):
            if (isinstance(kwarg["MaxPos"], Coordinate)):
                self.MaxPos = kwarg["MaxPos"]
            elif (isinstance(kwarg["MaxPos"], dict)):
                self.MaxPos = Coordinate(**kwarg["MaxPos"])
        
        if (not self.MaxPos):
            self.MaxPos = Coordinate()

        if ("MinPos" in kwarg):
            if (isinstance(kwarg["MinPos"], Coordinate)):
                self.MinPos = kwarg["MinPos"]
            elif (isinstance(kwarg["MinPos"], dict)):
                self.MinPos = Coordinate(**kwarg["MinPos"])
        
        if (not self.MinPos):
            self.MinPos = Coordinate()

        if ('SIToPix' in kwarg):
            self.SIToPix = kwarg['SIToPix']
        if (not self.SIToPix):
            self.SIToPix = {'x':[1, 0], 'y':[1, 0], 'z': [1, 0]}



    def CalibrateSIToPix(self):
        X = [[self.MaxPos.x, self.MinPos.x],[self.MaxPos.y, self.MinPos.y],[self.MaxPos.z, self.MinPos.z]]
        Y = [[self.MaxPixPos.x + self.Dimension.x, self.MinPixPos.x + self.Dimension.x],
             [self.MaxPixPos.y + self.Dimension.y, self.MinPixPos.y + self.Dimension.y],
             [self.MaxPixPos.z + self.Dimension.z, self.MinPixPos.z + self.Dimension.z]]

        Coeff = [[] for _ in range(3)]
        for index, item in enumerate(('x', 'y', 'z')):
            self.SIToPix[item] = list(numpy.polyfit(X[index], Y[index],deg = 1))

        

    def GetPixelPos(self):
        return Coordinate(  self.CurrPos.x * self.SIToPix['x'][0] + self.SIToPix['x'][1],
                            self.CurrPos.y * self.SIToPix['y'][0] + self.SIToPix['y'][1],
                            self.CurrPos.z * self.SIToPix['z'][0] + self.SIToPix['z'][1])

    def __str__(self) -> str:
        Status = f'{"Name:":15}{self.Name}\n{"Dimension":15}{self.Dimension}\n{"CurrPos:":15}{str(self.CurrPos)}\n{"Max:":15}{self.MaxPos}\n{"Min:":15}{self.MinPos}\n'
        return Status

class ArmComponent(MovingComponent):
    def __init__(self, *arg, **kwarg) -> None:
        super().__init__(*arg, **kwarg)

        


if __name__ == '__main__':
    # Eye = MovingComponent(Name = "Hand", x = 10, y = 20, z = 30)
    Head = CartesianComponent(Name = "Head", CurrPos = Coordinate(x = -1000.0, y = -1000, z = -1000))
    # leg = CartesianComponent()
    Head.MaxPos = Coordinate(x = 1000, y = 1000, z = 1000)
    Head.MinPos = Coordinate(x = -1000, y = -1000, z = -1000)
    Head.MaxPixPos = Coordinate(x = 600, y = 420, z = 840)
    Head.MinPixPos = Coordinate(0, 0, 0)

    print(Head)

    Head.CalibrateSIToPix()
    print(Head.GetPixelPos())

    Head.CurrPos = Coordinate(1000, 1000, 1000)

    print(Head.GetPixelPos())