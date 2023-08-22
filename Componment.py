from dataclasses import dataclass

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

        if ("Dimension" in kwarg):
            if (isinstance(kwarg["Dimension"], Coordinate)):
                self.Dimension = kwarg["Dimension"]
            elif (isinstance(kwarg["Dimension"], dict)):
                self.Dimension = Coordinate(**kwarg["Dimension"])

        if ("CurrPos" in kwarg):
            if (isinstance(kwarg["CurrPos"], Coordinate)):
                self.CurrPos = kwarg["CurrPos"]
            elif (isinstance(kwarg["CurrPos"], dict)):
                self.CurrPos = Coordinate(**kwarg["CurrPos"])

        if ("MaxPos" in kwarg):
            if (isinstance(kwarg["MaxPos"], Coordinate)):
                self.MaxPos = kwarg["MaxPos"]
            elif (isinstance(kwarg["MaxPos"], dict)):
                self.MaxPos = Coordinate(**kwarg["MaxPos"])

        if ("MinPos" in kwarg):
            if (isinstance(kwarg["MinPos"], Coordinate)):
                self.MinPos = kwarg["MinPos"]
            elif (isinstance(kwarg["MinPos"], dict)):
                self.MinPos = Coordinate(**kwarg["MinPos"])

        if ("SIToPixRatio" in kwarg):
            if (isinstance(kwarg["SIToPixRatio"], Coordinate)):
                self.SIToPixRatio = kwarg["SIToPixRatio"]
            elif (isinstance(kwarg["SIToPixRatio"], dict)):
                self.SIToPixRatio = Coordinate(**kwarg["SIToPixRatio"])


        # if ("CurrPos" in kwarg and isinstance(kwarg["CurrPos"], Coordinate)):
        #     self.CurrPos = kwarg["CurrPos"]
        
        # if ("MaxPos" in kwarg and isinstance(kwarg["MaxPos"], Coordinate)):
        #     self.MaxPos = kwarg["MaxPos"]

        # if ("MinPos" in kwarg and isinstance(kwarg["MinPos"], Coordinate)):
        #     self.MinPos = kwarg["MinPos"]

        # if ("SIToPixRatio" in kwarg and isinstance(kwarg["SIToPixRatio"], Coordinate)):
        #     self.SIToPixRatio = kwarg["SIToPixRatio"]

    def __str__(self) -> str:
        Status = f'{"Name:":15}{self.Name}\n{"Dimension":15}{self.Dimension}\n{"CurrPos:":15}{str(self.CurrPos)}\n{"Max:":15}{self.MaxPos}\n{"Min:":15}{self.MinPos}\n{"SIToPixRatio:":15}{self.SIToPixRatio}'
        return Status

class ArmComponent(MovingComponent):
    def __init__(self, *arg, **kwarg) -> None:
        super().__init__(*arg, **kwarg)

if __name__ == '__main__':
    # Eye = MovingComponent(Name = "Hand", x = 10, y = 20, z = 30)
    Head = MovingComponent(CurrPos = Coordinate(x = 5.0))
    leg = MovingComponent()
    print(Head)