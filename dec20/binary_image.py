import itertools as itt

class BinaryImage():
    def __init__(self,height,width,background) -> None:
        self.width = width
        self.height = height
        self.background = 1 if background else 0
        self.field = [background] * (self.width*self.height)
    
    def __getitem__(self,index):
        pix_index = 0
        h_index,v_index = 0,0
        if isinstance(index,tuple):
            h_index,v_index = index
            pix_index = h_index + (v_index*self.width)
        elif isinstance(index,int):
            h_index = index % self.width
            v_index = index // self.width
            pix_index = index
        else:
            raise TypeError("Expected a tuple or int, got "+str(type(index)))
        
        if h_index in range(0,self.width) and v_index in range(0,self.height):
            return self.field[pix_index]
        return self.background

    def __setitem__(self,index,value):
        pix_index = 0
        h_index,v_index = 0,0
        if isinstance(index,tuple):
            h_index,v_index = index
            pix_index = h_index + (v_index*self.width)
        elif isinstance(index,int):
            pix_index = index
            h_index = index % self.width
            v_index = index // self.width
        else:
            raise TypeError("Expected a tuple or int, got "+str(type(index)))
        
        if h_index in range(0,self.width) and v_index in range(0,self.height):
            self.field[pix_index] = 1 if bool(value) else 0
        #Silently discard out-of-range indices.

    def __iter__(self):
        return iter(self.field)

    def get_neighborhood(self,center_x:int,center_y:int):
        return tuple(
            self[x,y] for y,x in itt.product(
                range(center_y-1,center_y+2),
                range(center_x-1,center_x+2),
                )
            )
    
    def print_image(self):
        dark = '░'
        light = '█'
        for row in range(self.height):
            for column in range(self.width):
                print(light,end="") if self[column,row] == 1 else print(dark,end="")
            print()
        