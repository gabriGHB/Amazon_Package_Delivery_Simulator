from djkistra import GraphDijkstra

class AdjacentVertex:
    """Class that represents an adjacent vertex, it includes the vertex and the weight"""

    def __init__(self,vertex,weight):
        self.vertex=DeliveryPoint(vertex.street,vertex.num,vertex.pc)
        self.weight=weight
  
    def __str__(self):
        return '('+str(self.vertex)+','+str(self.weight)+')'

    def __eq__(self,other):
        if other == None:
            return False
        return self.vertex==other.vertex and self.weight==other.weight
        
        

class DeliveryPoint:
    """Class that represents a vertex of the graph"""
    
    def __init__(self,street,num=None,pc=None):
        self.street=street
        self.num=num
        self.pc=pc
        
    def __eq__(self,other):
        if other==None:
            return False
        
        return self.street==other.street and self.num==other.num and self.pc==other.pc
    
    def __hash__(self):
        return hash(self.street)
    
    
    def __str__(self):
        result=str(self.street)
        if self.num!=None:
            result+=', '+str(self.num)
        if self.pc!=None:
            result+=', '+str(self.pc)
        return result


class Map(GraphDijkstra):
    def __init__(self):
        self.vertices={}
    
    
    def addDeliveryPoint(self,point):
        """Method that creates a delivery point"""
        self.vertices[point]=[]
       
   
        
    def addConnection(self,point1,point2,distance):
        """Method that creates a connection between two points"""
        
        #checking that the parameters are ok
        if point1 not in self.vertices:
            print("Point1 does not exists!!")
            return
        if point2 not in self.vertices:
            print("Point2 does not exits!!")
        if distance<0:
            print("Not valid distance!!")
            return
        
        self.vertices[point1].append(AdjacentVertex(point2,distance))
        self.vertices[point2].append(AdjacentVertex(point1,distance))

        
    def areConnected(self,point1,point2):
        """Method that checks if two points re connected"""
        for i in range(len(self.vertices[point1])):
            if self.vertices[point1][i].vertex==point2:
                return self.vertices[point1][i].weight
        return 0
    
            
    def deleteConnection(self,point1,point2):
        """Method that deletes the connection between two points"""
        
        #checking if the points exist
        if point1 not in self.vertices:
            print("Point1 does not exists!!")
            return
        if point2 not in self.vertices:
            print("Point2 does not exits!!")
        
        #since the graph is undirected the connection should be removed from both verteces
        for i in self.vertices[point1]:
            if i.vertex == point2:
                self.vertices[point1].remove(i)

        for i in self.vertices[point2]:
            if i.vertex == point1:
                self.vertices[point2].remove(i)


    def __str__(self):
        result=''
        for v in self.vertices:
            result+='\n'+str(v)+':'
            for adj in self.vertices[v]:
                result+=str(adj)
                
        return result
        

    def generateRoute(self):
        """This function prints all vertices of the graph by the DFS traversal."""
        
        # Mark all the vertices as not visited 
        visited={}
        result=[]
        for v in self.vertices.keys():
            visited[v]=False
        #if a vertex has not been visited the _dfs method is called
        for v in  self.vertices.keys():
            if visited[v]==False:
              self._dfs(v, visited,result)
        print() 
        return result
    
    
    def _dfs(self, v, visited,result):
         """This funcion prints the DFS traversal from the vertex whose index is index"""
         # Mark the current node as visited and print it 
         visited[v] = True
         print(v,end=' ')
         result.append(v)
         #if the vertex is not visited the method is called again
         for adj in self.vertices[v]: 
             if visited[adj.vertex] == False: 
                 self._dfs(adj.vertex, visited,result)
            
    def minRoute(self, start, end):
        """"Method that prints the path with the minimum distance and the distance between two points"""
        return self.dijkstra(start,end)
        
    
        
        

pA=DeliveryPoint('C/A',1,28921)             #A
pB=DeliveryPoint('C/B',2,28921)             #B
pC=DeliveryPoint('C/C',3,28922)             #C
pD=DeliveryPoint('C/D',4,28922)             #D
pE=DeliveryPoint('C/E',5,28923)             #E
pF=DeliveryPoint('C/F',6,28923)             #F
pG=DeliveryPoint('C/G',6,28923)             #G

points=[pA,pB,pC,pD,pE,pF,pG]
m=Map()
for p in points:
    m.addDeliveryPoint(p)

m.addConnection(pA,pB,8)                    #A,B,8
m.addConnection(pA,pC,9)                    #A,C,9
m.addConnection(pA,pD,14)                   #A,D,14

m.addConnection(pB,pE,15)                   #B,E,15
m.addConnection(pB,pF,11)                   #B,F,11

m.addConnection(pC,pF,2)                    #C,F,2

m.addConnection(pF,pG,8)                    #F,G,8
m.addConnection(pD,pG,2)

m.dijkstra(pA,pG)    
