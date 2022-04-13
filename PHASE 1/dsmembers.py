from dlist import DList
from orders import Orders

class Zones(DList):
    """Class that represents the zones, it is a DList"""
    #Add any method you may need
    def __init__(self):
        super().__init__()
    
class DSMember:
    """Class for a DSMember"""
    def __init__(self,iddsm,name,status,zones):
        self.iddsm=iddsm
        self.name=name
        self.status=status
        self.zones=Zones()
        self.zonesStr=""
        for z in zones:
            self.zones.addLast(z)
            if zones[0]==z:
                self.zonesStr+=str(z)
            else:
                self.zonesStr+=","+str(z)
                
        self.orders=Orders()
    #Add any method you may need
    
    def __str__(self):
        if self.orders.isEmpty():
            return("DSMember:" + str(self.iddsm) + "," + str(self.name)+ "," + str(self.status)  + "," + "Zones:" + str(self.zonesStr))
        else:
            return("DSMember:" + str(self.iddsm) + "," + str(self.name)+ "," + str(self.status)  + "," + "Zones:" + str(self.zonesStr)+ "\n\t"+ "Packages:\n\t\t"+ str(self.orders))
        
class DSMembers(DList):
       """Class that represents the dsmembers, it is a DList"""
       #Add any method you may need
       def __init__(self):
        super().__init__()
        
    