from dsmembers import DSMembers
from dsmembers import DSMember
from myqueue import SQueue
from orders import Orders
from orders import Package
from orders import PackageDelivered
from orders import PackageIncidence
import sys


import random 


class AmazonManagement:
    """Main class including functionality for phase 1"""
    
    def __init__(self):
        self.orders=Orders()
        self.dsmembers=DSMembers()
        self.delivered=PackageDelivered()
        self.incidences=PackageIncidence()
        #here we create an auxiliary queue that will be used later on
        self.auxiliary=SQueue()
        

    def loadOrders(self,data):
        """ This method receives the data needed to initialize the object 
        storing the orders that Amazon must deliver  
        """
        for t in data:
            idpac=t[0]
            street=t[1]
            num=t[2]
            pc=t[3]
            package=Package(idpac,street,num,pc)
            #include the instructions needed to add the package to the orders 
            #object
            #introducing all the packages in the orders queue class
            self.orders.enqueue(package)
            

    def loadDSMembers(self,data):
        """ This method receives data to initialice the object storing the 
        delivery staff members at Amazon"""
        for t in data:
            iddsm=t[0]
            name=t[1]
            status=t[2]
            zones=t[3]
                
            dsmember=DSMember(iddsm,name,status,zones)
            #include the operations needed to add the dsmember to the dsmembers
            #object
            
            #this function introduce the dsmembers directly in alphabetical order
            
            #first case. The list is empty
            if self.dsmembers.isEmpty():
               self.dsmembers.addLast(dsmember)
               
            #second case. The list only has one element
            elif self.dsmembers.size==1:
                if dsmember.name.lower()<self.dsmembers.head.elem.name.lower():
                    self.dsmembers.addFirst(dsmember)
                else:
                    self.dsmembers.addLast(dsmember)
                
            #third case. The list has more than one element
            #we traverse the list until we find an element greater than 
            #the one we want to add to the list. Then, we introduce it
            else:

                current = self.dsmembers.head
                counter = 0
                while current and dsmember.name.lower() > current.elem.name.lower():
                    counter += 1
                    current =current.next
                self.dsmembers.insertAt(counter, dsmember)
                        
                        
    def showDSMembers(self):
        """Shows delivery staff members by alphabetical order"""
        current = self.dsmembers.head
        while current:
            print (current.elem, '\n')
            current  = current.next


    def assignDistribution(self):
        """
        assigns each order (package) to a distributor. Remember that the 
        distributor must be active and must cover the area of the package.
        If there is no active distributor for that zone, the package (and its 
        zone) will be assigned to the active distributor with fewer zones.
          """
       
        #we create a double foor loop. The first one for the dsmembers, 
        #for each dsmember we traverse the orders list (second loop), 
        #and then we check if the zone of that order is in the dsmember´s orders.
        #If the order´s zone matches any of the dsmemeber´s. We assign it.
        
        for a in range(self.dsmembers.size):
            dsm=self.dsmembers.getAt(a)
            #the length of the orders is saved
            myLen=self.orders.size
            for b in range(self.orders.size):
                if dsm.zones.search(self.orders.top().pc) and dsm.status=="Active":
                        dsm.orders.enqueue(self.orders.dequeue())
                        
                #if the length have not changed means that no package has been assigned 
                #so we sent that package to the end of the queue
                if self.orders.size==myLen:
                    self.orders.enqueue(self.orders.dequeue())
                    
        #if there are remaining orders we assign an extra zone to somebody and deliver those orders
        #after that the method is called again.
        if not self.orders.isEmpty():
            for i in range(self.orders.size):
                self.assignExtraZone(self.orders.top().pc)
                self.orders.enqueue(self.orders.dequeue())
            self.assignDistribution()
                
            
    def assignExtraZone(self,zone):
        """ This method is invoked in case nobody has the zone of a package to deliver. 
        This function assign that extra zone to the                         
            person with the minimum number of zones """
        
        #the first loop checks the dsmemeber with the least number of zones and saves that number
        #the second one checks who has that minimun number of zones and assigns the new zone to him
        minZone=sys.maxsize
        for a in range(self.dsmembers.size):
            if self.dsmembers.getAt(a).zones.size < minZone:
                minZone=self.dsmembers.getAt(a).zones.size
        for a in range(self.dsmembers.size):
            if self.dsmembers.getAt(a).zones.size == minZone:
                self.dsmembers.getAt(a).zones.addLast(zone)
                return 
            
                
    def deliverPackages(self,dsmember):
        """ which simulates the delivery of the
        packages for a specific distributor. The function receives a distributor
        (identifier) and must process all its packages, always starting with the first
        package and processing them in strict order"""
        
        #we get the index of the dsmember with a while loop
        check=True
        index=0
        
        while check:
            
            if self.dsmembers.getAt(index).iddsm == dsmember:
                check=False
                
            else:
                index+=1
    
        dsm=self.dsmembers.getAt(index)
        
        #if the dsmember has packages to deliver
        if not dsm.orders.isEmpty():
            #while there are packages to deliver...
            while dsm.orders.size !=0:
                print("\n processing delivery for: ")
                print(dsm, "\n")
                print("Package to deliver ...",dsm.orders.top() )
                ran=random.randint(0, 1)
                
                #first case: the package is delivered (is sent to the delivered packages list)
                if ran and dsm.orders.top().numAttempts <3:
                    #updating the number of attempts
                    dsm.orders.top().numAttempts+=1
                    print("Delivered:", dsm.orders.top().idpac, "delivered by;", dsm.iddsm ,"at attempt:", dsm.orders.top().numAttempts)
                    self.delivered.enqueue(str(dsm.iddsm +dsm.orders.top().idpac))
                    dsm.orders.dequeue()
                    
                #second case: the package is not delivered and the numbers of attempts is less than 3.
                elif ran==0 and dsm.orders.top().numAttempts <3:
                   #updating the number of attempts
                   dsm.orders.top().numAttempts+=1
                   print("Could not be delivered:", dsm.orders.top().idpac, " DSMmber por:",dsm.iddsm, "attempts:", dsm.orders.top().numAttempts)
                   #the package is sent to the end of the list
                   dsm.orders.enqueue(dsm.orders.dequeue())
                    
                #third case: the number of attemps is bigger than 3 so it is sent to incidences 
                else:
                    print("Package incidence:",dsm.orders.top().idpac, " DSMmber por:",dsm.iddsm, "attempts:", dsm.orders.top().numAttempts)
                    self.incidences.enqueue(str(dsm.orders.top().idpac + dsm.iddsm + " number of delivery attempts exceeded"))
                    dsm.orders.dequeue()
          
        #if the dsmember does not have packages to deliver            
        else:
            print(dsm.iddsm, "does not have packages to deliver.")
            
        
    def deliver(self):
        """
        that simulates the delivery of packages from all distributors.
        """           
        for i in range(self.dsmembers.size):
            self.deliverPackages(self.dsmembers.getAt(i).iddsm)
        
    def removeDSMember(self,idrep):
        """receives a distributor (identifier) and sets it as inactive. If the 
        distributor has a pending package to be delivered, it must be 
        reassigned to an active distributor that covers the area of the 
        package. If no available distributor is found, the package will be 
        registered as an incident."""

        #get the index of the dsmember
        check=True
        index=0
        
        while check:
            
            if self.dsmembers.getAt(index).iddsm == idrep:
                check=False
                
            else:
                index+=1
                
        dsm=self.dsmembers.getAt(index)
        #we set the dsmemeber to inactive
        print("Removing DSMember:", dsm.iddsm)
        dsm.status="inactive"
        
        #we add all the packages to the orders list and delete them from the dsmember
        for i in range(dsm.orders.size):
            self.orders.enqueue(dsm.orders.dequeue())
            
        #we follow the same procedure as in assign distribution.
        #If the package can be delivered we sent that pakage to the auxiliary queue
        for a in range(self.dsmembers.size):
            dsm=self.dsmembers.getAt(a)
            myLen=self.orders.size
            for b in range(self.orders.size):
                if dsm.zones.search(self.orders.top().pc) and dsm.status=="Active":
                    print("reassigning package ", self.orders.top().idpac, "to: ", dsm.iddsm)
                    self.auxiliary.enqueue(self.orders.dequeue())
                    
                if self.orders.size==myLen:
                    self.orders.enqueue(self.orders.dequeue()) 
                    
        #the packages that remain in self.orders are sent to incidences because they cannot be delivered        
        for i in range(self.orders.size):
            self.incidences.enqueue(str(self.orders.top().idpac + "delivery staff member not available"))
            self.orders.dequeue()
            
        #we move the packages from the auxiliary list to the self.orders list in order to redistribute    
        for i in range(self.auxiliary.size):
            self.orders.enqueue(self.auxiliary.top())
            self.auxiliary.enqueue(self.auxiliary.dequeue())
            
        #the packages are distributed
        self.assignDistribution()
        
   