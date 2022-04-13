import sys
 
class GraphDijkstra:

    def minDistance(self, distances, visited): 
        """This functions returns the vertex (index) whose associated value in
        the dictionary distances is the smallest value. We 
        only consider the set of vertices that have not been visited"""
        # Initilaize minimum distance for next node 
        min = sys.maxsize 

        #returns the vertex with minimum distance from the non-visited vertices
        for vertex in self.vertices.keys(): 
            if distances[vertex] <= min and visited[vertex] == False: 
                min = distances[vertex] #update the new smallest
                min_vertex = vertex      #update the index of the smallest
    
        return min_vertex 



    def dijkstra(self, origin,end=None): 
        """"This function takes a vertex v and calculates its mininum path 
        to the rest of vertices by using the Dijkstra algoritm"""  
        
        #visisted is a dictionary whose keys are the verticies of our graph. 
        #When we visite a vertex, we must mark it as True. 
        #Initially, all vertices are defined as False (not visited)
        visited={}
        for v in self.vertices.keys():
            visited[v]=False

        #this dictionary will save the previous vertex for the key in the minimum path
        previous={}
        for v in self.vertices.keys():
            #initially, we defines the previous vertex for any vertex as None
            previous[v]=None


        #This distance will save the accumulate distance from the  
        #origin to the vertex (key)
        distances={}
        for v in self.vertices.keys():
            distances[v]=sys.maxsize


        #The distance from origin to itself is 0
        distances[origin] = 0
        
        for n in range(len(self.vertices)): 
            # Pick the vertex with the minimum distance vertex.
            # u is always equal to origin in first iteration 
            u = self.minDistance(distances, visited) 

            visited[u] = True
            
            # Update distance value of the u's adjacent vertices only if the current  
            # distance is greater than new distance and the vertex in not in the shotest path tree 
            
            #we must visit all adjacent vertices (neighbours) for u
            for adj in self.vertices[u]: 
                i=adj.vertex
                w=adj.weight
                if visited[i]==False and distances[i]>distances[u]+w:
                    #we must update because its distance is greater than the new distance
                    distances[i]=distances[u]+w   
                    previous[i]=u       
                
        #finally, we print the minimum path from origin to the other vertices
        return self.printSolution(distances,previous,origin,end)
        

  

    def printSolution(self,distances,previous,origin,end): 
        print("Mininum path from ",origin)
        for i in self.vertices.keys():
            if distances[i]==sys.maxsize:
                print("There is not path from ",origin,' to ',i)
            else: 
                #minimum_path is the list wich contains the minimum path from v to i
                minimum_path=[]
                print_path=[]
                prev=previous[i]
                #this loop helps us to build the path
                while prev!=None:
                    minimum_path.insert(0,prev)
                    print_path.insert(0,str(prev))
                    prev=previous[prev]
                
                #we append the last vertex, which is i
                minimum_path.append(i)  
                print_path.append(str(i))
                #we print the path from v to i and the distance
                if end:
                    if i==end:
                        print(origin,'->',i,":", print_path ,distances[i])
                        return minimum_path,distances[i]
                else:
                    print(origin,'->',i,":", print_path ,distances[i])