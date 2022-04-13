from myqueue import SQueue

class Package:
    """Class for one package"""
    def __init__(self,idpac,street,num,pc):
        self.idpac=idpac
        self.street=street
        self.num=num
        self.pc=pc
        #By default the number of attempts for a package is 0
        self.numAttempts=0
    
     #Add any method you may need
    def __str__(self):
        return(str(self.idpac)+" "+str(self.street)+" "+str(self.num)+" "+str(self.pc)+" "+str(self.numAttempts))
    
class Orders(SQueue):
    """Class that represents the zones, it is a queue"""
    def __init__(self):
        super().__init__()
    #Add any method you may need

    
class PackageDelivered(SQueue):
    """To represent packages successfully delivered"""
    def __init__(self):
        super().__init__()
        
   
     #Add any method you may need
    
            
class PackageIncidence(SQueue):
    """To represent packages that have suffered some incident"""
    #Add any method you may need
    def __init__(self):
        super().__init__()
        
      
 