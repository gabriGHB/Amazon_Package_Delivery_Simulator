from dlist import DList
from binarytreeszone import BinaryTree

 
class Zones(BinaryTree):

    def createZone(self,pc):
         """Method that creates a new zone"""
         self.insert(pc,"zone")
 
    
    def showZones(self):
        """Returns an ascending ordered list of zones"""
        auxZones=self.createList()
        #an inorder method is called
        self.inorderZone(self.root)
        return auxZones
    

    def inorderZone(self,currentNode):
        """Inorder method that, for each zone, prints its dsmembers"""
        if currentNode!=None:
            self.inorderZone(currentNode.leftChild)
            print("Zone: ",currentNode.elem,"\nDistributors: ")
            #for each zone an inorder method is called to print the people
            currentNode.dsmembers.inorder()
            self.inorderZone(currentNode.rightChild)
        
    
       
    def assignsDistributor(self,pc,distributor):
        """Method that assigns a distributor to a zone"""
        zone=self.find(pc)
        zone.dsmembers.insert(distributor,"people")
        
        
    def deleteDistributor(self,pc,distributor):
        """Deletes a given distributor from a given zone"""
        zone=self.find(pc)
        zone.dsmembers.remove(distributor)


    
    def showDistributors(self,pc):
        """Prints the distributors for a given zone"""
        zone=self.find(pc)
        #the inorder prints the distributors in alphabetical order
        zone.dsmembers.inorder()
        auxList=zone.dsmembers.createList()
        return auxList
    
        
        
    def deleteZone(self,CP):
        """Method that deletes a zone and distribibute its people among the adjoining zones"""
        
        #firstly the dsmembers are redistributed
        self.distributeDistributors(CP)
        #the zone is removed
        self.remove(CP)

        
        
    def distributeRight(self,counter,lis,lis2,length):
        """Distribute the dsmembers to the sucessor zones
           The counter makes posible to iterate through the dsmembers,
           the two list in the parameter store the dsmembers                                                               that will receive a package and the packages to redistribute. 
           Finally the length sets when the loop stops. 
           If for example the length == length of the list that means that all the dsmember list should be traverse, if the lenght == half of the length of the dsmembers list that would mean that the packages should be redistributed among half of the people only"""
           
        counter_=counter
        #we create a loop in order to distribute dsmemebers to the succesor zones. The loop is restarted when the           last zone is reached
        while length>0:
            lis.getAt(counter_).dsmembers.insert(lis2.removeLast().elem,"people")
            if counter_==len(lis)-1:
                counter_=counter-1
            counter_+=1
            length-=1

            
    def distributeLeft(self,counter,lis,lis2,length):
        """Distribute the dsmembers to the predecessor zones
           The counter makes posible to iterate through the dsmembers,
           the two list in the parameter store the dsmembers                                                               that will receive a package and the packages to redistribute. 
           Finally the length sets when the loop stops. 
           If for example the length == length of the list that means that all the dsmember list should be traverse, if the lenght == half of the length of the dsmembers list that would mean that the packages should be redistributed among half of the people only"""
           
        counter_=counter
        #we create a loop in order to distribute dsmemebers to the succesor zones. The loop is restarted when the           last zone is reached
        while length>0:
           lis.getAt(counter_).dsmembers.insert(lis2.removeLast().elem,"people")
          
           if counter_==0:
                counter_=counter+1
           counter_-=1
           length-=1

          
    def distributeDistributors(self,CP):
        """This method distirbute the dsmembers among the  adjoining zones"""
        #we set some variables that will be used later
        zone=self.find(CP)
        zonesList=self.createList()
        peopleList=zone.dsmembers.createList()
        index=zonesList.index(zone)
        halfLen=len(peopleList)//2
        halfLen_=len(peopleList)-halfLen
        
        #first case: if the zone to be deleted is the lowest zone all the dsmembers are sent to the greater zones
        if zone.elem == zonesList.head.elem.elem:
            self.distributeRight(1, zonesList, peopleList,len(peopleList))
                
        #second case: if the zone to be deleted is the greatest zone all the dsmembers are sent to the lower zones
        elif zone.elem == zonesList.tail.elem.elem:
            self.distributeLeft(len(zonesList)-2, zonesList, peopleList,len(peopleList))
            
        #third case: dsmemebers are sent half to the left and the other half to the right
        else:
            self.distributeLeft(index-1, zonesList, peopleList, halfLen_)
            self.distributeRight(index+1, zonesList, peopleList, halfLen)
   
    
    def isBalanced(self):
        """Checks if the tree is size-balanced"""
        return self._isSizeBalanced(self.root)
        
    def _isSizeBalanced(self,node):
        if node is None:
            return True
        
        if self.fsize(node)>1:
            return False
        
        return self._isSizeBalanced(node.leftChild) and self._isSizeBalanced(node.rightChild)
     
    def cut(self):
      """This method cuts the tree down"""
      self.root=None


    def createSortList(self):
        """Create a list with the elements sorted following the inorder aproach"""
        aux=DList()
        self.createSortList_(self.root, aux)
        return aux
    
    def createSortList_(self,node,l):
        if node!=None:
            self.createSortList_(node.leftChild,l)
            l.addLast(node.elem)
            self.createSortList_(node.rightChild,l)
     
    def balance(self):
        """This method balances the tree"""
        #we save the data before we cut the tree
        l2=self.createList()
        l=self.createSortList()
        #then we cut the tree
        self.cut()
        #a new balance tree is created
        self.balance_(l)
        #the people is brougth back
        self.reassignPeople(l2)
  
    def balance_(self,l):
        """Method that using divide and conquer creates a balanced tree, this method does not take into account people"""
        """Given a sorted list, firstly the element in the middle is inserted, then we repeate the process for the left half and right half"""
        
        if not self.search(l.getAt(len(l)//2)):
           self.insert(l.getAt(len(l)//2),"zone")
        if len(l)==1:
            return 0
        l3=DList()
        l4=DList()
        for i in range(len(l)//2):
            l3.addLast(l.getAt(i))
        for i in range(len(l)-len(l)//2):
            l4.addLast(l.getAt(len(l)//2+i))
        return self.balance_(l4) + self.balance_(l3)
    
    def reassignPeople(self,l2):
        """Method that brings the people back to their zone, l2 is a list that contains all the data of the tree, this list was created before the tree was cut"""
        counter=0
        while counter<len(l2):
            zone=self.find(l2.getAt(counter).elem)
            #a list with the dsmembers of the zone is created
            aux=l2.getAt(counter).dsmembers.createList()
            counter2=0
            while counter2<len(aux):
                self.assignsDistributor(zone.elem, aux.getAt(counter2).elem)
                counter2+=1
            counter+=1
        

def test():
    objZ=Zones()
    lZones=[28225,28054,28440,28369,28165,28009,28001,28547,28889,28847]
    for z in lZones:
        objZ.createZone(z)

    objZ.draw()
    print()

   # print("Zones:",objZ.showZones())
    print()


    objZ.assignsDistributor(28225,'Herrero, Maria')
    objZ.assignsDistributor(28225,'Segura, Isabel')
    objZ.assignsDistributor(28225,'Abad, Juan')
    
        

    
    objZ.assignsDistributor(28847,'Martinez, Leticia')
    objZ.assignsDistributor(28847,'Sanz, Jorge')
    objZ.assignsDistributor(28847,'Bono, Mario')
    
    
    objZ.assignsDistributor(28165,'Merlo, Luis')
    objZ.assignsDistributor(28165,'Soria, José')
    objZ.assignsDistributor(28165,'Canto, Toni')
    
    objZ.assignsDistributor(28054,'Benitez, Manuel')
    
    objZ.assignsDistributor(28009,'Iglesias, Pablo')
    objZ.assignsDistributor(28009,'Echenique, Pablo')
    
    objZ.assignsDistributor(28001,'Casado, Pablo')
    objZ.assignsDistributor(28001,'Álvarez de Toledo, Cayetana')
    
    objZ.assignsDistributor(28889,'Montero, Irene')
    
    objZ.assignsDistributor(28547,'Ortega Smith, Javier')
    objZ.assignsDistributor(28547,'Abascal, Santiago')


    objZ.assignsDistributor(28440,'Espinosa, Ivan')
    objZ.assignsDistributor(28440,'Monasterio, Rocío')


    
    

    print()
    print(objZ.showZones())
    print()
    
    objZ.draw()

    objZ.deleteDistributor(28001,'Casado, Pablo')
    
    print("Distributors for zone 28001:",objZ.showDistributors(28001))

    objZ.deleteDistributor(28054,'Benitez, Manuel')
    print("Distributors for zone 28054:",objZ.showDistributors(28054))
    objZ.draw()

    objZ.deleteZone(28225)
    objZ.draw()
    objZ.deleteZone(28440)
    objZ.draw()

    print('Is balanced:',objZ.isBalanced())
    print()
    print("BEFORE BALANCE")
    objZ.showZones()
    objZ.balance()
    print("AFTER BALANCE")
    objZ.showZones()
    objZ.deleteZone(28054)
    objZ.balance()
    objZ.showZones()
    
    print()
    objZ.draw()
    print()
    print('Is balanced:',objZ.isBalanced())
    
if __name__ == '__main__':
    test()        
    
