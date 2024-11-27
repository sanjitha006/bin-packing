class Node:
    def __init__(self,key,data=None):#check later if height needed
        self.left=None
        self.right=None
        self.data=data
        self.key=key
        self.height=1