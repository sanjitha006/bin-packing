from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException
from node import Node

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        #avl tree of bins
        self.binsystem=AVLTree()
        self.bin__id=AVLTree()
        self.objectsystem=AVLTree()

    def add_bin(self, bin_id, capacity):
        b=Bin(bin_id,capacity)
        self.binsystem.add_node(capacity,b)
        self.bin__id.add_node(bin_id,b)
        
        

    def add_object(self, object_id, size, color):
        obj = Object(object_id, size, color)


        if color == Color.BLUE:
            t = self.binsystem.find_ceil_leastid(size)
        elif color == Color.YELLOW:
            t = self.binsystem.find_ceil_maxid(size)
        elif color == Color.RED:
            t = self.binsystem.find_largest_minid(size)
        elif color==Color.GREEN:
            t = self.binsystem.find_largest_maxid(size)
   

        if t is None:
            raise NoBinFoundException


        new = Node(t.key - size, t.data)
        self.binsystem._delete_node(t)
        self.binsystem.add_node(new.key, new.data)
        new.data.capacity-=size
        new.data.add_object(obj)
        self.objectsystem.add_node(object_id, (size, new.data))
        
        

                
            

    def delete_object(self, object_id):
 
        x = self.objectsystem.search_node(object_id)
        if x is None:
            raise NoBinFoundException
        
        size, bin_obj = x.data  
        
        bin_obj.remove_object(object_id)
        self.objectsystem._delete_key(object_id)
        y=self.binsystem.search_node(bin_obj.capacity,bin_obj)
        self.binsystem._delete_node(y)
        self.binsystem.add_node(bin_obj.capacity+size,bin_obj)
        bin_obj.capacity+=size
        
        
  



      

    def bin_info(self, bin_id):
        # returns a tuple with current capacity of the bin and the list of objects in the bin (int, list[int])
        g=self.bin__id.search_node(bin_id)
        
        c=g.data.capacity
        l=[]
        for i in g.data.objects:
           # c=c-i.sizeobj
            l.append(i.object_id)
        
        res=(c,l)
        return res
       
        

    def object_info(self, object_id):
        # returns the bin_id in which the object is stored
        x=self.objectsystem.search_node(object_id)
        if(x==None):
            return None
        return(((x.data)[1]).bin_id)


        
    
