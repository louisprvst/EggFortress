from Units import Units

class Diplodocus(Units) :

    # Constructeur pour le diplodocus ( Dino 1 )
    def __init__(self , position : tuple , owner : str ) :
        super().__init__(10 , 2 , 25 , 50 , 5 , position , owner)