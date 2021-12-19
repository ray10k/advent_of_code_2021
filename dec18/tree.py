class LeafNode():
    def __init__(self,number):
        self.number = int(number)
    
    def __int__(self):
        return self.number
    
    def __float__(self):
        return float(self.number)
    
    def __str__(self):
        return str(self.number)
    
    def __repr__(self):
        return f"<{self.number}>"

    def __iadd__(self, other):
        self.number += int(other)
        return self

    def __add__(self,other):
        return self.number + int(other)
    
    def __truediv__(self,other):
        return self.number / float(other)

    def __gt__(self,other):
        return self.number > int(other)
    
    def __ge__(self,other):
        return self.number >= int(other)
    
    def append(self,num):
        self.number *= 10
        self.number += int(num)
    
    def depth(self):
        return 1

    def get_leaves(self):
        return self

class TreeNode():
    def __init__(self,parent = None):
        self.left = None
        self.right = None
        self.parent:TreeNode = parent

    def insert(self,value):
        if not isinstance(value,TreeNode):
            value = LeafNode(value)
        if self.left == None:
            self.left = value
            return
        if self.right == None:
            self.right = value

    def __str__(self):
        return f"[{str(self.left)},{str(self.right)}]"
    def __repr__(self):
        return f"[{repr(self.left)},{repr(self.right)}]"

    def __add__(self, other):
        retval = TreeNode()
        retval.left = self
        retval.right = other
        self.parent = retval
        if isinstance(other,TreeNode):
            other.parent = retval
        return retval
    
    def depth(self):
        l_depth = 0
        r_depth = 0
        if isinstance(self.left,TreeNode):
            l_depth = self.left.depth()
        if isinstance(self.right,TreeNode):
            r_depth = self.right.depth()
        return max(l_depth,r_depth) + 1
    
    def get_leaves(self):
        retval = []
        if isinstance(self.left,TreeNode):
            retval.extend(self.left.get_leaves())
        else:
            retval.append(self.left)
        if isinstance(self.right,TreeNode):
            retval.extend(self.right.get_leaves())
        else:
            retval.append(self.right)
        return tuple(retval)

    def iterate(self,reverse = False):
        first, second = "left","right"
        if reverse:
            first = "right"
            second = "left"
        current = self
        previous = None
        while current is not None:
            if previous is current.__getattribute__(second):
                yield current
                previous = current
                current = current.parent
                continue
            if previous is current.__getattribute__(first):
                candidate = current.__getattribute__(second)
                if isinstance(candidate,TreeNode):
                    previous = current
                    current = candidate
                    continue
                else:
                    previous = candidate
                    continue
            candidate = current.__getattribute__(first)
            if isinstance(candidate,TreeNode):
                previous = current
                current = candidate
                continue
            previous = candidate
            continue