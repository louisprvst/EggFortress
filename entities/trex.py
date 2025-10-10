from Units import Units

class Trex(Units) :

    # Constructeur pour le T Rex ( Dino 3 )
    def __init__(self , position : tuple , owner : str ) :
        super().__init__(50 , 1 , 100 , 200 , 20 , position , owner)