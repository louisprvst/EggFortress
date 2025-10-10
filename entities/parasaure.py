from Units import Units

class Parasaure(Units) :

    # Constructeur pour le parasaure ( Dino 2 )
    def __init__(self , position : tuple , owner : str ) :
        super().__init__(25 , 2 , 50 , 100 , 10 , position , owner)