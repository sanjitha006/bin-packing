class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id=bin_id
        self.capacity=capacity
        self.objects=[]

    def add_object(self, new_object):
        # Implement logic to add an object to this bin
        #print(new_object)
        self.objects.append(new_object)

    def remove_object(self, obj_id):
        # Implement logic to remove an object by ID
        for j in self.objects:
            if (j.object_id==obj_id):
                self.objects.remove(j)


