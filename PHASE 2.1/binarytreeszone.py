from dlist import DList

class Zone:
  """Class that represents a zone (node of the main tree)"""
  def __init__(self,elem=None):
    self.elem=elem
    self.leftChild=None
    self.rightChild=None
    self.parent=None
    self.dsmembers=BinaryTree()
    
  def __str__(self):
      return str(self.elem)

class People:
  """Class that represents a dsmemeber (node of the the tree of a zone)"""  
  def __init__(self,elem=None):
    self.elem=elem
    self.leftChild=None
    self.rightChild=None
    self.parent=None

  def __str__(self):
      return str(self.elem)  

class BinaryTree:
  
  def __init__(self):
    self.root=None
    
  def __len__(self):
      return self.size()
  
  
  def createList(self):
        l=DList()
        self.createList_(self.root,l)
        return l
    
  def createList_(self,currentNode,l):
        if currentNode!=None:
            self.createList_(currentNode.leftChild,l)
            l.addLast(currentNode)
            self.createList_(currentNode.rightChild,l)
    
  
  def size(self):
    """Returns the number of nodes"""
    return self._size(self.root)
      
  def _size(self,currentNode):
    if currentNode==None:
      return 0
    
    return 1 + self._size(currentNode.leftChild) + self._size(currentNode.rightChild)
   

         
  def inorder(self):
    self._inorder(self.root)
    print()
    
  def _inorder(self,currentNode):
    if currentNode!=None:
         self._inorder(currentNode.leftChild)
         print(currentNode.elem)
         self._inorder(currentNode.rightChild)
            

  def draw(self):
      """Fucntion to draw a tree"""
      self._draw('',self.root,False)
      print()
      
  def _draw(self,prefix, node, isLeft):
    if node !=None:
        self._draw(prefix + "     ", node.rightChild, False)
        print(prefix + ("|-- ") + str(node.elem))
        self._draw(prefix + "     ", node.leftChild, True)
    


  def insert(self,x,string):
        """inserts a new node, with element x, into the tree"""
        if self.root==None:
            if string == 'zone':
                self.root = Zone(x)
            elif string == 'people':
                self.root = People(x)
    
        else:
          self._insertNode(self.root,x, string)
    
  def _insertNode(self,node,x, string):
      """Inserts a new node (with the element x) inside of the subtree node"""
      if node.elem==x:
        # Duplicate elements are not allowed
        print(x,' already exists!!!')
        return
  
      if x<node.elem:
  
        if node.leftChild==None:
            if string == 'zone':
                newNode = Zone(x)
            elif string  == 'people':
                newNode = People(x)
            node.leftChild=newNode
            newNode.parent=node
        else:
          self._insertNode(node.leftChild,x, string)
  
      else: #if x>node.elem
  
        if node.rightChild==None:
            if string == 'zone':
                newNode = Zone(x)
            elif string  == 'people':
                newNode = People(x)
            node.rightChild=newNode
            newNode.parent=node
        else:
          self._insertNode(node.rightChild,x,string)

  def search(self,x):
        return self.searchNode(self.root,x)
    
  def searchNode(self,node,x):
        """Auxiliary method to search a node with value x"""
        if node is None:
            return False
        
        if node.elem==x:
            return True
        
        if x<node.elem:
            return self.searchNode(node.leftChild,x)
        
        if x>node.elem:
            return self.searchNode(node.rightChild,x)
 
  def find(self,x):
        """Returns the node whose element is x. If it is not found, it returns None"""
        return self.findNode(self.root,x)
    
  def findNode(self,node,x):
        if node is None:
            return None
        
        if node.elem==x:
            return node
        
        if x<node.elem:
            return self.findNode(node.leftChild,x)
        
        if x>node.elem:
            return self.findNode(node.rightChild,x)      
          
  def remove(self,x):
        """Searches and removes the node whose element is x"""
        node=self.find(x)
        if node is None:
            print(x,' does not exist!!!')
            return
        self.removeNode(node)
        
        
  def removeNode(self,node):    
        """Auxiliary method to remove the node which takes as parameter"""
        #First case: no children
        if node.leftChild is None and node.rightChild is None:
            parent_node=node.parent
            if parent_node is not None:
                if parent_node.leftChild==node:
                    parent_node.leftChild=None
                else:
                    parent_node.rightChild=None
                node.parent=None
            else:
                self.root=None
            return
        
        #Second case: only one child
        if node.leftChild is not None and node.rightChild is None:
            
            parent_node=node.parent
            if parent_node is not None:
                if parent_node.leftChild==node:
                    parent_node.leftChild=node.leftChild
                else:
                    parent_node.rightChild=node.leftChild
                node.leftChild.parent=parent_node
            else:
                self.root=node.leftChild
            return
        
         #Second case: only one child
        if node.leftChild is None and node.rightChild is not None:
            
            parent_node=node.parent
            if parent_node is not None:
                if parent_node.leftChild==node:
                    parent_node.leftChild=node.rightChild
                else:
                    parent_node.rightChild=node.rightChild
                node.rightChild.parent=parent_node
            else:
                self.root=node.rightChild
            return
            
        #Third case: two children
        successor=node.rightChild
        while successor.leftChild is not None:
            successor=successor.leftChild
            
        #we replace the node's elem by the successor's elem
        node.elem=successor.elem
        #we remove the succesor from the tree
        self.removeNode(successor)
        
  def fsize(self,node):
        """Returns the size balance factor for the input node"""
        if node is None:
            return 0
        return abs(self._size(node.leftChild)-self._size(node.rightChild))
    
  print()

