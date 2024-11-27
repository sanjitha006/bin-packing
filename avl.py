from node import Node
def comp_1(node_1, node_2):
    if node_1.key < node_2.key:
        return -1
    elif node_1.key > node_2.key:
        return 1
    else:
        return 0

class AVLTree:
    def __init__(self, compare_function=comp_1):
        self.root = None
        self.size = 0
        self.comparator = compare_function
    def get_height(self,node):
        if(node==None):
            return(0)
        else:
            return node.height
    def update_height(self, node):
        if (node!=None):
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    def height_diff(self,node):
        if(node==None):
            return 0
        else:
            return(self.get_height(node.left)-self.get_height(node.right))
    def right_rotate(self, x):
        y= x.left
        z = y.right
        y.right = x
        x.left = z
        self.update_height(x)
        self.update_height(y)

        return y
    def left_rotate(self, x):
        y=x.right
        z=y.left
        y.left=x
        x.right=z
        self.update_height(x)
        self.update_height(y)
        return y

    def inorder_successor(self, node):  
      if (node == None):
          return None
      if (node.right != None):
          x= node.right
          while x.left is not None:
              x = x.left
          return x
      successor = None
      curr = self.root  
      while current is not None:
        if node.key < curr.key:
          successor = curr
          curr = curr.left
        elif node.key > curr.key:
          curr = curr.right
        else:
          break

      return successor

           

    def search_node(self, key, data=None):
        def _search(current_node, key, data):
            if current_node is None:
                return None
            if key < current_node.key:
                return _search(current_node.left, key, data)
            elif key > current_node.key:
                return _search(current_node.right, key, data)
            else:
           
                if (data == None or current_node.data == data):
                    return current_node
                else:
                
                    left_search = _search(current_node.left, key, data)
                    if left_search:
                        return left_search
                    return _search(current_node.right, key, data)

        return _search(self.root, key, data)


    def find_ceil_leastid(self,  key):
        ceil_node = None
        node=self.root

        while node:
            if node.key == key:
                
                if ((ceil_node is None) or (node.key<ceil_node.key) or ( node.data.bin_id < ceil_node.data.bin_id and node.key==ceil_node.key)):
                    ceil_node = node
               
                node = node.right

            elif node.key >key:
               
                if ((ceil_node is None) or(node.key<ceil_node.key)or( (node.data.bin_id < ceil_node.data.bin_id) and (node.key==ceil_node.key))):
                    ceil_node = node
              
                node = node.left

            else:
           
                node = node.right
       
        return ceil_node
    def find_ceil_maxid(self, key):
        ceil_node = None
        node=self.root
        while (node!=None):
            if node.key == key:
               
                 if ((ceil_node is None) or (node.key<ceil_node.key) or ( (node.data.bin_id > ceil_node.data.bin_id) and node.key==ceil_node.key)):
                    ceil_node = node
                 node = node.right

            elif node.key > key:
                
                if ((ceil_node is None) or( (node.data.bin_id > ceil_node.data.bin_id )and (node.key==ceil_node.key)) or (node.key<ceil_node.key)):
                   
                        ceil_node = node
                node = node.left

            else:
              
                node = node.right
       
        return ceil_node
    def find_largest_minid(self,size):
        node = self.root
        if node is None:
            return None

        current = node
        largest_node = current

       
        while current.right is not None:
            current = current.right

        largest_node = current 

      
        current = node
        while current is not None:
            if current.key == largest_node.key:
                if current.data.bin_id < largest_node.data.bin_id:
                    largest_node = current  
            current = current.right
    
        return largest_node
        


    def find_largest_maxid(self,size):
        current = self.root
        max_node = None

        while current:
            if max_node is None or current.key > max_node.key:
                max_node = current
            elif current.key == max_node.key:
               
                if current.data.bin_id > max_node.data.bin_id:
                    max_node = current
            current = current.right  


        return max_node
   
    def add_node(self, key, data):
        new_node = Node(key, data)
        self.root = self.insert(self.root, new_node)
   
    
    def insert(self, node, new_node):
        if node is None:
            self.size += 1
            return new_node

        if self.comparator(new_node, node) < 0:
            node.left = self.insert(node.left, new_node)
        else:
            node.right = self.insert(node.right, new_node)

   
        self.update_height(node)

        balance = self.height_diff(node)

        if( balance > 1 and self.comparator(new_node, node.left) < 0):
            return self.right_rotate(node)


        elif( balance < -1 and self.comparator(new_node, node.right) > 0):
            return self.left_rotate(node)

        elif( balance > 1 and self.comparator(new_node, node.left) > 0):
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        elif( balance < -1 and self.comparator(new_node, node.right) < 0):
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def _delete_key(self,key):
        self.root = self._delete(self.root, key)

    def print_tree(self, node, level=0, side="root"):
        if node is not None:
            print("    " * level + f"{side}: Node({node.key}, height={node.height})")
            self.print_tree(node.left, level + 1, "left")
            self.print_tree(node.right, level + 1, "right")

    def _delete(self, node, key):
      if node is None:
        return None

      if key < node.key:
        node.left = self._delete(node.left, key)
      elif key > node.key:
        node.right = self._delete(node.right, key)
      else:
        if node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        
        temp = self.inorder_successor(node)
        node.key = temp.key
        node.data = temp.data
        node.right = self._delete(node.right, temp.key)

      self.update_height(node)
      balance = self.height_diff(node)


      if balance > 1:
        if self.height_diff(node.left) >= 0:
            return self.right_rotate(node)
        else:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

      if balance < -1:
        if self.height_diff(node.right) <= 0:
            return self.left_rotate(node)
        else:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

      return node
   

    

    def _delete_node(self, node):
        def _delete(current_node, node_to_delete):
            if current_node is None:
                return None

            if node_to_delete.key < current_node.key:
                current_node.left = _delete(current_node.left, node_to_delete)

            elif node_to_delete.key > current_node.key:
                current_node.right = _delete(current_node.right, node_to_delete)

   
            elif node_to_delete.key == current_node.key and node_to_delete.data == current_node.data:
            
                if current_node.left is None:
                    return current_node.right
                elif current_node.right is None:
                    return current_node.left
       
                temp = self.inorder_successor(current_node)
            
                current_node.key = temp.key
                current_node.data = temp.data

                current_node.right = _delete(current_node.right, temp)

    
            elif node_to_delete.key == current_node.key and node_to_delete.data != current_node.data:
    
                current_node.right = _delete(current_node.right, node_to_delete)
   
            self.update_height(current_node)
            balance = self.height_diff(current_node)

            if balance > 1 and self.height_diff(current_node.left) >= 0:
                return self.right_rotate(current_node)
            if balance > 1 and self.height_diff(current_node.left) < 0:
                current_node.left = self.left_rotate(current_node.left)
                return self.right_rotate(current_node)

            if balance < -1 and self.height_diff(current_node.right) <= 0:
                return self.left_rotate(current_node)
            if balance < -1 and self.height_diff(current_node.right) > 0:
                current_node.right = self.right_rotate(current_node.right)
                return self.left_rotate(current_node)

            return current_node

        # Start the recursive deletion from the root
        self.root = _delete(self.root, node)
